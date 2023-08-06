"""LICENSE
Copyright 2020 Hermann Krumrey <hermann@krumreyh.com>

This file is part of betbot.

betbot is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

betbot is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with betbot.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

import os
import csv
import time
import requests
import dryscrape
from datetime import datetime
from io import StringIO
from bs4 import BeautifulSoup
from webkit_server import InvalidResponseError
from typing import List, Tuple, Dict, Optional
from betbot.neural.data.vector.InputVector import InputVector
from betbot.neural.data.vector.OutputVector import OutputVector
from betbot.neural.data.Match import Match
from betbot.neural.data.DataFetcher import DataFetcher
from betbot.neural.data.enums import Bookmakers, Countries
from betbot.neural.data.names import oddsportal_to_football_data


class FootballDataFetcher(DataFetcher):
    """
    Class that uses football-data.org to fetch data
    """

    def load(self) -> Dict[str, Dict[int, Dict[int, List[Dict[str, str]]]]]:
        """
        Loads the match data from the internet
        :return: The data as dictionaries representing matches,
                 mapped to their respective countries, leagues and seasons
        """
        csv_urls = self._load_csv_urls()
        self.logger.info("Loaded all CSV URLs")
        loaded: Dict[str, Dict[int, Dict[int, List[Dict[str, str]]]]] = {}
        for country, leagues in csv_urls.items():
            loaded[country] = {}
            for league, seasons in leagues.items():
                loaded[country][league] = {}
                for season, url in seasons.items():
                    self.logger.info(f"Loading data for "
                                     f"{country}/{league}/{season}")
                    loaded[country][league][season] = self._load_csv_data(
                        country,
                        league,
                        season,
                        url
                    )
        return loaded

    def get_training_data(self) \
            -> List[Tuple[Match, InputVector, OutputVector]]:
        """
        :return: All training data from previous matches
        """
        vectors = []
        all_matches = self.load_matches()
        segmented_matches = self.segment_matches_by_team(all_matches)

        for country, matches in all_matches.items():
            self.logger.info(f"Getting Training Data for {country}")
            for match in matches:

                histories = []
                for team in [match.home_team, match.away_team]:
                    team_matches = segmented_matches[country][team]
                    team_history = []

                    for team_match in team_matches:
                        if match == team_match:
                            break
                        else:
                            team_history.append(team_match)
                    histories.append(team_history)

                home_history, away_history = histories
                if len(home_history) < 34 or len(away_history) < 34:
                    continue  # Minimum history of 34 matches

                assert match.home_ft_score is not None
                assert match.away_ft_score is not None

                input_vector = InputVector.from_data(
                    match, home_history, away_history
                )
                output_vector = OutputVector(
                    match.home_ft_score, match.away_ft_score
                )
                vectors.append((match, input_vector, output_vector))

        return vectors

    def get_current_matchday_vectors(
            self,
            country: str,
            league: int
    ) -> List[Tuple[InputVector, Match]]:
        """
        Retrieves input vectors for the current matchday
        :param country: The country for which to fetch vectors
        :param league: The league for which to fetch vectors
        :return: The input vectors and the corresponding match objects
        """
        country_enum = Countries(country)
        if country_enum != Countries.GERMANY or league != 1:
            self.logger.warning("Unsupported league")
            return []
        league_identifier = "D1"  # TODO Generalize

        csv_urls = self._load_csv_urls([country_enum])
        current_season = max(csv_urls[country][league].keys())
        now_url = "https://www.football-data.co.uk/fixtures.csv"
        current_url = csv_urls[country][league][current_season]
        lower_url = csv_urls[country][league + 1][current_season]
        previous_url = csv_urls[country][league][current_season - 1]
        previous_lower_url = csv_urls[country][league + 1][current_season - 1]

        current_data = self._load_csv_data(
            country, league, current_season, current_url
        )
        lower_data = self._load_csv_data(
            country, league + 1, current_season, lower_url
        )
        previous_data = self._load_csv_data(
            country, league, current_season - 1, previous_url
        )
        previous_lower_league_data = self._load_csv_data(
            country, league + 1, current_season - 1, previous_lower_url
        )

        with StringIO(requests.get(now_url).text) as f:
            data = [x for x in csv.reader(f)]
            keys = [x.lower() for x in data.pop(0)]
            data = [x for x in data if x[0] == league_identifier]

        current_matches = []
        base_match_dict = {
            "country": country,
            "season": str(current_season),
            "league": str(league),
            "finished": str(False)
        }
        for item in data:
            match_dict = {keys[i]: item[i] for i in range(len(keys))}
            match_dict.update(base_match_dict)
            match = Match.from_football_data(match_dict)
            if match is not None and match.date > datetime.utcnow():
                current_matches.append(match)

        if len(current_matches) == 0:
            retry = 0
            self.logger.info("football-data not available, using oddportal")
            while retry < 3:
                retry += 1
                try:
                    current_matches = self.load_oddsportal_matches()
                except InvalidResponseError:
                    self.logger.warning("Failed to fetch data from oddsportal")
                    if retry < 3:
                        self.logger.info("Retrying...")
                        time.sleep(15)
                    else:
                        self.logger.warning("Couldn't fetch data")
                        return []

        _all_matches = [
            Match.from_football_data(x)
            for x in
            current_data +
            lower_data +
            previous_data +
            previous_lower_league_data
        ]
        all_matches = current_matches + \
            [x for x in _all_matches if x is not None]
        all_matches.sort(key=lambda x: x.date, reverse=True)

        current_matchday = all_matches[0:9]
        all_matches = all_matches[9:]

        vector_matches = []
        for match in current_matchday:
            team_history: Dict[str, List[Match]] = {}
            for team in [match.home_team, match.away_team]:
                team_history[team] = []
                for other_match in all_matches:
                    if team in [other_match.home_team, other_match.away_team]:
                        team_history[team].append(other_match)

            input_vector = InputVector.from_data(
                match,
                team_history[match.home_team],
                team_history[match.away_team]
            )
            vector_matches.append((input_vector, match))

        return vector_matches

    @staticmethod
    def load_oddsportal_matches() -> List[Match]:
        """
        Loads match data from oddsportal
        :return: THe match data from oddsportal
        """
        session = dryscrape.Session()
        headers = {"User-Agent": "Mozilla/5.0"}
        bl_url = "https://www.oddsportal.com/soccer/germany/bundesliga/"
        resp = requests.get(bl_url, headers=headers)
        soup = BeautifulSoup(resp.text, "html.parser")
        entries = soup.find("table", {"id": "tournamentTable"})
        matches = [x for x in entries.find_all("tr") if "\xa0---" in x.text]
        urls = [
            os.path.join(
                "https://www.oddsportal.com",
                x.select("a")[1]["href"][1:]
            ) for x in matches
        ]

        matches = []
        bookmakers = {
            "bet365": Bookmakers.B365,
            "bwin": Bookmakers.BWIN,
            "William Hill": Bookmakers.WILLIAM_HILL
        }
        for url in urls:
            session.visit(url)
            match_soup = BeautifulSoup(session.body(), "html.parser")

            teams = match_soup.find("h1").text
            home_team = teams.split("-")[0].strip()
            away_team = teams.split("-")[1].strip()

            home_team = oddsportal_to_football_data.get(home_team, home_team)
            away_team = oddsportal_to_football_data.get(away_team, away_team)

            date_string = match_soup.find("p", "date").text.split(", ", 1)[1]
            date = datetime.strptime(date_string, "%d %b %Y, %H:%M")

            odds_table = match_soup.find("table", {"class": "detail-odds"})
            if odds_table is None:
                continue
            odds = {}
            for row in odds_table.find_all("tr"):
                tds = row.find_all("td")
                if len(tds) < 1:
                    continue
                name = tds[0].text.strip()
                if name in bookmakers:
                    bookmaker_odds = []
                    for index in range(1, 4):
                        try:
                            odds_number = float(tds[index].text)
                        except ValueError:
                            fraction = [
                                int(x) for x in tds[index].text.split("/")
                            ]
                            odds_number = 1.0 + (fraction[0] / fraction[1])
                        bookmaker_odds.append(odds_number)
                    bookmaker_odds_tuple = (
                        bookmaker_odds[0], bookmaker_odds[1], bookmaker_odds[2]
                    )
                    odds[bookmakers[name]] = bookmaker_odds_tuple

            matches.append(Match(
                "germany",
                1,
                2020,
                date,
                False,
                home_team,
                away_team,
                None, None, None, None,
                odds
            ))
        matches.sort(key=lambda x: x.date)
        return matches[0:9]

    def _load_csv_urls(self, limit_by: Optional[List[Countries]] = None) \
            -> Dict[str, Dict[int, Dict[int, str]]]:
        """
        Retrieves the URLs to all CSV files containing the statistics from
        football-data.co.uk
        :param limit_by: Optionally limits the countries to load data for
        :return: The URLs to the csv files, categorized by country, league and
                 season.
        """
        if limit_by is None:
            limit_by = [x for x in Countries]
        countries = [x.value for x in limit_by]

        base_url = "https://www.football-data.co.uk/"
        csv_urls: Dict[str, Dict[int, Dict[int, str]]] = {}
        for country in countries:
            self.logger.info(f"Loading CSV URLs for {country}")
            csv_urls[country] = {}
            url = f"{base_url}/{country}m.php"
            soup = BeautifulSoup(requests.get(url).text, "html.parser")

            for a in soup.select("a"):
                href = a["href"]
                if href.endswith("csv"):
                    csv_url = os.path.join(base_url, href)
                    season_string = href.split("/")[-2]
                    league_string = href.split("/")[-1]

                    # This will break once we hit 2090
                    # Let's hope this code won't still be used by then
                    century = "19" if season_string.startswith("9") else "20"
                    season = int(century + season_string[0:2])
                    try:
                        league = int("".join([
                            x for x in league_string if x.isdigit()
                        ]))
                    except ValueError:
                        continue

                    if league not in csv_urls[country]:
                        csv_urls[country][league] = {}
                    csv_urls[country][league][season] = csv_url
        return csv_urls

    # noinspection PyMethodMayBeStatic
    def _load_csv_data(
            self,
            country: str,
            league: int,
            season: int,
            csv_url: str
    ) -> List[Dict[str, str]]:
        """
        Loads the data from a CSV file and turns it into match dictionaries
        :param csv_url: The URL to the CSV file
        :return: The matches from the CSV file as dictionaries
        """
        required_keys = [
            "date",
            "hthg",
            "htag",
            "fthg",
            "ftag",
            "hometeam",
            "awayteam"
        ]
        for bookmaker in Bookmakers:
            required_keys += [bookmaker.value + x for x in ["h", "a", "d"]]

        with StringIO(requests.get(csv_url).text) as f:
            data = [x for x in csv.reader(f)]
        keys = data.pop(0)

        while keys[-1] == "":
            keys.pop()

        data_dicts = []
        for entry in data:
            while len(entry) < len(keys):
                entry.append("")
            match = {
                keys[i].lower(): entry[i] for i in range(len(keys))
            }
            invalid = False
            for key in required_keys:
                if match.get(key, "") == "":
                    invalid = True
            if not invalid:
                match.update({
                    "country": country,
                    "season": str(season),
                    "league": str(league),
                    "finished": str(True)
                })
                data_dicts.append(match)

        return data_dicts

    def load_matches(self) -> Dict[str, List[Match]]:
        """
        Loads all matches segmented by country
        :return: {country: [matches]}
        """
        all_matches: Dict[str, List[Match]] = {}
        for country, leagues in self.data.items():
            all_matches[country] = []
            for league, seasons in leagues.items():
                for season, match_data in seasons.items():
                    for match_json in match_data:
                        match = Match.from_football_data(match_json)
                        if match is not None:
                            all_matches[country].append(match)
        return all_matches

    # noinspection PyMethodMayBeStatic
    def segment_matches_by_team(self, all_matches: Dict[str, List[Match]]) \
            -> Dict[str, Dict[str, List[Match]]]:
        """
        Segments matches by the teams involved in them
        :param all_matches: Data on all matches
        :return: The segmented match data
        """
        matches_by_team: Dict[str, Dict[str, List[Match]]] = {}
        for country, matches in all_matches.items():
            matches_by_team[country] = {}
            teams = []
            for match in matches:
                teams += [match.home_team, match.away_team]

            for team in set(teams):
                matches_by_team[country][team] = []
                for match in matches:
                    if match.home_team == team or match.away_team == team:
                        matches_by_team[country][team].append(match)
                matches_by_team[country][team].sort(key=lambda x: x.date)
        return matches_by_team

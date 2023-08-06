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

import time
import dryscrape
from math import sqrt
from bs4 import BeautifulSoup
from typing import List, Tuple
from betbot.api.Bet import Bet
from betbot.api.Match import Match
from betbot.prediction.Predictor import Predictor


class TipicoOddsPredictor(Predictor):
    """
    Class that determinalistically predicts matches based on Tipico quotes
    """

    @classmethod
    def name(cls) -> str:
        """
        :return: The name of the predictor
        """
        return "tipico-odds"

    def predict(self, matches: List[Match]) -> List[Bet]:
        """
        Performs the prediction
        :param matches: The matches to predict
        :return: The predictions as Bet objects
        """
        tipico = self.load_tipico_data(matches[0].matchday)
        bets = []

        for home_team, away_team, home_odds, draw_odds, away_odds in tipico:
            match_found = False
            for match in matches:
                if home_team == match.home_team \
                        and away_team == match.away_team:
                    print(match.home_team)
                    print(match.away_team)
                    bet = self.generate_bet(
                        match.id, home_odds, draw_odds, away_odds
                    )
                    bets.append(bet)
                    match_found = True

            if not match_found:
                self.logger.warning(f"Failed to match {home_team}:{away_team}")

        return bets

    # noinspection PyMethodMayBeStatic
    def load_tipico_data(self, matchday: int) \
            -> List[Tuple[str, str, float, float, float]]:
        """
        Loads tipico quote data for the 2020/21 bundesliga season
        :param matchday: The matchday for which to retrieve the data
        :return: The quote data as a list of tuples of the form:
                    home team name, away team name,
                    home win odds, draw odds, away win odds
        """
        session = dryscrape.Session()
        tipico_data = []
        url = f"https://s5.sir.sportradar.com/tipico/de/1/season" \
              f"/77189/fixtures/round/21-{matchday}"
        session.visit(url)
        time.sleep(5)
        body = session.body()
        with open("x.html", "w") as f:
            f.write(body)
        soup = BeautifulSoup(body, "html.parser")
        matches = soup.findAll("tr", {"class": "cursor-pointer"})
        for match in matches:
            names = match.findAll("div", {"class": "wrap"})
            odds = match.findAll("button", {"class": "odds-normal-content"})
            home = names[2].text
            away = names[5].text
            home_odds = float(odds[0].text)
            draw_odds = float(odds[1].text)
            away_odds = float(odds[2].text)

            translator = {  # Tipico -> Hk-Tippspiel
                "ARB": "BIE",
                "KOE": "FCK",
                "UNI": "SCU",
                "WOB": "VFL",
                "BSC": "BSC",
                "SGE": "SGE",
                "BMG": "BMG",
                "SCU": "SCU",
                "SCH": "S04",
                "BMÜ": "FCB",
                "LEV": "B04"
            }
            home = translator.get(home, home)
            away = translator.get(away, away)

            tipico_data.append((home, away, home_odds, draw_odds, away_odds))
        from pprint import pprint
        pprint(tipico_data)
        return tipico_data

    # noinspection PyMethodMayBeStatic
    def generate_bet(
            self,
            match_id: int,
            home_odds: float,
            draw_odds: float,
            away_odds: float
    ) -> Bet:
        """
        Generates a Bet based on the quote data
        :param match_id: The ID of the match to vote on
        :param home_odds: The odds that the home team wins
        :param draw_odds: The odds that the match ends in a draw
        :param away_odds: The odds that the away team wins
        :return: The generated bet
        """
        winner = int(sqrt(abs(home_odds - away_odds) * 2))
        loser = int(min(home_odds, away_odds) - 1)

        if home_odds < away_odds:
            home_score, away_score = winner, loser
        else:
            home_score, away_score = loser, winner

        if draw_odds > home_odds and draw_odds > away_odds:
            home_score += 1
            away_score += 1

        return Bet(match_id, home_score, away_score)

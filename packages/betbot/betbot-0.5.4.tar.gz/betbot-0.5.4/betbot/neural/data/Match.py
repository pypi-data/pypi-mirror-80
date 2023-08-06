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

from datetime import datetime
from typing import Optional, Tuple, Dict
from dataclasses import dataclass
from betbot.neural.data.enums import Bookmakers


@dataclass
class Match:
    """
    Models the required attributes of a Match
    """
    country: str
    league: int
    season: int
    date: datetime
    finished: bool
    home_team: str
    away_team: str
    home_ht_score: Optional[int]
    away_ht_score: Optional[int]
    home_ft_score: Optional[int]
    away_ft_score: Optional[int]
    bet_odds: Dict[Bookmakers, Tuple[float, float, float]]

    @classmethod
    def from_football_data(cls, data: Dict[str, str]) -> Optional["Match"]:
        """
        Generates a match based on data from football-data.co.uk
        :param data: The data to use
        :return: The generated Match
        """
        try:
            date = datetime.strptime(data["date"], "%d/%m/%Y")
        except ValueError:
            date = datetime.strptime(data["date"], "%d/%m/%y")

        bet_odds: Dict[Bookmakers, Tuple[float, float, float]] = {}
        for bookmaker in Bookmakers:
            try:
                home = data[bookmaker.value + "h"]
                away = data[bookmaker.value + "a"]
                draw = data[bookmaker.value + "d"]
                bet_odds[bookmaker] = (float(home), float(away), float(draw))
            except (KeyError, ValueError):
                return None

        away_ht = None if not data.get("htag") else int(data["htag"])
        away_ft = None if not data.get("ftag") else int(data["ftag"])
        home_ht = None if not data.get("hthg") else int(data["hthg"])
        home_ft = None if not data.get("fthg") else int(data["fthg"])

        return cls(
            country=data["country"],
            league=int(data["league"]),
            season=int(data["season"]),
            date=date,
            finished=bool(data["finished"]),
            home_team=data["hometeam"],
            away_team=data["awayteam"],
            home_ht_score=home_ht,
            home_ft_score=home_ft,
            away_ht_score=away_ht,
            away_ft_score=away_ft,
            bet_odds=bet_odds
        )

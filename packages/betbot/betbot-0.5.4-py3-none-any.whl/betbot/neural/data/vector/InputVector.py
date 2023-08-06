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

from typing import List, Dict, Tuple
from dataclasses import dataclass
from betbot.neural.data.Match import Match
from betbot.neural.data.enums import Bookmakers
from betbot.neural.data.vector.Vector import Vector


@dataclass
class InputVector(Vector):
    """
    Class that models an input vector for use as training data for a
    neural network
    """
    bet_odds: Dict[Bookmakers, Tuple[float, float, float]]
    average_goals: Dict[str, Dict[str, Dict[int, float]]]
    average_odds: Dict[str, Dict[Bookmakers, Dict[str, Dict[int, float]]]]

    @classmethod
    def from_data(
            cls,
            match: Match,
            home_history: List[Match],
            away_history: List[Match]
    ) -> "InputVector":
        """
        Generates an input vector based on match and historical match data
        :param match: The match data
        :param home_history: Historical match data for the home team
        :param away_history: Historical match data for the away team
        :return: The generated input vector object
        """
        # Format: {"home": {"goals_for": {5: 3.5}}}
        average_goals: Dict[str, Dict[str, Dict[int, float]]] = {
            side: {
                category: {} for category in ["goals_for", "goals_against"]
            } for side in ["home", "away"]
        }
        # Format: {"home": {"bwin": {"for": {3: 2.5}}}}
        average_odds: Dict[str, Dict[Bookmakers, Dict[str, Dict[int, float]]]]\
            = {
            side: {
                bookmaker: {
                    category: {} for category in ["for", "against", "draw"]
                } for bookmaker in Bookmakers
            } for side in ["home", "away"]
        }

        for side, history in [("home", home_history), ("away", away_history)]:
            history.sort(key=lambda x: x.date, reverse=True)

            for interval in [5, 17, 34]:
                goals_for = 0
                goals_against = 0
                odds_for = {bookmaker: 0.0 for bookmaker in Bookmakers}
                odds_against = {bookmaker: 0.0 for bookmaker in Bookmakers}
                odds_draw = {bookmaker: 0.0 for bookmaker in Bookmakers}

                for history_match in history[0:interval]:

                    if history_match.home_ft_score is None \
                            or history_match.away_ft_score is None:
                        interval -= 1
                        continue

                    is_home_team = history_match.home_team == match.home_team
                    if is_home_team:
                        goals_for += history_match.home_ft_score
                        goals_against += history_match.away_ft_score
                    else:
                        goals_for += history_match.away_ft_score
                        goals_against += history_match.home_ft_score

                    for bookmaker in Bookmakers:
                        if is_home_team:
                            for_, against, draw = match.bet_odds[bookmaker]
                        else:
                            against, for_, draw = match.bet_odds[bookmaker]
                        odds_for[bookmaker] += for_
                        odds_against[bookmaker] += against
                        odds_draw[bookmaker] += draw

                average_goals[side]["goals_for"][interval] = \
                    goals_for / interval
                average_goals[side]["goals_against"][interval] = \
                    goals_against / interval
                for bookmaker in Bookmakers:
                    average_odds[side][bookmaker]["for"][interval] = \
                        odds_for[bookmaker] / interval
                    average_odds[side][bookmaker]["against"][interval] = \
                        odds_against[bookmaker] / interval
                    average_odds[side][bookmaker]["draw"][interval] = \
                        odds_draw[bookmaker] / interval

        return cls(match.bet_odds, average_goals, average_odds)

    @property
    def vector(self) -> List[float]:
        """
        :return: A vector of floats that can be used to train neural networks
        """
        vector = []

        bookmaker_names = sorted([x.value for x in Bookmakers])

        for bookmaker_name in bookmaker_names:
            bookmaker = Bookmakers(bookmaker_name)
            vector += list(self.bet_odds[bookmaker])

        for side, categories in sorted(self.average_goals.items()):
            for category, intervals in sorted(categories.items()):
                for interval, value in sorted(intervals.items()):
                    vector.append(value)

        for side, bookmakers in sorted(self.average_odds.items()):
            for bookmaker_name in bookmaker_names:
                bookmaker = Bookmakers(bookmaker_name)
                categories = bookmakers[bookmaker]
                for category, intervals in sorted(categories.items()):
                    for interval, value in sorted(intervals.items()):
                        vector.append(value)
        return vector

    @classmethod
    def legend(cls) -> List[str]:
        """
        :return: Strings describing the individual parts of the vectors
        """
        keys = []
        bookmaker_names = sorted([x.value for x in Bookmakers])

        for bookmaker_name in bookmaker_names:
            keys += [bookmaker_name + x for x in ["h", "a", "d"]]

        for side in sorted(["home", "away"]):
            for category in sorted(["goals_for", "goals_against"]):
                for interval in sorted([5, 17, 34]):
                    keys.append(f"AVG-{side}-{category}({interval})")

        for side in sorted(["home", "away"]):
            for bookmaker_name in bookmaker_names:
                for category in sorted(["for", "against", "draw"]):
                    for interval in sorted([5, 17, 34]):
                        keys.append(f"AVG-{side}-{bookmaker_name}-"
                                    f"{category}({interval})")
        return keys

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

from typing import List
from dataclasses import dataclass
from betbot.neural.data.vector.Vector import Vector


@dataclass
class OutputVector(Vector):
    """
    Class that models an output vector for a match
    """
    home_goals: int
    away_goals: int

    @property
    def vector(self) -> List[float]:
        """
        :return: The vector as a list of float values
        """
        return [float(self.home_goals), float(self.away_goals)]

    @classmethod
    def legend(cls) -> List[str]:
        """
        :return: Strings describing the individual parts of the vectors
        """
        return [
            "home_team_ft_score",
            "away_team_ft_score"
        ]

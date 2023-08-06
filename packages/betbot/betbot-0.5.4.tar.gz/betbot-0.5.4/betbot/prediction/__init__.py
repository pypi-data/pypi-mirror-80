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

from typing import Type, List
from betbot.prediction.MatchHistoryNNPredictor import TableHistoryNNPredictor
from betbot.prediction.Predictor import Predictor
from betbot.prediction.DrawPredictor import DrawPredictor
from betbot.prediction.RandomPredictor import RandomPredictor
from betbot.prediction.TipicoOddsPredictor import TipicoOddsPredictor

predictors: List[Type[Predictor]] = [
    DrawPredictor,
    RandomPredictor,
    TipicoOddsPredictor,
    TableHistoryNNPredictor
]

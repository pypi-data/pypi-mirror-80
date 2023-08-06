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
from typing import List
from betbot.api.Bet import Bet
from betbot.api.Match import Match
from betbot.prediction.Predictor import Predictor
from betbot.neural.data.names import abbreviations_to_football_data
from betbot.neural.data.FootballDataFetcher import FootballDataFetcher
from betbot.neural.keras.MatchHistoryTrainer import MatchHistoryTrainer


class TableHistoryNNPredictor(Predictor):
    """
    Class that predicts results based on historical match data
    """

    def __init__(self):
        """
        Initializes the Neural Network.
        Loads existing weights if they exist, otherwise will train new weights
        """
        super().__init__()
        self.model_data_path = os.path.join(self.model_dir, self.name())
        trainer = MatchHistoryTrainer(self.model_data_path)
        self.model = trainer.load_trained_model(minimum_accuracy=41.5)

    @classmethod
    def name(cls) -> str:
        """
        :return: The name of the predictor
        """
        return "match-history"

    def predict(self, matches: List[Match]) -> List[Bet]:
        """
        Performs the prediction
        :param matches: The matches to predict
        :return: The predictions as Bet objects
        """
        bets = []
        vector_data = FootballDataFetcher().get_current_matchday_vectors(
            "germany", 1
        )
        predictions = self.model.predict(
            [x[0].vector for x in vector_data]
        ).tolist()

        match_id_info = {}
        for api_match in matches:
            home_team = abbreviations_to_football_data.get(
                api_match.home_team, api_match.home_team
            )
            away_team = abbreviations_to_football_data.get(
                api_match.away_team, api_match.away_team
            )
            match_id_info[(home_team, away_team)] = api_match.id

        for i, (input_vector, match) in enumerate(vector_data):
            result = [int(round(x)) for x in predictions[i]]
            match_id = match_id_info.get((match.home_team, match.away_team))
            if match_id is not None:
                bets.append(Bet(match_id, result[0], result[1]))

        return bets

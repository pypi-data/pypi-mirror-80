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
from typing import List, Tuple
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Flatten, Dense
from tensorflow.keras import backend
from betbot.neural.keras.BetPredictorTrainer import BetPredictorTrainer
from betbot.neural.data.FootballDataFetcher import FootballDataFetcher
from betbot.neural.data.vector.OutputVector import OutputVector
from betbot.neural.data.vector.InputVector import InputVector


class MatchHistoryTrainer(BetPredictorTrainer):
    """
    Trainer Class that specifies a neural network for use with historical
    match data
    """

    def load_training_data(self, force_refresh: bool) \
            -> List[Tuple[List[float], List[float]]]:
        """
        Loads data for training the model
        :param force_refresh: Forces a refresh of data
        :return: The training data, with the input and output vectors separate
        """
        csv_file = os.path.join(self.model_dir, "training.csv")
        fetcher = FootballDataFetcher()
        self.logger.info("Loading Training Data")
        if not os.path.isfile(csv_file) or force_refresh:
            fetcher.write_training_vectors_to_csv(csv_file)
        self.logger.info("Done")
        return fetcher.load_training_vectors(csv_file)

    def _define_model(self) -> Model:
        """
        Specifies the model of the neural network
        :return: The model
        """
        model = Sequential()
        model.add(Flatten(input_shape=(len(InputVector.legend()),)))
        model.add(Dense(len(InputVector.legend()) - 10, activation="sigmoid"))
        model.add(Dense(len(OutputVector.legend()), activation="relu"))
        return model

    def _compile_model(self, model: Model):
        """
        Compiles the keras model
        :param model: The model to compile
        :return: None
        """
        def loss(expected, predicted):
            """
            Special loss function that takes goal difference into account
            :param expected: THe expected values
            :param predicted: The predicted values
            :return: The loss function definition
            """
            expected_home = backend.gather(expected, [0])
            expected_away = backend.gather(expected, [1])
            predicted_home = backend.gather(predicted, [0])
            predicted_away = backend.gather(predicted, [1])

            expected_diff = expected_home - expected_away
            predicted_diff = predicted_home - predicted_away
            mse_diff = backend.mean(
                backend.square(predicted_diff - expected_diff))
            mse = backend.mean(backend.square(predicted - expected))

            return mse + backend.sqrt(mse_diff)

        model.compile(loss=loss, optimizer="sgd")

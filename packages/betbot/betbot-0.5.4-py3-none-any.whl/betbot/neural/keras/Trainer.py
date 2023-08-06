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
import random
import logging
from typing import Tuple, List, Optional, Callable
from tensorflow.keras.models import Model


class Trainer:
    """
    Class that models common functions of a neural network trainer
    """

    def __init__(self, model_dir: str):
        """
        Initializes the trainer
        :param model_dir: The directory in which to store models
        """
        self.model_dir = model_dir
        if not os.path.isdir(model_dir):
            os.makedirs(model_dir)
        self.name = self.__class__.__name__
        self.weights_path = os.path.join(model_dir, self.name + ".h5")
        self.logger = logging.getLogger(self.name)

    def load_training_data(self, force_refresh: bool) \
            -> List[Tuple[List[float], List[float]]]:
        """
        Loads data for training the model
        :param force_refresh: Forces a refresh of data
        :return: The training data, with the input and output vectors separate
        """
        raise NotImplementedError()

    def _define_model(self) -> Model:
        """
        Specifies the model of the neural network
        :return: The model
        """
        raise NotImplementedError()

    def _compile_model(self, model: Model):
        """
        Compiles the keras model
        :param model: The model to compile
        :return: None
        """
        raise NotImplementedError()

    def _evaluate(
            self,
            predictions: List[List[float]],
            expected_output: List[List[float]]
    ) -> Tuple[float, float]:
        """
        Evaluates predictions of the neural network
        :param predictions: The predictions to check
        :param expected_output: The expected output for the predictions
        :return: The evaluation score and a percentage of how well the
                 prediction matches the expected output
        """
        raise NotImplementedError()

    def load_trained_model(
            self,
            iterations: int = 4,
            epochs: int = 32,
            batch_size: int = 64,
            force_retrain: bool = False,
            minimum_accuracy: float = 0.0,
            custom_model_fn: Optional[Callable[[], Model]] = None,
            custom_compile_fn: Optional[Callable[[Model], None]] = None
    ) -> Model:
        """
        Generates a trained keras model that can be used to predict output
        immediately
        :param iterations: The amount of iterations to train
        :param epochs: The amount of epochs to train
        :param batch_size: The batch size to use when training
        :param force_retrain: Whether or not to force retraining
        :param minimum_accuracy: Optional value for minimum accuracy
        :param custom_model_fn: Allows using a custom model to be trained
        :param custom_compile_fn: Allows using a custom compile function
        :return: The trained model
        """
        if force_retrain or not os.path.exists(self.weights_path):
            accuracy = -1.0
            model = None
            while accuracy < minimum_accuracy:
                model, _, accuracy, _, _ = self.train(
                    iterations,
                    epochs,
                    batch_size,
                    custom_model_fn,
                    custom_compile_fn
                )
            assert model is not None
        else:
            model = self._define_model()
            model.load_weights(self.weights_path)
        model.save_weights(self.weights_path)
        return model

    def train(
            self,
            iterations: int,
            epochs: int,
            batch_size: int,
            custom_model_fn: Optional[Callable[[], Model]] = None,
            custom_compile_fn: Optional[Callable[[Model], None]] = None
    ) -> Tuple[Model, float, float, float, float]:
        """
        Trains the model using the training data for a specified amount of
        times and returns the best performing model
        Iterations and epochs are different things!
        Each iteration starts from scratch.
        :param iterations: The amount of iterations
        :param epochs: The amount of epochs to train
        :param batch_size: The batch size to use
        :param custom_model_fn: Allows using a custom model to be trained
        :param custom_compile_fn: Allows using a custom compile function
        :return: The best trained model and its score + accuracy
                 as well as average score and accuracy stats
        """
        scores = []
        best_score = [-1.0, -1.0]
        best_model = None
        for i in range(iterations):
            train_in, train_out, valid_in, valid_out, test_in, test_out = \
                self._prepare_training_data()

            if custom_model_fn is None:
                model = self._define_model()
            else:
                model = custom_model_fn()

            if custom_compile_fn is None:
                self._compile_model(model)
            else:
                custom_compile_fn(model)

            self.logger.info(f"Training model {self.name} (Iteration {i})...")
            history = model.fit(
                train_in,
                train_out,
                epochs=epochs,
                batch_size=batch_size,
                validation_data=(valid_in, valid_out),
                verbose=1
            )
            predictions = [
                [float(x) for x in vector]
                for vector in model.predict(test_in).tolist()
            ]
            try:
                score, accuracy = self._evaluate(predictions, test_out)
            except ValueError:
                score, accuracy = 0, 0.0
            scores.append((score, accuracy))

            self.logger.info(f"Finished training: "
                             f"loss={history.history['loss'][0]:.5f}, "
                             f"score={score:.2f}")

            if accuracy > best_score[1]:
                best_score = [score, accuracy]
                best_model = model

        average_score = sum([x[0] for x in scores]) / len(scores)
        average_accuracy = sum([x[1] for x in scores]) / len(scores)
        return best_model, best_score[0], best_score[1],\
            average_score, average_accuracy

    def _prepare_training_data(self) -> Tuple[
        List[List[float]],
        List[List[float]],
        List[List[float]],
        List[List[float]],
        List[List[float]],
        List[List[float]]
    ]:
        """
        Prepares the training data by shuffling the data and splitting
        it up into a training, validation and test set
        :return: The prepared training data
        """
        labelled_data = self.load_training_data(False)
        random.shuffle(labelled_data)
        inputs = [x[0] for x in labelled_data]
        outputs = [x[1] for x in labelled_data]
        divider_1 = int(4 * len(inputs) / 6)
        divider_2 = int(5 * len(inputs) / 6)
        train_in = inputs[0:divider_1]
        train_out = outputs[0:divider_1]
        valid_in = inputs[divider_1:divider_2]
        valid_out = outputs[divider_1:divider_2]
        test_in = inputs[divider_2:]
        test_out = outputs[divider_2:]
        self.logger.debug(f"{len(train_in)} samples of training data")
        self.logger.debug(f"{len(valid_in)} samples of validation data")
        self.logger.debug(f"{len(test_in)} samples of testing data")
        return train_in, train_out, valid_in, valid_out, test_in, test_out

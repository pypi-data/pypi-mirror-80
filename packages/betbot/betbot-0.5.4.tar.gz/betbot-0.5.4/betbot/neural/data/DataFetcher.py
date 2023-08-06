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
import json
import logging
from typing import List, Tuple, Dict, Union
from betbot.neural.data.vector.InputVector import InputVector
from betbot.neural.data.vector.OutputVector import OutputVector
from betbot.neural.data.Match import Match


class DataFetcher:
    """
    Class that specifies common methods used to fetch data
    """

    def __init__(self, no_cache: bool = False):
        """
        Initializes the DataFetcher
        Automatically loads data from the internet if it does not yet exist
        locally.
        :param no_cache: Whether or not to use local data (if it exists)
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        betbot_dir = os.path.join(os.path.expanduser("~"), ".config/betbot")
        data_dir = os.path.join(betbot_dir, "data")
        data_file_name = self.__class__.__name__ + ".json"
        self.data_file = os.path.join(data_dir, data_file_name)

        if not os.path.isdir(data_dir):
            os.makedirs(data_dir)

        if os.path.isfile(self.data_file) and not no_cache:
            with open(self.data_file, "r") as f:
                self.data = json.load(f)
        else:
            self.data = self.load()
            self.save(self.data_file)

    def load(self) -> Dict[str, Dict[int, Dict[int, List[Dict[str, str]]]]]:
        """
        Loads the match data from the internet
        :return: The data as dictionaries representing matches,
                 mapped to their respective countries, leagues and seasons
        """
        raise NotImplementedError()

    def save(self, target_file: str):
        """
        Saves the currently loaded data to a file
        :param target_file: The file to which to save
        :return: None
        """
        with open(target_file, "w") as f:
            json.dump(self.data, f)

    def get_training_data(self) \
            -> List[Tuple[Match, InputVector, OutputVector]]:
        """
        :return: All training data from previous matches
        """
        raise NotImplementedError()

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
        raise NotImplementedError()

    def write_training_vectors_to_csv(self, target: str):
        """
        Writes the training vectors to a CSV file
        :param target: The path to the CSV file
        :return: None
        """
        vectors = self.get_training_data()
        lines = [["match", *InputVector.legend(), *OutputVector.legend()]]
        for match, input_vector, output_vector in vectors:
            identifier = f"{match.country}-{match.league}-{match.season}-" \
                         f"{match.date.strftime('%Y-%m-%d')}-" \
                         f"{match.home_team}-{match.away_team}"
            data = [str(x) for x in input_vector.vector + output_vector.vector]
            lines.append([identifier] + data)
        with open(target, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(lines)

    # noinspection PyMethodMayBeStatic
    def load_training_vectors(self, target: str) \
            -> List[Tuple[List[float], List[float]]]:
        """
        Loads the raw training vectors from a CSV file
        :param target: The target file
        :return: The vectors
        """
        with open(target, "r") as f:
            reader = csv.reader(f)
            data = [x for x in reader]
        data.pop(0)

        vectors = []
        for line in data:
            line.pop(0)
            input_vector = [
                float(x) for x in line[0:len(InputVector.legend())]
            ]
            output_vector = [
                float(x) for x in line[len(InputVector.legend()):]
            ]
            vectors.append((input_vector, output_vector))

        return vectors

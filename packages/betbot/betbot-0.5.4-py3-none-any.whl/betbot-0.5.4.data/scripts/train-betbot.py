#!python
"""LICENSE
Copyright 2017 Hermann Krumrey <hermann@krumreyh.com>

This file is part of bundesliga-tippspiel.

bundesliga-tippspiel is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

bundesliga-tippspiel is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with bundesliga-tippspiel.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

import os
import argparse
import tensorflow
from betbot import sentry_dsn
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from puffotter.init import cli_start, argparse_add_verbosity
from betbot.neural.keras.MatchHistoryTrainer import MatchHistoryTrainer
from betbot.neural.data.vector.OutputVector import OutputVector
from betbot.neural.data.vector.InputVector import InputVector


def main(args: argparse.Namespace):
    """
    Trains the betbot neural networks and evaluates them
    :param args: The command line arguments
    :return: None
    """
    print(tensorflow.executing_eagerly())

    if args.trainer == "match_history":
        trainer = MatchHistoryTrainer(args.output_dir)
    else:
        return

    trainer.name = args.name

    if args.refresh_training_data:
        trainer.load_training_data(True)

    def gen_model(h, o, layers):
        h_size = len(InputVector.legend()) - 10

        h_ls = []
        for i in range(layers):
            h_ls.append(Dense(h_size, activation=h))

        return Sequential([
            Flatten(input_shape=(len(InputVector.legend()),)),
            *h_ls,
            Dense(len(OutputVector.legend()), activation=o)
        ])

    custom_models = [
        (lambda: gen_model("sigmoid", "relu", 1), "sigmoid-relu1"),
        (lambda: gen_model("sigmoid", "linear", 1), "sigmoid-linear1"),
        (lambda: gen_model("sigmoid", "exponential", 1),
         "sigmoid-exponential1"),
        (lambda: gen_model("linear", "linear", 1), "linear-linear1"),
        (lambda: gen_model("relu", "relu", 1), "relu-relu1"),
        (lambda: gen_model("relu", "exponential", 1), "relu-exponential1"),
        (lambda: gen_model("exponential", "exponential", 1), "expo-expo1"),
        (lambda: gen_model("sigmoid", "relu", 2), "sigmoid-relu2"),
        (lambda: gen_model("sigmoid", "linear", 2), "sigmoid-linear2"),
        (lambda: gen_model("sigmoid", "exponential", 2),
         "sigmoid-exponential2"),
        (lambda: gen_model("linear", "linear", 2), "linear-linear2"),
        (lambda: gen_model("relu", "relu", 2), "relu-relu2"),
        (lambda: gen_model("relu", "exponential", 2), "relu-exponential2"),
        (lambda: gen_model("exponential", "exponential", 2), "expo-expo2")
    ]
    custom_compilations = [
        (lambda m: m.compile(loss="mae", optimizer="sgd"), "mae-sgd"),
        (lambda m: m.compile(loss="mae", optimizer="adamax"), "mae-adamax"),
        (lambda m: m.compile(loss="mae", optimizer="nadam"), "mae-nadam"),
        (lambda m: m.compile(loss="mse", optimizer="sgd"), "mse-sgd"),
        (lambda m: m.compile(loss="mse", optimizer="adamax"), "mse-adamax"),
        (lambda m: m.compile(loss="mse", optimizer="nadam"), "mse-nadam")
    ]
    if not args.try_parameters:
        custom_models = [(None, "default")]
        custom_compilations = custom_models

    existing = [x.split("]")[-1].strip() for x in os.listdir(args.output_dir)]

    for custom_model in custom_models:
        for custom_compilation in custom_compilations:
            name = f"{args.name}-{custom_model[1]}-{custom_compilation[1]}"

            if name in existing:
                print(f"{name} exists, skipping")
                continue

            trainer.name = name
            try:
                model, score, accuracy, avg_score, avg_acc = trainer.train(
                    args.iterations,
                    args.epochs,
                    args.batch_size,
                    custom_model_fn=custom_model[0],
                    custom_compile_fn=custom_compilation[0]
                )
            except ValueError as e:
                print(f"Failed to train {name}")
                continue
            print(f"Best Score: {score}, "
                  f"Best Accuracy: {accuracy:.2f}%")
            print(f"Average Score: {avg_score}, "
                  f"Average Accuracy: {avg_acc:.2f}%")
            name = f"[{avg_score:.2f}][{score:.2f}] {name}"
            model.save(os.path.join(args.output_dir, name))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir")
    parser.add_argument("name")
    parser.add_argument("trainer", choices={"match_history"})
    parser.add_argument("--iterations", type=int, default=3)
    parser.add_argument("--epochs", type=int, default=32)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--refresh-training-data", action="store_true")
    parser.add_argument("--try-parameters", action="store_true")
    argparse_add_verbosity(parser)
    cli_start(main, parser, "Thanks for using betbot", "betbot", sentry_dsn)

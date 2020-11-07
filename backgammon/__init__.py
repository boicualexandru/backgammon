# Copyright 2020 Softwerks LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import enum
from typing import List, Tuple

from backgammon import position

STARTING_POSITION_ID = "4HPwATDgc/ABMA"

POINTS = 24
POINTS_PER_QUADRANT = int(POINTS / 4)

ASCII_BOARD_HEIGHT = 11
ASCII_MAX_CHECKERS = 5
ASCII_13_24 = "+13-14-15-16-17-18------19-20-21-22-23-24-+"
ASCII_12_01 = "+12-11-10--9--8--7-------6--5--4--3--2--1-+"


@enum.unique
class Player(enum.IntEnum):
    ZERO = 0
    ONE = 1


@enum.unique
class Position(enum.IntEnum):
    OPPONENT_BAR = 0
    BOARD_POINTS_START = 1
    BOARD_POINTS_END = 24
    PLAYER_BAR = 25
    PLAYER_HOME = 26
    OPPONENT_HOME = 27


class Backgammon:
    def __init__(self, position_id: str = STARTING_POSITION_ID):
        position_key: str = position.decode(position_id)
        self.position: List[int] = position.position_from_key(position_key)
        self.player: Player = Player.ZERO

    def __repr__(self):
        position_id: str = position.encode(position.key_from_position(self.position))
        return f"{__name__}.{self.__class__.__name__}('{position_id}')"

    def __str__(self):
        def checkers(top: List[int], bottom: List[int]) -> List[List[str]]:
            """Return an ASCII checker matrix."""
            ascii_checkers: List[List[str]] = [
                ["   " for j in range(len(top))] for i in range(ASCII_BOARD_HEIGHT)
            ]

            for half in (top, bottom):
                for col, num_checkers in enumerate(half):
                    row: int = 0 if half is top else len(ascii_checkers) - 1
                    for i in range(abs(num_checkers)):
                        if (
                            abs(num_checkers) > ASCII_MAX_CHECKERS
                            and i == ASCII_MAX_CHECKERS - 1
                        ):
                            ascii_checkers[row][col] = f" {abs(num_checkers)} "
                            break
                        ascii_checkers[row][col] = " O " if num_checkers > 0 else " X "
                        row += 1 if half is top else -1

            return ascii_checkers

        def split(position: List[int]) -> Tuple[List[int], List[int]]:
            """Return a position split into top (Player.ZERO 12-1) and bottom (Player.ZERO 13-24) halves."""

            def normalize(position: List[int]) -> List[int]:
                """Return position for Player.ZERO"""
                if self.player is Player.ONE:
                    position = list(map(lambda n: -n, position[::-1]))
                return position

            position = normalize(position)

            half_len: int = int(len(position) / 2)
            top: List[int] = position[:half_len][::-1]
            bottom: List[int] = position[half_len:]

            return top, bottom

        points: List[List[str]] = checkers(
            *split(
                self.position[
                    Position.BOARD_POINTS_START : Position.BOARD_POINTS_END + 1
                ]
            )
        )

        bar: List[List[str]] = checkers(
            *split(
                [
                    self.position[Position.PLAYER_BAR],
                    self.position[Position.OPPONENT_BAR],
                ]
            )
        )

        ascii_board: str = ""
        position_id: str = position.encode(position.key_from_position(self.position))
        ascii_board += f"Position ID: {position_id}\n"
        ascii_board += (
            " " + (ASCII_12_01 if self.player is Player.ZERO else ASCII_13_24) + "\n"
        )
        for i in range(len(points)):
            ascii_board += (
                ("^|" if self.player == 0 else "v|")
                if i == int(ASCII_BOARD_HEIGHT / 2)
                else " |"
            )
            ascii_board += "".join(points[i][:POINTS_PER_QUADRANT])
            ascii_board += "|"
            ascii_board += "BAR" if i == int(ASCII_BOARD_HEIGHT / 2) else bar[i][0]
            ascii_board += "|"
            ascii_board += "".join(points[i][POINTS_PER_QUADRANT:])
            ascii_board += "|"
            ascii_board += "\n"
        ascii_board += (
            " " + (ASCII_13_24 if self.player is Player.ZERO else ASCII_12_01) + "\n"
        )

        return ascii_board

from enum import Enum


class GameResult(Enum):
    WIN = 1
    LOSE = 2
    LOSE_FREEBET = 3


class TeamType(Enum):
    UNDERDOG = 1
    OVERDOG = 2

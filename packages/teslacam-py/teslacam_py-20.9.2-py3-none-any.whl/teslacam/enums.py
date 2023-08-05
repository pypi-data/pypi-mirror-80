from enum import Enum

class ClipType(Enum):
    RECENT = 1
    SAVED = 2
    SENTRY = 3

class Camera(Enum):
    FRONT = 1
    LEFT_REPEATER = 2
    RIGHT_REPEATER = 3
    BACK = 4
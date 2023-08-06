import enum

class ColourSpace(enum.Enum):
    RGB = enum.auto()
    LAB = enum.auto()
    HSV = enum.auto()

    @staticmethod
    def from_str(colour_space: str) -> 'ColourSpace':
        return getattr(ColourSpace, colour_space.upper())

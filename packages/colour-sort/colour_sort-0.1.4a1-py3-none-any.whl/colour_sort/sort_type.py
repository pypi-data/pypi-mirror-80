import enum

class SortType(enum.Enum):
    BRIGHTNESS = enum.auto()
    AVG        = enum.auto()

    # Shift modes
    ABC        = enum.auto()
    ACB        = enum.auto()
    BAC        = enum.auto()
    BCA        = enum.auto()
    CAB        = enum.auto()
    CBA        = enum.auto()

    # Shift modes with clipping
    ABCC       = enum.auto()
    ACBC       = enum.auto()
    BACC       = enum.auto()
    BCAC       = enum.auto()
    CABC       = enum.auto()
    CBAC       = enum.auto()

    # Space fillinig curve approach
    ZORDER     = enum.auto()
    # HILBERT    = enum.auto()

    # PCA
    PCA        = enum.auto()

    @staticmethod
    def from_str(sort_type: str) -> 'SortType':
        return getattr(SortType, sort_type.upper())

    def is_clip(self):
        return False
        # return self in [
        #     SortType.ABCC,
        #     SortType.ACBC,
        #     SortType.BACC,
        #     SortType.BCAC,
        #     SortType.CABC,
        #     SortType.CBAC,
        # ]

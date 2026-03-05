class ParkError(Exception):
    pass


class VisitorNotFoundError(ParkError):
    pass


class AttractionNotFoundError(ParkError):
    pass


class QueueEmptyError(ParkError):
    pass
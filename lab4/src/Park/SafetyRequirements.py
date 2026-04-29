class SafetyRequirements:
    def __init__(self) -> None:
        self._pass = False

    @property
    def is_pass(self) -> bool:
        return self._pass

    def recheck(self, status: bool) -> None:
        self._pass = bool(status)
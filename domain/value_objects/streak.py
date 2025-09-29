class Streak:
    def __init__(self, value: int = 0):
        if not isinstance(value, int):
            raise TypeError(f"Streak must be int, got {type(value).__name__}")
        if value < 0:
            raise ValueError("Streak cannot be negative")

        self._value = value

    @property
    def value(self) -> int:
        return self._value

    def increase(self) -> 'Streak':
        """Devuelve una nueva instancia con la racha incrementada en 1."""
        return Streak(self._value + 1)

    def reset(self) -> 'Streak':
        """Devuelve una nueva instancia con la racha en 0."""
        return Streak(0)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Streak):
            return False
        return self._value == other._value

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return f"Streak({self._value})"

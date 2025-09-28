class Frequency:
    DAYS = ["lunes", "martes", "miercoles", "jueves", "viernes",
            "sabado", "domingo"]

    def __init__(self, days=None):
        self.days = [0] * 7 if days is None else days

    @property
    def value(self):
        return self.days

    def set_day(self, day):
        if isinstance(day, int):  # Si pasa un número (0-6)
            if day < 0 or day > 6:
                error_msg = "El día debe estar entre 0 (lunes) y 6 (domingo)"
                raise ValueError(error_msg)
            self.days[day] = 1
        elif isinstance(day, str):  # Si pasa un nombre
            if day.lower() not in self.DAYS:
                error_msg = f"Invalid day '{day}', must be one of {self.DAYS}"
                raise ValueError(error_msg)
            index = self.DAYS.index(day.lower())
            self.days[index] = 1
        else:
            raise TypeError("El día debe ser int o str")

    def is_active(self, day):
        if isinstance(day, int):
            if day < 0 or day > 6:
                error_msg = "El día debe estar entre 0 (lunes) y 6 (domingo)"
                raise ValueError(error_msg)
            return self.days[day] == 1
        elif isinstance(day, str):
            if day.lower() not in self.DAYS:
                error_msg = f"Invalid day '{day}', must be one of {self.DAYS}"
                raise ValueError(error_msg)
            index = self.DAYS.index(day.lower())
            return self.days[index] == 1
        else:
            raise TypeError("El día debe ser int o str")

    def __str__(self):
        return str(self.days)

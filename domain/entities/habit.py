from domain.value_objects.name import Name
from domain.value_objects.streak import Streak
from domain.value_objects.frequency import Frequency
from domain.value_objects.description import Description
from domain.utils.checks import check_type


class Habit:
    def __init__(self,
                 habit_id: int,
                 name: Name,
                 description: Description, *,
                 is_completed: bool = False,
                 frequency: Frequency = Frequency(),
                 streak: Streak = Streak(0)):

        check_type("habit_id", habit_id, int)
        if habit_id < 0:
            raise TypeError("habit_id must be greater than zero")

        check_type("name", name, Name)
        check_type("description", description, Description)
        check_type("frequency", frequency, Frequency)
        check_type("streak", streak, Streak)

        self.habit_id = habit_id
        self.name = name
        self.description = description
        self.frequency = frequency
        self.is_completed = is_completed
        self.streak = streak

    def __eq__(self, other: 'Habit') -> bool:
        return self.habit_id == other.habit_id or self.name == other.name

    def complete(self):
        """Marca el hábito como completado y aumenta la racha."""
        self.is_completed = True
        self.streak = self.streak.increase()

    def fail(self):
        """Resetea la racha si el hábito no se cumplió."""
        self.is_completed = False
        self.streak = self.streak.reset()

    def __str__(self):
        string = f"id:{self.habit_id}"
        string += f", name:{self.name}"
        string += f", description:{self.description}"
        string += f", frequency:{self.frequency}"
        string += f", is_completed:{self.is_completed}"
        string += f", streak:{self.streak}"
        return string

    def copy(self):
        copy = Habit(self.habit_id,
                     self.name,
                     self.description,
                     is_completed=self.is_completed,
                     frequency=self.frequency,
                     streak=self.streak)
        return copy

    def modify(self, name=None, description=None, frequency=None,
               is_completed=None, streak=None):
        if name:
            check_type("name", name, Name)
            self.name = name
        if description:
            check_type("description", description, Description)
            self.description = description
        if frequency:
            check_type("frequency", frequency, Frequency)
            self.frequency = frequency

        if is_completed is not None:
            check_type("is_completed", is_completed, bool)
            self.is_completed = is_completed

        if streak is not None:
            check_type("streak", streak, Streak)
            self.streak = streak

from domain.value_objects.name import Name
from domain.value_objects.description import Description


class Habit:
    def __init__(self, habit_id, name, description, frequency):
        if not isinstance(name, Name):
            error_msg = f"name must be of type Name, got {type(name).__name__}"
            raise TypeError(error_msg)
        if not isinstance(description, Description):
            error_msg = "description must be of type Description"
            error_msg += f", got {type(description).__name__}"
            raise TypeError(error_msg)

        self.habit_id = habit_id
        self.name = name
        self.description = description
        self.frequency = frequency
        self.is_completed = False
        self.streak = 0

    def __eq__(self, other: 'Habit') -> bool:
        return self.habit_id == other.habit_id or self.name == other.name

    def __str__(self):
        string = f"id:{self.habit_id}"
        string += f", name:{self.name}"
        string += f", description:{self.description}"
        string += f", frequency:{self.frequency}"
        string += f", is_completed:{self.is_completed}"
        string += f", streak:{self.streak}"
        return string

    def copy(self):
        copy = Habit(self.habit_id, self.name,
                     self.description, self.frequency)
        copy.is_completed = self.is_completed
        copy.streak = self.streak
        return copy

    def modify(self, name=None, description=None, frequency=None,
               is_completed=None, streak=None):
        if name:
            if not isinstance(name, Name):
                raise TypeError("name must be Name")
            self.name = name
        if description:
            if not isinstance(description, Description):
                raise TypeError("description must be Description")
            self.description = description
        if frequency:
            if not isinstance(frequency, list):
                raise ValueError("Invalid frequency")
            self.frequency = frequency

        if is_completed is not None:
            if not isinstance(is_completed, bool):
                raise TypeError("is_completed must be a boolean")
            self.is_completed = is_completed
            
        if streak is not None:
            if not isinstance(streak, int):
                raise TypeError("streak must be a int")
            self.streak = streak

import datetime


from domain.entities.habit import Habit
from domain.value_objects.name import Name
from domain.value_objects.streak import Streak
from domain.value_objects.frequency import Frequency
from domain.value_objects.description import Description
import json


class HabitDto:
    @classmethod
    def infraestructure_to_domain(cls, habit: tuple) -> Habit:
        habit_id, name, description, frequency, is_completed, streak = habit
        name = Name(name)
        description = Description(description)
        frequency = Frequency(json.loads(frequency))
        is_completed = is_completed == 1
        streak = Streak(streak)
        return Habit(name,
                     description,
                     frequency=frequency,
                     is_completed=is_completed,
                     streak=streak,
                     habit_id=habit_id)

    @classmethod
    def domain_to_infraestructure(cls, habit: Habit) -> tuple:
        return (
                habit.habit_id,
                habit.name.value,
                habit.description.value,
                json.dumps(habit.frequency.value),
                1 if habit.is_completed else 0,
                habit.streak.value
               )

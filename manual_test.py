# manual_test.py (recomendado)
from domain.entities.habit import Habit
from domain.value_objects.name import Name
from domain.value_objects.description import Description
from domain.value_objects.frequency import Frequency

def manual_test():
    name = Name("Leer un libro")
    desc = Description("Leer al menos 10 páginas al día")
    frequency = Frequency()
    frequency.set_day("lunes"); frequency.set_day("martes"); frequency.set_day("jueves")

    habit = Habit(1, name, desc, frequency)   # habit.streak se crea internamente como Streak(0)
    print("Habit inicial:", habit)

    habit.complete()
    print("Después de complete():", habit.streak)   # -> Streak(1)

    habit.complete()
    print("Después de otro complete():", habit.streak)   # -> Streak(2)

    habit.fail()
    print("Después de fail():", habit.streak)   # -> Streak(0)

    # Verificamos frecuencia
    print("¿El hábito se hace el lunes?", frequency.is_active("lunes"))   # True
    print("¿El hábito se hace el miércoles?", frequency.is_active("miercoles"))  # False


if __name__ == "__main__":
    manual_test()
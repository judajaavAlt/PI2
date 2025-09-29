from domain.repositories.habit_repository import HabitRepository


class HabitProgress:
    def __init__(self, repository: HabitRepository) -> None:
        self.repository = repository

    def daily_progress(self):
        pass

    def detailed_progress(self):
        pass

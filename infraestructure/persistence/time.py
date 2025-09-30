from datetime import datetime


class TimeManager:
    @classmethod
    def now(cls) -> str:
        """
        Returns current local time formatted for SQLite.
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def today(cls) -> str:
        """
        Returns the current day of the week (e.g., 'Monday').
        """
        return datetime.now().strftime("%A").lower()

    @classmethod
    def days_distance(cls, t1: str, t2: str) -> int:
        """
        Returns the difference in whole days between two 'now()' results.
        Example: today=0, yesterday=1, etc.
        """
        fmt = "%Y-%m-%d %H:%M:%S"
        d1 = datetime.strptime(t1, fmt).date()
        d2 = datetime.strptime(t2, fmt).date()
        return abs((d2 - d1).days)

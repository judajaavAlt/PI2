from datetime import datetime


class TimeManager:
    @classmethod
    def now(cls) -> str:
        """
        Returns current local time formatted for SQLite.
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

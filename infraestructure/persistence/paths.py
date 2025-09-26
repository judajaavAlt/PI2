import os
import platform


class paths:
    @classmethod
    def get_data_dir(cls):
        system = platform.system()
        if system == 'Windows':
            base = os.getenv("APPDATA", "")
        path = os.path.join(base, "HabitApp")
        os.makedirs(path, exist_ok=True)
        return path

    @classmethod
    def get_db_path(cls):
        return os.path.join(cls.get_data_dir(), 'database.sqlite')

    @classmethod
    def get_user_data_path(cls):
        return os.path.join(cls.get_data_dir(), 'userPreferences.json')
    
    
import os
import platform


class paths:
    @classmethod
    def get_data_dir(cls):
        system = platform.system()
        if system == 'Windows':
            base = os.getenv("APPDATA", "")
        elif system == 'Darwin':  # macOS
            base = os.getenv("HOME", "")
        elif system == 'Linux':
            alt = os.path.join(os.getenv("HOME", ""), ".local", "share")
            base = os.getenv("XDG_DATA_HOME", alt)
        else:
            raise NotImplementedError(f"Unsupported OS: {system}")

        path = os.path.join(base, "HabitApp")
        os.makedirs(path, exist_ok=True)
        return path

    @classmethod
    def get_db_path(cls):
        return os.path.join(cls.get_data_dir(), 'database.sqlite')

    @classmethod
    def get_user_data_path(cls):
        return os.path.join(cls.get_data_dir(), 'userPreferences.json')
    
    
import json
import os

# Save the user preferences
class Preferences:

    FILE_PATH = "UserPreferences.json"
    
    hour_formats = {
        "12h": "%I %p",
        "24h": "%H:%M",
        "with_seconds": "%H:%M:%S"
    }

    def __init__(self):
        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "r") as f:
                self.preferences_data = json.load(f)

        else:
            self.preferences_data = {
                "username" : " ",
                "hour_format" : self.hour_formats["12h"]} 
            self.save_to_file()
        
    def update_preferences(self,new_username=None,new_hour_format=None):
        if new_username is not None:
            self.__class__.preferences_data["username"] = new_username
        if new_hour_format in self.hour_formats:
            self.__class__.preferences_data["hour_format"] = self.hour_formats["new_hour_format"]
        self.save_to_file()

    def save_to_file(self):
        with open(self.FILE_PATH,"w") as f:
            json.dump(self.preferences_data,f,indent=4)

    def get_preferences(self):
       return self.preferences_data
    
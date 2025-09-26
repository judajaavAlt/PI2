import json
import datetime

# Save the user preferences
class Preferences:
    # Initial preferences for the app, this includes username and hour_format (12-hour with AM or PM)
    preferences_data = {
       "username" : " ",
        "hour_format" : "%I %p",
    } 

    def __init__(self):
        pass
        
    def update_preferences(self,new_name=None,new_hour_format=None):
        if new_name is not None:
            self.__class__.preferences_data["username"] = new_name
        if new_hour_format is not None:
            self.__class__.preferences_data["edad"] = new_hour_format

    def get_preferences(self):
       return self.preferences_data
    
import json
import datetime

# Save the user preferences
class Preferences:
    
    hour_formats = {
        "12h": "%I %p",
        "24h": "%H:%M",
        "with_seconds": "%H:%M:%S"
    }

    def __init__(self):
        self.preferences_data = {
            "username" : " ",
            "hour_format" : self.hour_formats["12h"]} 
        
    def update_preferences(self,new_username=None,new_hour_format=None):
        if new_username is not None:
            self.__class__.preferences_data["username"] = new_username
        if new_hour_format in self.hour_formats:
            self.__class__.preferences_data["hour_format"] = self.hour_formats["new_hour_format"]

    def get_preferences(self):
       return self.preferences_data
    
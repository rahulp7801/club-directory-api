import pandas as pd
import constants
import json
from jsonschema import validate, ValidationError


# Class Name: String
# Grades: String (Will convert to list)
# Weighted: Boolean
# 3rd Year Science: Boolean
# UC A-G: String
# PreRequisite: String
# Code: String
# Rigor: float
# Homework: int
class VistaClub:
    def __init__(self, name, description, president, vp, treasurer, secretary, webmaster, historian, image, tags, advisor, times, room, video) -> None:
        self.name = name
        self.description = description
        self.president = president.split(", ")
        self.vp = vp.split(", ")
        self.treasurer = treasurer.split(", ")
        self.secretary = secretary.split(", ")
        self.webmaster = webmaster.split(", ")
        self.historian = historian.split(", ")
        self.image = image
        self.tags = tags.split(", ")
        self.advisor = advisor
        self.times = times
        self.room = room
        self.video = video

    def get_name(self) -> str:
        return self.name
    
    def get_desc(self) -> str:
        return self.description
    
    def get_president(self) -> list:
        return self.president
    
    def get_vp(self) -> list:
        return self.vp

    def get_historian(self) -> list:
        return self.historian
    
    def get_treasurer(self) -> list:
        return self.treasurer
    
    def get_secretary(self) -> list:
        return self.secretary
    
    def get_webmaster(self) -> list:
        return self.webmaster
    
    def get_club_image(self) -> str:
        return self.image

    def get_club_tags(self) -> list:
        return self.tags
    
    def get_club_advisor(self) -> str:
        return self.advisor
    
    def get_meeting_times(self) -> str:
        return self.times
    
    def get_meeting_room(self) -> str:
        return self.room

    def get_club_video(self) -> str:
        return self.video


    # Populate grade list given a range from the table
    def _convert_grades_list(self, grades):
        try:
            newgrades = (grades.split("-"))
            if (len(newgrades) > 1):
                newgrades = self.fill_nums(int(newgrades[0]), int(newgrades[1]))
            else:
                newgrades = [int(newgrades[0])]
        except AttributeError: # we have passed in an already formatted list for grades, pass
            newgrades = grades
        return newgrades
        
    
    @staticmethod
    def fill_nums(lower, upper):
        return list(range(lower, upper + 1))

class VistaClubHelper:

    @staticmethod
    def convert_data(data):    
        vista_class_list = []

        for i in data:
            vista_class_list.append(VistaClub(i['Club Name'], i['Club Description'], i['President'], i['Vice President'], i['Treasurer'], i['Secretary'], i['Webmaster'], i['Historian'], i['Image'], i['Tags'], i['Advisor'], i['Meeting Times'], i['Meeting Room'], i["Club Video"]))

        return vista_class_list

    @staticmethod
    def convert_to_df(data):
        new_list = []
        for i in data:
            new_list.append({"Club Name": i.get_name(), "Club Description": i.get_desc(), "President": i.get_president(), "Vice President": i.get_vp(), "Treasurer": i.get_treasurer(), "Secretary": i.get_secretary(), "Webmaster": i.get_webmaster(), "Historian": i.get_historian(), "Image": i.get_club_image(), "Tags": i.get_club_tags(), "Advisor": i.get_club_advisor(), "Meeting Times": i.get_meeting_times(), "Meeting Room": i.get_meeting_room(), "Club Video": i.get_club_video()})
        
        df = pd.DataFrame(new_list)
        return df

    @staticmethod
    def convert_to_dictlist(data):
        new_list = []
        count = 1
        for i in data:
            new_list.append({"id": count, "Club Name": i.get_name(), "Club Description": i.get_desc(), "President": i.get_president(), "Vice President": i.get_vp(), "Treasurer": i.get_treasurer(), "Secretary": i.get_secretary(), "Webmaster": i.get_webmaster(), "Historian": i.get_historian(), "Image": i.get_club_image(), "Tags": i.get_club_tags(), "Advisor": i.get_club_advisor(), "Meeting Times": i.get_meeting_times(), "Meeting Room": i.get_meeting_room(), "Club Video": i.get_club_video()})
            count +=1
        return new_list
    
    
    schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "number"},
        "grades": {"type": "number"},
    },
    "required": ["name", "age"]
    }

class VistaClubLookup:

    def __init__(self, df=None):
        if df is None:
            # Read from CSV if no DataFrame is provided
            self.df = pd.read_csv(constants.CLUB_SHEET_URL)
            print(self.df)
        else:
            # Use the provided DataFrame
            self.df = df

        self.easy_df = VistaClubHelper.convert_data(self.df.to_dict(orient="records"))

    def print_db(self):
        print(self.df)

    def print_dict(self):
        print(self.easy_df)

    def get_json_string(self):
        return json.dumps(VistaClubHelper.convert_to_dictlist(self.easy_df))

    # Returns a list of VistaClass Objects
    def get_classes_by_category(self, category:str):
        filtered_df = self.df[self.df["Category Code"] == category.lower().strip()]
        return VistaClubHelper.convert_data(filtered_df.to_dict(orient="records"))
    
    def get_classes_by_weight(self, is_weighted:bool):
        filtered_df = self.df[self.df["Weighted"] == is_weighted]
        return VistaClubHelper.convert_data(filtered_df.to_dict(orient="records"))
    
    # Returns all classes a grade can take
    def get_classes_by_grade(self, grade:int):
        class_list = []
        for i in self.easy_df:
            if grade in i.get_grades():
                class_list.append(i)
        return class_list
    
    def get_classes_by_ucreq(self, req:str):
        filtered_df = self.df[self.df["UC a-g approved course"] == req.lower().strip()]
        return VistaClubHelper.convert_data(filtered_df.to_dict(orient="records"))
    
    def sort_classes_by_rigor(self, asc=True):
        sorted_df = self.df.sort_values(by="Rigor", ascending=asc)
        return VistaClubHelper.convert_data(sorted_df.to_dict(orient='records'))

    def sort_classes_by_hw(self, asc=True):
        sorted_df = self.df.sort_values(by="Homework", ascending=asc)
        return VistaClubHelper.convert_data(sorted_df.to_dict(orient='records'))


clown = VistaClubLookup()
print(clown.get_json_string())







import pandas as pd
import constants

# Class Name: String
# Grades: String (Will convert to list)
# Weighted: Boolean
# 3rd Year Science: Boolean
# UC A-G: String
# PreRequisite: String
# Code: String
# Rigor: float
# Homework: int
class VistaClass:
    def __init__(self, name, grades, is_weighted, is_three_year, ucag, prereq, code, rigor, homework) -> None:
        self.name = name
        self.grades = self._convert_grades_list(grades)
        self.is_weighted = is_weighted
        self.is_three_year = is_three_year
        self.ucag = ucag
        self.prereq = prereq
        self.code = code
        self.rigor = rigor
        self.hw = homework

    def get_name(self) -> str:
        return self.name
    
    def get_grades(self) -> list:
        return self.grades
    
    def get_prerequisites(self) -> str:
        return self.prereq
    
    def get_ucreq(self) -> str:
        return self.ucag
    
    def get_third_year_req(self) -> bool:
        return self.is_three_year
    
    def get_is_weighted(self) -> bool:
        return self.is_weighted
    
    def get_class_code(self) -> str:
        return self.code
    
    def get_rigor(self) -> float:
        return self.rigor

    def get_hw_time(self) -> int:
        return self.hw


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

class VistaClassHelper:

    @staticmethod
    def convert_data(data):    
        vista_class_list = []

        for i in data:
            vista_class_list.append(VistaClass(i['Course Name'], i['Grade Levels'], i['Weighted'], i['3rd Year Science'], i['UC a-g approved course'], i['Prerequisite'], i['Category Code'], i['Rigor'], i['Homework']))

        return vista_class_list

    @staticmethod
    def convert_to_df(data):
        new_list = []
        for i in data:
            new_list.append({"Course Name": i.get_name(), "Grade Levels": i.get_grades(), "Weighted": i.get_is_weighted(), "3rd Year Science": i.get_third_year_req(), "UC a-g approved course": i.get_ucreq(), "Prerequisite": i.get_prerequisites(), "Category Code": i.get_class_code(), "Rigor": i.get_rigor(), "Homework": i.get_hw_time()})
        
        df = pd.DataFrame(new_list)
        return df

class VistaClassLookup:

    def __init__(self, df=None):
        if df is None:
            # Read from CSV if no DataFrame is provided
            self.df = pd.read_csv(constants.SHEET_URL)
        else:
            # Use the provided DataFrame
            self.df = df

        self.easy_df = VistaClassHelper.convert_data(self.df.to_dict(orient="records"))

    def print_db(self):
        print(self.df)

    def print_dict(self):
        print(self.easy_df)

    # Returns a list of VistaClass Objects
    def get_classes_by_category(self, category:str):
        filtered_df = self.df[self.df["Category Code"] == category.lower().strip()]
        return VistaClassHelper.convert_data(filtered_df.to_dict(orient="records"))
    
    def get_classes_by_weight(self, is_weighted:bool):
        filtered_df = self.df[self.df["Weighted"] == is_weighted]
        return VistaClassHelper.convert_data(filtered_df.to_dict(orient="records"))
    
    # Returns all classes a grade can take
    def get_classes_by_grade(self, grade:int):
        class_list = []
        for i in self.easy_df:
            if grade in i.get_grades():
                class_list.append(i)
        return class_list
    
    def get_classes_by_ucreq(self, req:str):
        filtered_df = self.df[self.df["UC a-g approved course"] == req.lower().strip()]
        return VistaClassHelper.convert_data(filtered_df.to_dict(orient="records"))
    
    def sort_classes_by_rigor(self, asc=True):
        sorted_df = self.df.sort_values(by="Rigor", ascending=asc)
        return VistaClassHelper.convert_data(sorted_df.to_dict(orient='records'))

    def sort_classes_by_hw(self, asc=True):
        sorted_df = self.df.sort_values(by="Homework", ascending=asc)
        return VistaClassHelper.convert_data(sorted_df.to_dict(orient='records'))


clown = VistaClassLookup()
gang = (clown.get_classes_by_grade(9))
slime = VistaClassLookup(VistaClassHelper.convert_to_df(gang))
for i in slime.sort_classes_by_rigor(False):
    print(f"Name: {i.get_name()}, Rigor: {i.get_rigor()}")






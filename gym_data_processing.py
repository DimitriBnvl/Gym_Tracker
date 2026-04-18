import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class GymDataProcessing:
    def __init__(self, query, weight, height, age, gender):
        #-----------------Post Exercise-----------------#
        self.exercise_url      = "https://app.100daysofpython.dev"
        self.exercise_post_url = f"{self.exercise_url}/v1/nutrition/natural/exercise"

        self.exercise_params = {
            "query"    : query,
            "weight_kg": weight,
            "heigh_cm" : height,
            "age"      : age,
            "gender"   : gender,
        }

        self.exercise_headers = {
            "Content-Type": "application/json",
            "x-app-id"    : os.environ.get("EXERCISE_API_APP_ID"),
            "x-app-key"   : os.environ.get("EXERCISE_API_KEY"),
        }

        #-----------------Post in Sheets-----------------#
        self.sheety_post_url   = f"https://api.sheety.co/12b1cd54a019188aeb95639019259c73/workoutTracker/workouts"

        self.date_now = datetime.today().strftime('%d/%m/%Y')
        self.time_now = datetime.today().strftime("%H:%M:%S")


        self.sheets_headers = {
            "Content-Type": "application/json",
            "Authorization": os.environ.get("SHEETY_API_KEY"),
        }

        exercises_list = self.post_exercise()

        for exercise in exercises_list:
            self.exercise_name = exercise["name"]
            self.exercise_duration = exercise["duration_min"]
            self.exercise_calories = exercise["nf_calories"]

        self.sheets_params = {
            "workout": {
                "date": self.date_now,
                "time": self.time_now,
                "exercise": self.exercise_name.title(),
                "duration": self.exercise_duration,
                "calories": self.exercise_calories,
            }
        }

    def post_exercise(self):
        exercise_data = requests.post(url=self.exercise_post_url, json=self.exercise_params, headers=self.exercise_headers)
        exercise_data.raise_for_status()
        exercises = exercise_data.json()
        return exercises["exercises"]

    def post_in_sheet(self):
            sheet_data = requests.post(url=self.sheety_post_url, json=self.sheets_params, headers=self.sheets_headers)
            sheet_data.raise_for_status()
            print(sheet_data.status_code)

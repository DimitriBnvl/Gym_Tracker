import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class GymDataProcessing:
    def __init__(self, query, weight, height, age, gender):
        self.exercise_url      = "https://app.100daysofpython.dev"
        self.exercise_post_url = f"{self.exercise_url}/v1/nutrition/natural/exercise"
        self.sheety_post_url   = f"https://api.sheety.co/12b1cd54a019188aeb95639019259c73/workoutTracker/workouts"

        self.exercise_params = {
            "query"    : query,
            "weight_kg": weight,
            "heigh_cm" : height,
            "age"      : age,
            "gender"   : gender,
        }

        self.headers = {
            "Content-Type": "application/json",
            "x-app-id"    : os.environ.get("EXERCISE_API_APP_ID"),
            "x-app-key"   : os.environ.get("EXERCISE_API_KEY"),
        }

        self.query_guidelines = """
        Welcome to Gym Track! To log your exercise, please use the following convention:
            * Include a time frame (in minutes or hours).
            * Include one of the following activities:
                - Running/Jogging - "ran for 30 minutes", "jogged 2 kilometers"
                - Swimming - "swam for 1 hour", "swimming laps"
                - Walking - "walked 3 km", "brisk walk 45 min"
                - Cycling - "biked for 1 hour", "rode bike 10 km"
                - Weightlifting - "lifted weights 45 min", "weight training"
        """

    def post_exercise(self):
        exercise_data = requests.post(url=self.exercise_post_url, json=self.exercise_params, headers=self.headers)
        exercise_data.raise_for_status()
        exercises = exercise_data.json()
        return exercises["exercises"]

    def post_in_sheet(self):
        exercises_list = self.post_exercise()

        date_now = datetime.today().strftime('%d/%m/%Y')
        time_now = datetime.today().strftime("%H:%M:%S")

        for exercise in exercises_list:
            exercise_name = exercise["name"]
            exercise_duration = exercise["duration_min"]
            exercise_calories = exercise["nf_calories"]

            sheets_params = {
                "workout": {
                    "date": date_now,
                    "time": time_now,
                    "exercise": exercise_name.title(),
                    "duration": exercise_duration,
                    "calories": exercise_calories,
                }
            }

            sheet_data = requests.post(url=self.sheety_post_url, json=sheets_params)
            sheet_data.raise_for_status()

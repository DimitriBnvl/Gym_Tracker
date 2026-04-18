import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class GymDataProcessing:
    """
    Tracks workout data by fetching exercise metrics from the Nutritionix API
    and logging each exercise as a row in a Google Sheet via Sheety.

    Credentials are read from environment variables at instantiation time:
        - EXERCISE_API_APP_ID  : Nutritionix application ID
        - EXERCISE_API_KEY     : Nutritionix application key
        - SHEETY_API_TOKEN     : Sheety authorisation token (include the
                                 scheme if required, e.g. "Bearer <token>")

    Typical usage:
        tracker = GymDataProcessing(
            query="ran 5km and did 20 minutes of cycling",
            weight=75.0,
            height=180.0,
            age=25,
            gender="male",
        )
        tracker.log_exercises()

    Raises:
        KeyError: If any required environment variable is missing.
        requests.HTTPError: If either API returns a non-2xx response.
    """

    EXERCISE_URL_ENDPOINT = "https://app.100daysofpython.dev/v1/nutrition/natural/exercise"
    SHEETY_URL = "https://api.sheety.co/12b1cd54a019188aeb95639019259c73/workoutTracker/workouts"

    def __init__(self, query: str, weight: float, height: float, age: int, gender: str):
        self.query = query
        self.weight = weight
        self.height = height
        self.age = age
        self.gender = gender

        self.exercise_headers = {
            "Content-Type": "application/json",
            "x-app-id": os.environ["EXERCISE_API_APP_ID"],
            "x-app-key": os.environ["EXERCISE_API_KEY"],
        }
        self.sheets_headers = {
            "Content-Type": "application/json",
            "Authorization": os.environ["SHEETY_API_TOKEN"],
        }

    def fetch_exercises(self) -> list[dict]:
        """Call the nutrition API and return a list of parsed exercises."""
        payload = {
            "query": self.query,
            "weight_kg": self.weight,
            "height_cm": self.height,
            "age": self.age,
            "gender": self.gender,
        }

        response = requests.post(
            url=self.EXERCISE_URL_ENDPOINT,
            json=payload,
            headers=self.exercise_headers,
        )

        response.raise_for_status()
        return response.json()["exercises"]

    def log_exercises(self) -> None:
        """Fetch exercises and write each one as a row in the spreadsheet."""
        date = datetime.today().strftime("%d/%m/%Y")
        time = datetime.today().strftime("%H:%M:%S")

        for exercise in self.fetch_exercises():
            payload = {
                "workout": {
                    "date": date,
                    "time": time,
                    "exercise": exercise["name"].title(),
                    "duration": exercise["duration_min"],
                    "calories": exercise["nf_calories"],
                }
            }

            response = requests.post(
                url=self.SHEETY_URL,
                json=payload,
                headers=self.sheets_headers,
            )

            response.raise_for_status()
            print(f"Logged: {exercise['name']} — {response.status_code}")
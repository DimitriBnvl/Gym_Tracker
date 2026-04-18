from gym_data_processing import GymDataProcessing

WEIGHT_KG = 64
HEIGHT_CM = 182
AGE = 19
GENDER = "male"

print("""
        Welcome to Gym Track! To log your exercise, please use the following convention:
            * Include a time frame (in minutes or hours).
            * Include one of the following activities:
                - Running/Jogging - "ran for 30 minutes", "jogged 2 kilometers"
                - Swimming - "swam for 1 hour", "swimming laps"
                - Walking - "walked 3 km", "brisk walk 45 min"
                - Cycling - "biked for 1 hour", "rode bike 10 km"
                - Weightlifting - "lifted weights 45 min", "weight training"
        """
)

query = input("What exercises did you do today: ")

if __name__ == '__main__':
    data_processor = GymDataProcessing(query, WEIGHT_KG, HEIGHT_CM, AGE, GENDER)
    data_processor.log_exercises()



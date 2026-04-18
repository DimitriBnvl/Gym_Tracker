from gym_data_processing import GymDataProcessing

WEIGHT_KG = 64
HEIGHT_CM = 182
AGE = 19
GENDER = "male"

query = input("Enter query: ")

if __name__ == '__main__':
    data_processor = GymDataProcessing(query, WEIGHT_KG, HEIGHT_CM, AGE, GENDER)
    data_processor.post_exercise()



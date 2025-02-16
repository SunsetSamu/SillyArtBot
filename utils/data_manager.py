import json

class DataManager:
    @staticmethod
    def load_data():
        try:
            with open('guild_data.json', 'r') as f:
                print("==========\nData loaded successfully.\n==========")
                return json.load(f)
        except FileNotFoundError:
            print("XXXXXXXXXXXXXXXXXXXXX\nError: Guild data file not found. Initialized with empty data.\nXXXXXXXXXXXXXXXXXXXXX")
            return {}
        except json.JSONDecodeError:
            print("XXXXXXXXXXXXXXXXXXXXX\nError: Unable to decode JSON from guild data file.\nXXXXXXXXXXXXXXXXXXXXX")
            return {}

    @staticmethod
    def save_data(data):
        try:
            with open('guild_data.json', 'w') as file:
                json.dump(data, file, indent=4)
                print("==========\nData saved successfully.\n==========")
        except IOError as error:
            print(f"Error saving data: {error}")
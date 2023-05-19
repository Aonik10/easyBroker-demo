from src.properties import Properties
from secrets import API_KEY

if __name__ == "__main__":
    app = Properties(api_key=API_KEY)
    app.print_all_properties_titles()
from tkinter import *
from tkinter import ttk
import requests
from typing import Dict, Any


class WeatherAPIError(Exception):
    """Custom exception for API related errors"""
    pass


class WeatherAPI:
    """Handles all weather API related operations"""

    def __init__(self, api_key: str):
        self.__api_key = api_key
        self.__base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city: str) -> Dict[str, Any]:
        """Fetch weather data for given city"""
        try:
            url = f"{self.__base_url}?q={city}&appid={self.__api_key}"
            response = requests.get(url)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            return response.json()
        except requests.RequestException as e:
            raise WeatherAPIError(f"Failed to fetch weather data: {e}")


class WeatherData:
    """Handles weather data processing and storage"""

    def __init__(self, raw_data: Dict[str, Any]):
        self.__raw_data = raw_data
        self.__process_data()

    def __process_data(self):
        """Process raw weather data"""
        weather = self.__raw_data['weather'][0]
        main_data = self.__raw_data['main']

        self.__climate = weather['main']
        self.__description = weather['description']
        self.__temperature = main_data['temp'] - 273.15  # Convert to Celsius
        self.__pressure = main_data['pressure']
        self.__humidity = main_data['humidity']

    @property
    def climate(self) -> str:
        return self.__climate

    @property
    def description(self) -> str:
        return self.__description

    @property
    def temperature(self) -> float:
        return round(self.__temperature, 1)

    @property
    def pressure(self) -> int:
        return self.__pressure

    @property
    def humidity(self) -> int:
        return self.__humidity


class WeatherDisplay:
    """Handles the display of weather information"""

    def __init__(self, master):
        self.master = master
        self.__create_labels()

    def __create_labels(self):
        """Create all display labels"""
        # Weather Climate
        self.climate_label = Label(self.master, text="Weather Climate",
                                   font=('Poppins', 20))
        self.climate_value = Label(self.master, text="", font=('Poppins', 20))
        self.climate_label.place(x=25, y=270, height=50, width=200)
        self.climate_value.place(x=250, y=270, height=50, width=200)

        # Weather Description
        self.desc_label = Label(self.master, text="Weather Description",
                                font=('Poppins', 20))
        self.desc_value = Label(self.master, text="", font=('Poppins', 20))
        self.desc_label.place(x=25, y=330, height=50, width=200)
        self.desc_value.place(x=250, y=330, height=50, width=200)

        # Temperature
        self.temp_label = Label(self.master, text="Temperature",
                                font=('Poppins', 20))
        self.temp_value = Label(self.master, text="", font=('Poppins', 20))
        self.temp_label.place(x=25, y=390, height=50, width=200)
        self.temp_value.place(x=250, y=390, height=50, width=200)

        # Pressure
        self.pressure_label = Label(self.master, text="Pressure",
                                    font=('Poppins', 20))
        self.pressure_value = Label(self.master, text="", font=('Poppins', 20))
        self.pressure_label.place(x=25, y=450, height=50, width=200)
        self.pressure_value.place(x=250, y=450, height=50, width=200)

        # Humidity
        self.humidity_label = Label(self.master, text="Humidity",
                                    font=('Poppins', 20))
        self.humidity_value = Label(self.master, text="", font=('Poppins', 20))
        self.humidity_label.place(x=25, y=510, height=50, width=200)
        self.humidity_value.place(x=250, y=510, height=50, width=200)

    def update_display(self, weather_data: WeatherData):
        """Update all display labels with new weather data"""
        self.climate_value.config(text=weather_data.climate)
        self.desc_value.config(text=weather_data.description)
        self.temp_value.config(text=f"{weather_data.temperature}°C")
        self.pressure_value.config(text=f"{weather_data.pressure} hPa")
        self.humidity_value.config(text=f"{weather_data.humidity}%")


class WeatherApp:
    """Main Weather App class"""

    INDIAN_STATES = [
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
        "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jammu and Kashmir",
        "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra",
        "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
        "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
        "Uttar Pradesh", "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands",
        "Chandigarh", "Dadra and Nagar Haveli", "Daman and Diu", "Lakshadweep",
        "National Capital Territory of Delhi", "Puducherry"
    ]

    def __init__(self):
        # Initialize main window
        self.__window = Tk()
        self.__city_name = StringVar()

        # Initialize components
        self.__api = WeatherAPI("")
        self.__setup_window()
        self.__create_widgets()

    def __setup_window(self):
        """Configure the main window"""
        self.__window.title("Weather App")
        self.__window.config(bg='black')
        self.__window.geometry('500x600')

    def __create_widgets(self):
        """Create all GUI widgets"""
        # App Title
        self.__create_title()

        # Dropdown for city selection
        self.__create_dropdown()

        # Done button
        self.__create_button()

        # Weather display
        self.__display = WeatherDisplay(self.__window)

    def __create_title(self):
        """Create app title"""
        name_label = Label(self.__window, text="Weather App",
                           font=('Poppins', 30, 'bold'))
        name_label.place(x=25, y=25, height=50, width=450)

    def __create_dropdown(self):
        """Create city selection dropdown"""
        self.dropdown = ttk.Combobox(self.__window, values=self.INDIAN_STATES,
                                     font=('Poppins', 30),
                                     textvariable=self.__city_name)
        self.dropdown.place(x=25, y=130, height=50, width=450)

    def __create_button(self):
        """Create the Done button"""
        done_button = Button(self.__window, text="Done",
                             font=('Poppins', 30), command=self.__fetch_weather)
        done_button.place(x=200, y=200, height=50, width=100)

    def __fetch_weather(self):
        """Fetch and display weather data"""
        try:
            city = self.__city_name.get()
            if not city:
                raise ValueError("Please select a city")

            raw_data = self.__api.get_weather(city)
            weather_data = WeatherData(raw_data)
            self.__display.update_display(weather_data)

        except (WeatherAPIError, ValueError) as e:
            self.__show_error(str(e))

    def __show_error(self, message: str):
        """Display error message"""
        # You could create a more sophisticated error display
        print(f"Error: {message}")

    def run(self):
        """Start the application"""
        self.__window.mainloop()


if __name__ == "__main__":
    app = WeatherApp()
    app.run()

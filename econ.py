import matplotlib.pyplot as plt
import requests
from datetime import date
import os
import configparser
from full_fred.fred import Fred
from fredapi import Fred as fredapi
import pandas as pd

welcome = """
    Welcome to the Economic Tracker

    This tool is designed to pull basic economic indicators (CPI, M2, etc) and to generate a general economic forecast score
"""


class Lib:
    def get_api_key(self, key:str)->str:
        config = configparser.ConfigParser()
        config.read('env.ini')
        # Fetching the value from environment variables
        env_value = os.getenv(key)
        if env_value is None:
            # If environment variable is not set, fetching it from the config file
            env_value = config.get('API', key)
        return env_value

class FREDDB:
    # https://fred.stlouisfed.org/docs/api/fred/
    lib = Lib()
    fred = Fred()
    fred_api = fredapi()    
    menu_options = """
        1 = GDP
        2 = S&P 500
        0 = Go Back
    """

    def __init__(self) -> None:
        key = self.lib.get_api_key("fred")
        os.environ["FRED_API_KEY"] = key
        self.fred.env_api_key_found()
        self.myfred = self.fred_api(api_key=key)
        pd.options.display.max_colwidth = 60


    def menu(self):
        while True:
            resp = int(input(self.menu_options))
            match resp:
                case 0:
                    return
                case 1:
                    self.get_GDP()
                case 2:
                    self.get_sp500()

                               
    def get_GDP(self):
        if input("Do you just want the latest data (y/n)? ").lower() == "y":
            data = self.myfred.get_series_latest_release('GDP')
            print(data.tail())
        else:
            dt = input("For which date do you want GDP data? ")
            print(self.myfred.get_series_as_of_date('GDP', dt))


    def get_sp500(self):
        if input("Do you just want the latest data (y/n)? ").lower() == "y":
            s = self.myfred.get_series('SP500', observation_start=date.today())
            print(s.tail())
        else:
            dt = input("Starting on date (e.g. 2014-09-02)? ")
            dt_end = input("Ending on date: ")
            s = self.myfred.get_series('SP500', observation_start=dt, observation_end=dt_end)
            print(s.tail())



class Charts:
    def plot_cpi(self, cpi_values:list,years:list):
        """
        Plot the CPI values for each year for the past n years.

        Args:
        - cpi_values (list): A list of CPI values for each year.
        """
        # Extract the data for the past n years
        n = len(cpi_values)
        # years = range(2022 - n + 1, 2022 + 1)
        cpi_values_past_n_years = cpi_values[-n:]

        # Plotting the data
        plt.figure(figsize=(10, 6))
        plt.plot(years, cpi_values_past_n_years, marker='o', linestyle='-')
        plt.title('Consumer Price Index (CPI) for the Past ' + str(n) + ' Years')
        plt.xlabel('Year')
        plt.ylabel('CPI')
        plt.grid(True)
        plt.xticks(years)
        plt.tight_layout()
        plt.show()


class GetData:
    lib = Lib()

    def get_cpi_data(self, year:int)->float:
        """
        Get CPI data for a specific year from the United States Bureau of Labor Statistics (BLS) API.

        Args:
        - year (int): The year for which to retrieve CPI data.

        Returns:
        - float: The CPI value for the specified year.
        """
        # BLS API endpoint for CPI data
        url = f"https://api.bls.gov/publicAPI/v2/timeseries/data/CUSR0000SA0/{year}"

        try:
            # Fetch CPI data from the BLS API
            response = requests.get(url)
            data = response.json()

            # Extract CPI value from the response
            cpi_value = data['Results']['series'][0]['data'][0]['value']

            return float(cpi_value)

        except Exception as e:
            print(f"Error retrieving CPI data: {e}")
            return None
        

    def get_ppi_data(self, year:int)->float:
        """Personal Consumption Expenditures

        Args:
            year (int): Year for which data you want

        Returns:
            float: PPI value for given year
        """
        url = f"https://api.bls.gov/publicAPI/v2/timeseries/data/PCU{year}0000{year}"

        try:
            response = requests.get(url)
            data = response.json()
            ppi_value = data['Results']['series'][0]['data'][0]['value']
            return float(ppi_value)
        except Exception as e:
            print(f"Error retrieving PPI data: {e}")
            return None
    
    def get_pce_data(self, year:int)->float:
        """Personal Consumption Expenditures)

        Args:
            year (int): Year for which data you want

        Returns:
            float: PCE value for given year
        """
        api_key = self.lib.get_api_key("bea")
        url = f"https://apps.bea.gov/api/data?&UserID={api_key}&method=GetData&DataSetName=NIPA&TableName=T10105&LineCode=1&Frequency=A&Year={year}&ResultFormat=JSON"

        try:
            response = requests.get(url)
            data = response.json()

            pce_value = data['BEAAPI']['Results']['Data'][0]['DataValue']

            return float(pce_value)

        except Exception as e:
            print(f"Error retrieving PCE data: {e}")
            return None


charts = Charts()
data = GetData()
def update():
    # get data
    nu_years = int(input("How many years' data do you want? "))
    curr_yr = date.today().year
    pci = []
    pce = []
    ppi = []
    start_yr = curr_yr - nu_years
    years = []
    while start_yr < curr_yr + 1:
        pci.append(data.get_cpi_data(start_yr))
        pce.append(data.get_pce_data(start_yr))
        ppi.append(data.get_ppi_data(start_yr))
        years.append(start_yr)
        start_yr += 1
    # create graphs

    # FRED

if __name__ == "__main__":
    print(welcome)
    update()
import matplotlib.pyplot as plt
import requests

def plot_cpi(cpi_values, yrs):
    """
    Plot the CPI values for each year for the past n years.

    Args:
    - cpi_values (list): A list of CPI values for each year.
    - n (int): The number of past years to plot.
    """
    # Extract the data for the past n years
    years = range(2022 - n + 1, 2022 + 1)
    cpi_values_past_n_years = cpi_values[-n:]

    # Plotting the data
    plt.figure(figsize=(10, 6))
    plt.plot(years, cpi_values_past_n_years, marker='o', linestyle='-')
    plt.title('Consumer Price Index (CPI) for the Past ' + str(yrs) + ' Years')
    plt.xlabel('Year')
    plt.ylabel('CPI')
    plt.grid(True)
    plt.xticks(years)
    plt.tight_layout()
    plt.show()

# Example CPI values (replace this with your actual CPI data)
cpi_values = [200, 205, 210, 215, 220, 225, 230, 235, 240]

# Number of past years to plot
n = 5

# Plot the CPI for the past n years
plot_cpi_past_n_years(cpi_values, n)


def get_cpi_data(year):
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

# Example usage:
year = 2022
cpi_value = get_cpi_data(year)

if cpi_value is not None:
    print(f"The CPI value for {year} is: {cpi_value}")
else:
    print("Failed to retrieve CPI data.")

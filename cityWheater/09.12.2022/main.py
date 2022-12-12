import requests

# Set the A
# PI key for your OpenWeatherAPI account
api_key = "11eb278e065db2a543d346722cc6f29f"

# Set the location for which you want to get the weather data
city = input('Introdu numele orasului:')

# Set the API endpoint for the current weather data
endpoint = "https://api.openweathermap.org/data/2.5/weather"

# Set the parameters for the request
params = {
    "q": city,
    
    "appid": api_key,
    "units": "metric"
}

# Send the GET request to the API endpoint
response = requests.get(endpoint, params=params)

# Print the response status code to check if the request was successful
print(response.status_code)

# If the request was successful, parse the JSON data from the ressponse
if response.status_code == 200:
    data = response.json()
    print(data)
    vreme=data['weather'][0]['description']
    temperature=round(data['main']['temp'],2)
    wind=data['wind']['speed']
    print(vreme)
    print(temperature)
    print(wind)
    file_name = "data.txt"

    with open(file_name, "w") as file:
        file.write('data='+str(data))

else:
    print('Nu exista asa oras, mai incearca sa reintroduci numele')
import requests
import json
import datetime
import os
from dotenv import load_dotenv

# Gather values from .env file stored in root folder
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_ENDPOINT = os.getenv("API_ENDPOINT")
STOP_IDS = os.getenv("STOP_IDS") # multiple values

headers = {
    'Content-Type': 'application/graphql'
}
parameters = {
    'digitransit-subscription-key': API_KEY
}


def get_next_departures():
    """
    Fetches and prints the next transit departures for the specified stop.
    """

    # Check if the required environment variables are set.
    if not API_KEY or not API_ENDPOINT or not STOP_IDS:
        print("Error: Required environment variables are missing.")
        print("Please ensure API_KEY, API_ENDPOINT, and STOP_ID are set in your .env file or environment.")
        return

    try:
        # Make the POST request to the API with the GraphQL query.
        response = requests.post(API_ENDPOINT, params=parameters, headers=headers, data=getGraphQL_query())
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        data = response.json()

        # Check if the data contains the expected structure.
        if "data" not in data or data["data"]["stops"] is None:
            print("Error: Could not retrieve stop data. Please check the stop ID or API key.")
            return

        stop_data = data["data"]["stops"]
        for s in stop_data:
                
            stop_name = s["name"]
            vehicle_mode = s["vehicleMode"]
            departures = s["stoptimesWithoutPatterns"]

            print(f"\nNext departures for stop: {stop_name} {vehicle_mode}:")

            if not departures:
                print("No upcoming departures found.")
                return

            for i, departure in enumerate(departures):
                # The API returns departure time as a number of seconds from the beginning of the current day.
                departure_timestamp_seconds = departure["realtimeDeparture"]
                start_of_day = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
                departure_datetime = start_of_day + datetime.timedelta(seconds=departure_timestamp_seconds)
                
                # Format the correctly calculated datetime object into a readable time string.
                departure_time = departure_datetime.strftime('%H:%M:%S')
                # Extract the transit line number and destination.
                transit_number = departure["trip"]["route"]["shortName"]
                destination = departure["headsign"]

                print(f"  {i+1}. Line {transit_number} to {destination} at {departure_time}")

    except requests.exceptions.RequestException as e:
        # Check for specific 401 error and provide a more helpful message.
        if e.response and e.response.status_code == 401:
            print("Error: 401 Unauthorized. The API key is likely missing, incorrect, or expired.")
            print("Please ensure you have replaced 'YOUR_API_KEY_HERE' with a valid key and that it is in the correct header.")
        elif e.response and e.response.status_code == 404:
            print("Error: 404 Not Found. The API endpoint may be incorrect or deprecated.")
            print("The code has been updated to use the correct endpoint. Please try again.")
        else:
            print(f"An error occurred while connecting to the API: {e}")
    except json.JSONDecodeError:
        print("Error: The API response was not valid JSON.")
    except KeyError as e:
        print(f"Error: Missing key in API response data: {e}")


def getGraphQL_query():
    # GraphQL query to retrieve next departure data
    # We are gathering data for the next 5 departures.
    # The query also specifies which data fields we want for each departure,
    # such as the tram number, destination (headsign), and real-time departure time.
    
    # STOP_IDS .env variable supports a single stop (ex. "HSL:11235") or multiple stops in csv format (ex. "HSL:11235,HSL:81321")
    query = """
        {
        stops(ids: ["%s"]) {
            name
            vehicleMode
            stoptimesWithoutPatterns(numberOfDepartures: 5) {
            realtimeDeparture
            headsign
            trip {
                route {
                shortName
                }
            }
            }
        }
        }
        """ % "\", \"".join(STOP_IDS.split(",")) #Format STOP_IDS for GraphQL query
    
    return query


if __name__ == "__main__":
    get_next_departures()
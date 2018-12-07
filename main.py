import sys
import json
import googlemaps
import gmplot


# Load Jason Data from commandline argument
with open(sys.argv[1]) as source_json_data:
    imported_json_data = json.load(source_json_data)

# Convert Jason Employee Location Format to GoogleAPI Query Format and get Locations

# Create object for storing incoming locations from the file
API_locations = []

# Create a connection to google API for search
gmaps = googlemaps.Client(key='AIzaSyDCXDLtoCKtmP17ElUD6NH8YD5QyQgbL3M')

# Search through provided json data for addresses
for employee_location in imported_json_data:
    try:

        # order provided locations in API compatible address format
        employee_API_address = employee_location["City"]\
                               + ", "\
                               + employee_location["State"]\
                               + ", "\
                               + employee_location["Country"]

        # Query google for the Geocode location (GPS cord)
        API_locations.append(gmaps.geocode(employee_API_address))

    # Handle error resulting from blank employee address inputs
    except TypeError:
        continue

# Convert google results in to lat long only data and add them to the gmplot map for later export
# Create gmplot object centered around seattle, WA
displaymap = gmplot.GoogleMapPlotter(47.5706548, -122.2220674, 13)

# Go though available sites and breakdown their results into only cordates
for sites in API_locations:

    # Look at the all site Data
    complete_site_info = sites

    # Examine only the location data for a site
    location_data = complete_site_info[0]

    # Examine geographical data for a site
    API_defined_site_center = location_data['geometry']

    # Look at the Geographical center for a site
    cord_object = (API_defined_site_center['location'])

    # Create a marker for the site coordinate on the gmplot
    displaymap.marker(cord_object['lat'], cord_object['lng'], "red")

# export the gmplot map
displaymap.draw("exportmap.html")

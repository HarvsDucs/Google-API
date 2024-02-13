import streamlit as st
import requests
import json
# Title of the app
st.title('Solar Savings Calculator')

address = st.text_input("Enter your address", placeholder="1234 Main St, Anytown, Country")

# List of electric bill values
bill_values = [40, 45, 50, 60, 70, 80, 90, 100, 125, 150, 175, 200, 225, 250, 300, 350, 400, 450, 500]

# Adding a select slider
selected_bill = st.select_slider(
    'Select your monthly electric bill',
    options=bill_values,
    format_func=lambda x: f"${x}"
)
print(bill_values)

if selected_bill in bill_values:
    i = bill_values.index(selected_bill) + 4

# Display the selected values
print(f'Your selected monthly electric bill is: ${selected_bill}')
print(f'Inputted address is: {address}')



#GeoCoding Google API

address = address
api_key = "AIzaSyCiasKnnynYp8bW_picPLFLMz3_7EjFiqc"
url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"

response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Convert the response to JSON
    data = response.json()
    print(data)
    formatted_json_2 = json.loads(response.text)

    location = formatted_json_2["results"][0]["formatted_address"]
    
    print(f"Captured address at: {location}?")

    st.write(f'Captured address at: {location}')

    latitude = formatted_json_2["results"][0]["geometry"]["location"]["lat"]
    print(f"Latitude: {latitude}")

    longitude = formatted_json_2["results"][0]["geometry"]["location"]["lng"]
    print(f"Longitude: {longitude}")

    api_key = "AIzaSyCiasKnnynYp8bW_picPLFLMz3_7EjFiqc"
    url = "https://solar.googleapis.com/v1/buildingInsights:findClosest"

    # Parameters to be sent in the query string
    params = {
        'location.latitude': latitude,
        'location.longitude': longitude,
        'key': api_key
    }

    # Making the GET request
    response = requests.get(url, params=params)

    # Assuming the response is JSON, parsing it
    data = response.json()

    formatted_json = json.dumps(data, indent=4, sort_keys=True)
    formatted_json_2 = json.loads(response.text)

    # Testing the Center Location from GeoCoding API to solar API @ 250 watts and other default values

    units_value = formatted_json_2["solarPotential"]["financialAnalyses"][i]["monthlyBill"]["units"]
    st.write(f"Monthly Electric Bill: ${units_value}")

    units_value = formatted_json_2["solarPotential"]["financialAnalyses"][i]["cashPurchaseSavings"]["rebateValue"]["units"]
    st.write(f"#### Cash Paid Rebate Value: ${units_value}")

    st.write("### For financed payments @ 0.05 interest rate")
    units_value = formatted_json_2["solarPotential"]["financialAnalyses"][i]["financedPurchaseSavings"]["savings"]["savingsYear1"]["units"]
    st.write(f"#### Savings after 1 year: ${units_value}")

    units_value = formatted_json_2["solarPotential"]["financialAnalyses"][i]["financedPurchaseSavings"]["savings"]["savingsYear20"]["units"]
    st.write(f"#### Savings after 20 years: ${units_value}")
else:
    print("Error:", response.status_code)
    st.write(f'Please input address')




from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Function to fetch currency conversion factor
def fetch_conversion_factor(source, target):
    url = "https://api.currencyfreaks.com/v2.0/rates/latest?apikey=2aeff7dd1ab84fcba58d4b8606530379"
    
    response = requests.get(url)
    data = response.json()

    # Debugging: Print API response to check structure
    print("API Response:", data)

    if isinstance(data, dict) and "rates" in data:
        rates = data["rates"]

        if isinstance(rates, dict) and source in rates and target in rates:
            source_rate = float(rates[source])
            target_rate = float(rates[target])
            return target_rate / source_rate  # Correct conversion formula

    return None  # Return None if conversion is not possible

@app.route('/', methods=['POST'])
def index():
    try:
        data = request.get_json()
        print("Received Data:", data)  # Debugging: Check incoming request data

        # Extract parameters from Dialogflow request
        source_currency = data['queryResult']['parameters']['unit-currency']['currency']
        amount = float(data['queryResult']['parameters']['unit-currency']['amount'])
        target_currency = data['queryResult']['parameters']['currency-name']

        # Fetch conversion factor
        cf = fetch_conversion_factor(source_currency, target_currency)

        if cf is None:
            response_text = "Sorry, I couldn't fetch the conversion rate for {} to {}".format(source_currency, target_currency)
        else:
            final_amount = round(amount * cf, 2)
            response_text = "{} {} is approximately {} {}".format(amount, source_currency, final_amount, target_currency)

        return jsonify({'fulfillmentText': response_text})
    
    except Exception as e:
        print("Error:", str(e))  # Debugging: Print the error
        return jsonify({'fulfillmentText': f"An error occurred: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)

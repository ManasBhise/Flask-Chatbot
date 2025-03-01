from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Function to fetch the conversion rate
def fetch_conversion_factor(source, target):
    url = "https://api.currencyfreaks.com/v2.0/rates/latest?apikey=2aeff7dd1ab84fcba58d4b8606530379"
    
    response = requests.get(url)
    data = response.json()

    # Extract conversion rate safely
    if "rates" in data and source in data["rates"] and target in data["rates"]:
        source_rate = float(data["rates"][source])
        target_rate = float(data["rates"][target])
        return target_rate / source_rate  # Conversion factor
    else:
        return None  # Handle missing currency

@app.route("/", methods=["POST"])
def index():
    try:
        data = request.get_json()

        # Extract values safely
        source_currency = data['queryResult']['parameters']['unit-currency']['currency']
        amount = data['queryResult']['parameters']['unit-currency']['amount']
        target_currency = data['queryResult']['parameters']['currency-name']

        # Get conversion factor
        cf = fetch_conversion_factor(source_currency, target_currency)
        if cf is None:
            return jsonify({"fulfillmentText": "Invalid currency or conversion not available."})

        final_amount = round(amount * cf, 2)

        # Response format
        response = {
            "fulfillmentText": f"{amount} {source_currency} is {final_amount} {target_currency}"
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"fulfillmentText": f"An error occurred: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)

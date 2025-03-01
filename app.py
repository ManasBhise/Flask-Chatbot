from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Function to fetch conversion rate
def fetch_conversion_rate(source, target):
    url = "https://api.currencyfreaks.com/v2.0/rates/latest?apikey=2aeff7dd1ab84fcba58d4b8606530379"
    
    response = requests.get(url)
    data = response.json()

    print("API Response:", data)  # Debugging: See actual API data

    try:
        rates = data.get("rates", {})
        source_rate = float(rates.get(source, 0))
        target_rate = float(rates.get(target, 0))

        if source_rate == 0 or target_rate == 0:
            return None  # Invalid currency

        return target_rate / source_rate  # Conversion factor

    except Exception as e:
        print("Error fetching rates:", str(e))
        return None  # Handle API errors

@app.route("/", methods=["POST"])
def index():
    try:
        data = request.get_json()

        # Extract values safely (Fix: Handle lists correctly)
        source_currency = data['queryResult']['parameters']['unit-currency'][0]['currency'].upper()
        amount = data['queryResult']['parameters']['unit-currency'][0]['amount']
        target_currency = data['queryResult']['parameters']['currency-name'][0].upper()

        # Get conversion rate
        conversion_rate = fetch_conversion_rate(source_currency, target_currency)
        if conversion_rate is None:
            return jsonify({"fulfillmentText": "Invalid currency or conversion rate not available."})

        final_amount = round(amount * conversion_rate, 2)

        # Response format
        response = {
            "fulfillmentText": f"{amount} {source_currency} is {final_amount} {target_currency}"
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"fulfillmentText": f"An error occurred: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)

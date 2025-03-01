from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Function to fetch the conversion rate
def fetch_conversion_factor(source, target):
    url = "https://api.currencyfreaks.com/v2.0/rates/latest?apikey=2aeff7dd1ab84fcba58d4b8606530379"
    
    response = requests.get(url)
    data = response.json()

    # Debugging: Print API response structure
    print("API Response:", data)

    # Ensure API returns rates
    if "rates" in data:
        rates = data["rates"]

        if source in rates and target in rates:
            source_rate = float(rates[source])
            target_rate = float(rates[target])

            return target_rate / source_rate  # Conversion factor
        else:
            return None  # Invalid currency

    return None  # Handle API structure errors

@app.route("/", methods=["POST"])
def index():
    try:
        data = request.get_json()

        # Extract values safely
        source_currency = data['queryResult']['parameters']['unit-currency']['currency'].upper()
        amount = data['queryResult']['parameters']['unit-currency']['amount']
        target_currency = data['queryResult']['parameters']['currency-name'].upper()

        # Get conversion factor
        cf = fetch_conversion_factor(source_currency, target_currency)
        if cf is None:
            return jsonify({"fulfillmentText": "Invalid currency or conversion rate not available."})

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

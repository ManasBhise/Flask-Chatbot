from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Webhook route for Dialogflow
@app.route('/', methods=['POST'])
def index():
    try:
        # Extract data from Dialogflow's request
        data = request.get_json()
        source_currency = data['queryResult']['parameters']['unit-currency']['currency']
        amount = data['queryResult']['parameters']['unit-currency']['amount']
        target_currency = data['queryResult']['parameters']['currency-name']

        # Fetch conversion rate
        cf = fetch_conversion_factor(source_currency, target_currency)

        if cf is None:
            return jsonify({'fulfillmentText': "Sorry, I couldn't fetch the exchange rate at the moment."})

        final_amount = round(amount * cf, 2)

        # Response for Dialogflow
        response = {
            'fulfillmentText': "{} {} is approximately {} {}".format(amount, source_currency, final_amount, target_currency)
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({'fulfillmentText': "An error occurred: {}".format(str(e))})

# Function to fetch exchange rates from CurrencyFreaks API
def fetch_conversion_factor(source, target):
    api_key = "2aeff7dd1ab84fcba58d4b8606530379"
    url = f"https://api.currencyfreaks.com/v2.0/rates/latest?apikey={api_key}"

    response = requests.get(url)
    if response.status_code != 200:
        return None

    data = response.json()
    rates = data.get("rates", {})

    if target in rates:
        return float(rates[target])
    return None

if __name__ == '__main__':
    app.run(debug=True)

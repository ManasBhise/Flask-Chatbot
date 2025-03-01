from flask import Flask, request,jsonify
import requests

app = Flask(__name__)


@app.route('/',methods=['POST'])

def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']


    cf = fetch_conversion_factor(source_currency, target_currency)
    final_amount = amount*cf

    response = {
        'fulfillmentText':"{} {} is {} {}".format(amount,source_currency,final_amount,target_currency)
    }
    return jsonify(response)

def fetch_conversion_factor(source, target):
    url = "https://api.currencyfreaks.com/v2.0/rates/latest?apikey=2aeff7dd1ab84fcba58d4b8606530379".format(source,target)

    response = requests.get(url)
    response = response.json()
    return response['{}_{}'.format(source,target )]
   
if __name__ == '__main__':
    app.run(debug=True) 

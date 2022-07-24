from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects import campaign
from facebook_business.api import FacebookAdsApi
from google.cloud import bigquery
from dotenv import load_dotenv
from enum import Enum
import requests
import json

load_dotenv()

def bq(data):

    client = bigquery.Client()
    rows_insert = data

    errors = client.insert_rows_json('movistar-proyecto.movistar.facebook-insights', rows_insert)
    if errors == []:
        print("Se han insertado los datos correctamente")
    else:
        print("Se ha presentado errores".format(errors))


def main(token):
    
    my_account = AdAccount('act_993734317752440')
    campaings = my_account.get_campaigns()
    campaing_aleatory = campaings[0]['id']

    breakdowns = ['age', 'gender']

    class dataPreset(Enum):
        today = 'today'

    url = f"https://graph.facebook.com/v14.0/{campaing_aleatory}/insights?breakdowns={breakdowns}&data_preset={dataPreset.today}&access_token={token}"

    request_data = requests.get(url)
    json_data = json.loads(request_data.content)
    data = json_data['data']

    return bq(data)
    


if __name__ == '__main__':

    my_app_id = '3298246517085760'
    my_app_secret = '1ae9d64894909ccc7702c81b9ffe58d8'
    my_access_token = 'EAAu3vNwIVkABAOS0kkxEOpAmqG7ZBn66qvixETAZCV3H3ZBDekV6oOiaBArbg7xfAvmvvaly07HzrceiQMxZC4uuDTEIRVZCg74L9pe36rZANhCUSvcUqZCnr5nmQpDZBfVNe2xwBxhWLcG9Wgtfyr6ds95fKO5gE6yxGLuZCt3ttByZADtKBtfU1qARQe8BNjnbgZBh4F0m6scn5rNcpajbClh8xEZCdEEQRke8Gwqc9uDSFK8uG6X1pnke'
    FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)

    main(my_access_token)
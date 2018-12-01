from flask import Flask
import pandas as pd
import hei_loader
import json

app = Flask(__name__)

# This is an example of what score_from_hhid will return after build_json_response
# {
# 	"hhid": "123",
# 	"hh_score": 2,
# 	"items": [{
# 			"description": "first food",
# 			"score": 1
# 		},
# 		{
# 			"description": "second food",
# 			"score": 1
# 		}
# 	]
# }
def build_json_response(df):
    response = {}
    response['hhnum'] = df['hhnum'].iloc[0].item()
    response['hhscore'] = df['hei_score'].sum().item()
    items = []
    for idx,row in df.iterrows():
        mydict = {}
        mydict['description'] = row['usdadescmain']
        mydict['hei_score'] = row['hei_score']
        items.append(mydict)
    response['items'] = items
    return json.dumps(response)

# returns all info for a household based on householdID. Grabbing random when we loading nutrifhir frontend
@app.route('/score_from_hhnum', methods=['GET'])
def hhid_to_score():
    df = hei_loader.get_household_df()
    json_response = build_json_response(df)
    return json_response

@app.route('/test/<mystr>', methods=['GET'])
def tester(mystr):
    return "string is {}".format(mystr)

# takes in UPCcode, returns HEI score.
@app.route('/score_from_upc/<upc>', methods=['GET'])
def get_score_from_upc(upc):
    results = {}
    upc_df = hei_loader.get_upc_df(upc)
    if upc_df.empty:
        results['usdadescmain'] = 'invalid food code'
        results['hei_score'] = 0
    else:
        row = upc_df.iloc[0].to_dict()
        results['usdadescmain'] = row['usdadescmain']
        results['hei_score'] = row['hei_score']
    return json.dumps(results)

# takes in foodcode returns HEI score
@app.route('/score_from_foodcode/<foodcode>', methods=['GET'])
def get_score_from_foodcode(foodcode):
    results = {}
    food_df = hei_loader.get_foodcode_df(float(foodcode))
    if food_df.empty:
        results['usdadescmain'] = 'invalid food code'
        results['hei_score'] = 0
    else:
        row = food_df.iloc[0].to_dict()
        results['usdadescmain'] = row['usdadescmain']
        results['hei_score'] = row['hei_score']
    return json.dumps(results)


# run the program
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
import requests
import xmltodict

def request(params):
  response = requests.get("http://web-api.tp.entsoe.eu/api",params=params)
  print(response.status_code)
  #print(response.json())
  if response.status_code !=200:
    data = xmltodict.parse(response.text)
    key = list(data.keys())[0]
    if key == "Acknowledgement_MarketDocument":
      return {"status":False,"data":[],"cause":data.get("Acknowledgement_MarketDocument").get("Reason").get("text")}
    else:
      return {"status":False,"data":[],"cause":"API crash."}
  elif response.status_code ==200:
    data = xmltodict.parse(response.text)
    key = list(data.keys())[0]
    if key == "Acknowledgement_MarketDocument":
      return {"status":False,"data":[],"cause":data.get("Acknowledgement_MarketDocument").get("Reason").get("text")}
    elif key == "GL_MarketDocument":
      return {"status":True,"data":data.get("GL_MarketDocument").get("TimeSeries"),"cause":""}
    elif key == "Publication_MarketDocument":
      return {"status":True,"data":data.get("Publication_MarketDocument").get("TimeSeries"),"cause":""}
    elif key == "Balancing_MarketDocument":
      return {"status":True,"data":data.get("Balancing_MarketDocument").get("TimeSeries"),"cause":""}



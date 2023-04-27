from app.models import Generation
from fastapi import Depends
from src.helpers.api_process.request_to_api import request
from datetime import datetime,timedelta
from src.helpers.external.utiliy import date_list_creator
from src.configs.datasources import psrType

def parse_params(generation: Generation = Depends(Generation)):
  start_period = datetime.strptime(generation.periodStart, '%Y-%m-%d %H:%M')
  end_period = datetime.strptime(generation.periodEnd, '%Y-%m-%d %H:%M')
  params_dict = dict(generation)
  params_dict['periodStart'] = start_period.strftime("%Y") + start_period.strftime("%m") + start_period.strftime(
    "%d") + start_period.strftime("%H") + start_period.strftime("%M")
  params_dict['periodEnd'] = end_period.strftime("%Y") + end_period.strftime("%m") + end_period.strftime(
    "%d") + end_period.strftime("%H") + end_period.strftime("%M")
  return params_dict


def installed_capacity_per_type(parsed_params: parse_params = Depends(parse_params)):
  if parsed_params['generationType'] != 'insCapPerType':
    return {}
  params_to_request = parsed_params.copy()
  params_to_request.pop("generationType")
  params_to_request['processType'] = "A33"
  params_to_request['documentType'] = "A68"
  resp = request(params_to_request)
  if resp['status'] == False:
    return resp

  obj_list = resp.get("data")
  end_date_str = obj_list[0].get("Period").get("timeInterval").get("end")
  year = datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M%z').year
  returning_obj = {"data":{},"year":year}
  for obj_ in obj_list:
    key = psrType.get(obj_.get("MktPSRType").get("psrType"))
    returning_obj["data"][key] = float(obj_.get("Period").get("Point").get("quantity"))
  return returning_obj

def day_ahead_aggregated_generation_forecast(parsed_params: parse_params = Depends(parse_params)):
  if parsed_params['generationType'] != 'dayAhAggGenFor':
    return {}
  params_to_request = parsed_params.copy()
  params_to_request.pop("generationType")
  params_to_request['processType'] = "A01"
  params_to_request['documentType'] = "A71"
  resp = request(params_to_request)
  if resp['status'] == False:
    return resp
  obj_list = [resp.get("data")] if type(resp.get("data")) != type([]) else resp.get("data")
  obj_list = [d for d in obj_list if "inBiddingZone_Domain.mRID" in list(d.keys())]
  returning_obj = {"data":[],"status":True}
  for obj in obj_list:
    start_date_str = obj.get("Period").get("timeInterval").get("start")
    end_date_str = obj.get("Period").get("timeInterval").get("end")
    resolution = obj.get("Period").get("resolution")
    date_list = date_list_creator(start_date_str, end_date_str,resolution)
    data_list = obj.get("Period").get("Point")
    print(len(data_list),len(date_list))
    for data_, date_ in zip(data_list, date_list):
      returning_obj["data"].append({"date": date_, "value": data_.get("quantity")})
  return returning_obj


def day_ahead_solar_generation_forecast(parsed_params: parse_params = Depends(parse_params)):
  if parsed_params['generationType'] != 'dayAhSolGenFor':
    return {}
  params_to_request = parsed_params.copy()
  params_to_request.pop("generationType")
  params_to_request['processType'] = "A01"
  params_to_request['documentType'] = "A69"
  params_to_request['psrType'] = "B16"
  resp = request(params_to_request)
  if resp['status'] == False:
    return resp
  obj_list = [resp.get("data")] if type(resp.get("data")) != type([]) else resp.get("data")
  obj_list = [d for d in obj_list if "inBiddingZone_Domain.mRID" in list(d.keys())]
  returning_obj = {"data":[],"status":True}
  for obj in obj_list:
    start_date_str = obj.get("Period").get("timeInterval").get("start")
    end_date_str = obj.get("Period").get("timeInterval").get("end")
    resolution = obj.get("Period").get("resolution")
    date_list = date_list_creator(start_date_str, end_date_str,resolution)
    data_list = obj.get("Period").get("Point")
    for data_, date_ in zip(data_list, date_list):
      returning_obj["data"].append({"date": date_, "value": float(data_.get("quantity"))})
  return returning_obj



def actual_generation_per_production_type(parsed_params: parse_params = Depends(parse_params)):
  if parsed_params['generationType'] != 'acGenPerProdType':
    return {}
  params_to_request = parsed_params.copy()
  params_to_request.pop("generationType")
  params_to_request['processType'] = "A16"
  params_to_request['documentType'] = "A75"
  resp = request(params_to_request)
  if resp['status'] == False:
    return resp
  obj_list = resp.get("data")
  returning_obj = {"data":[],"status":True}
  for obj in obj_list:
    start_date_str = obj.get("Period").get("timeInterval").get("start")
    end_date_str = obj.get("Period").get("timeInterval").get("end")

    resolution = obj.get("Period").get("resolution")
    date_list = date_list_creator(start_date_str, end_date_str,resolution)
    data_list = obj.get("Period").get("Point")
    key = psrType.get(obj.get("MktPSRType").get("psrType"))
    if len(data_list) == len(date_list):
      for data_, date_ in zip(data_list, date_list):
        returning_obj["data"].append({"date": date_, "value": data_.get("quantity"),"type":key})
  return returning_obj



def generation(insCapPerType : installed_capacity_per_type = Depends(installed_capacity_per_type),
               dayAhAggGenFor : day_ahead_aggregated_generation_forecast = Depends(day_ahead_aggregated_generation_forecast),
               dayAhSolGenFor : day_ahead_solar_generation_forecast = Depends(day_ahead_solar_generation_forecast),
               acGenPerProdType : actual_generation_per_production_type = Depends(actual_generation_per_production_type)):
  return {**insCapPerType,**dayAhAggGenFor,**dayAhSolGenFor,**acGenPerProdType}


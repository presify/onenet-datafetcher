from app.models import Load
from fastapi import Depends
from src.helpers.api_process.request_to_api import request
from datetime import datetime,timedelta
from src.helpers.external.utiliy import date_list_creator

def parse_params(load: Load = Depends(Load)):
  start_period = datetime.strptime(load.periodStart, '%Y-%m-%d %H:%M')
  end_period = datetime.strptime(load.periodEnd, '%Y-%m-%d %H:%M')
  params_dict = dict(load)
  params_dict['periodStart'] = start_period.strftime("%Y") + start_period.strftime("%m") + start_period.strftime(
    "%d") + start_period.strftime("%H") + start_period.strftime("%M")
  params_dict['periodEnd'] = end_period.strftime("%Y") + end_period.strftime("%m") + end_period.strftime(
    "%d") + end_period.strftime("%H") + end_period.strftime("%M")
  return params_dict


def actual_load(parsed_params: parse_params = Depends(parse_params)):
  if parsed_params['loadType'] != 'actLoad':
    return {}
  params_to_request = parsed_params.copy()
  params_to_request.pop("loadType")
  params_to_request['processType'] = "A16"
  resp = request(params_to_request)
  if resp['status'] == False:
    return resp
  else:
    obj_list = [resp.get("data")] if type(resp.get("data")) != type([]) else resp.get("data")
    returning_obj = {"data": [],"status":True}
    for obj in obj_list:
      start_date_str = obj.get("Period").get("timeInterval").get("start")
      end_date_str = obj.get("Period").get("timeInterval").get("end")
      resolution = obj.get("Period").get("resolution")
      date_list = date_list_creator(start_date_str,end_date_str,resolution)
      data_list = obj.get("Period").get("Point")
      for data_,date_ in zip(data_list,date_list):
        returning_obj["data"].append({"date":date_,"value":data_.get("quantity")})
    return returning_obj


def day_forecast(parsed_params: parse_params = Depends(parse_params)):
  if parsed_params['loadType'] != 'dayAhLoadFor':
    return {}
  params_to_request = parsed_params.copy()
  params_to_request.pop("loadType")
  params_to_request['processType'] = "A01"

  resp = request(params_to_request)
  if resp['status'] == False:
    return resp
  else:
    obj_list = [resp.get("data")] if type(resp.get("data")) !=type([]) else resp.get("data")
    returning_obj = {"data":[],"status":True}
    for obj in obj_list:
      start_date_str = obj.get("Period").get("timeInterval").get("start")
      end_date_str = obj.get("Period").get("timeInterval").get("end")
      resolution = obj.get("Period").get("resolution")
      date_list = date_list_creator(start_date_str, end_date_str,resolution)
      data_list = obj.get("Period").get("Point")
      for data_, date_ in zip(data_list, date_list):
        returning_obj["data"].append({"date": date_, "value": data_.get("quantity")})
    return returning_obj


def week_forecast(parsed_params: parse_params = Depends(parse_params)):
  if parsed_params['loadType'] != 'weekAhLoadFor':
    return {}
  params_to_request = parsed_params.copy()
  params_to_request.pop("loadType")
  params_to_request['processType'] = "A31"

  resp = request(params_to_request)
  if resp['status'] == False:
    return resp
  else:
    obj_list = [resp.get("data")] if type(resp.get("data")) !=type([]) else resp.get("data")
    min_obj_list = [d for d in obj_list if d['businessType']=="A60" ]
    max_obj_list = [d for d in obj_list if d['businessType'] == "A61"]
    returning_obj = {"data":[],"status":True}
    for min_obj,max_obj in zip(min_obj_list,max_obj_list):
      start_date_str = min_obj.get("Period").get("timeInterval").get("start")
      end_date_str = min_obj.get("Period").get("timeInterval").get("end")
      resolution = min_obj.get("Period").get("resolution")
      date_list = date_list_creator(start_date_str, end_date_str,resolution)
      min_data_list = min_obj.get("Period").get("Point")
      max_data_list = max_obj.get("Period").get("Point")

      for min_data_,max_data_, date_ in zip(min_data_list,max_data_list, date_list):
        returning_obj["data"].append({"date": date_, "min_value": min_data_.get("quantity"),"max_value": max_data_.get("quantity")})
    return returning_obj


def month_forecast(parsed_params: parse_params = Depends(parse_params)):
  if parsed_params['loadType'] != 'monthAhLoadFor':
    return {}
  params_to_request = parsed_params.copy()
  params_to_request.pop("loadType")
  params_to_request['processType'] = "A32"

  resp = request(params_to_request)
  if resp['status'] == False:
    return resp
  else:
    obj_list = [resp.get("data")] if type(resp.get("data")) != type([]) else resp.get("data")
    min_obj_list = [d for d in obj_list if d['businessType'] == "A60"]
    max_obj_list = [d for d in obj_list if d['businessType'] == "A61"]
    returning_obj = {"data": [],"status":True}
    for min_obj, max_obj in zip(min_obj_list, max_obj_list):
      start_date_str = min_obj.get("Period").get("timeInterval").get("start")
      end_date_str = min_obj.get("Period").get("timeInterval").get("end")
      resolution = min_obj.get("Period").get("resolution")
      date_list = date_list_creator(start_date_str, end_date_str, resolution)
      min_data_list = min_obj.get("Period").get("Point")
      max_data_list = max_obj.get("Period").get("Point")
      for min_data_, max_data_, date_ in zip(min_data_list, max_data_list, date_list):
        returning_obj["data"].append(
          {"date": date_, "min_value": min_data_.get("quantity"), "max_value": max_data_.get("quantity")})
    return returning_obj


def year_forecast(parsed_params: parse_params = Depends(parse_params)):#Not appropriate
  if parsed_params['loadType'] != 'yearAhLoadFor':
    return {}
  params_to_request = parsed_params.copy()
  params_to_request.pop("loadType")
  params_to_request['processType'] = "A33"

  resp = request(params_to_request)
  if resp['status'] == False:
    return resp
  else:
    obj_list = [resp.get("data")] if type(resp.get("data")) != type([]) else resp.get("data")
    min_obj_list = [d for d in obj_list if d['businessType'] == "A60"]
    max_obj_list = [d for d in obj_list if d['businessType'] == "A61"]
    returning_obj = {"data": [],"status":True}
    for min_obj, max_obj in zip(min_obj_list, max_obj_list):
      min_data_list = min_obj.get("Period").get("Point")
      max_data_list = max_obj.get("Period").get("Point")
      for idx, (min_data_, max_data_) in enumerate(zip(min_data_list, max_data_list),start=1):
        returning_obj["data"].append(
          {"week":idx, "min_value": min_data_.get("quantity"), "max_value": max_data_.get("quantity")})
    return returning_obj


def load(load: actual_load = Depends(actual_load),day:day_forecast = Depends(day_forecast),week:week_forecast = Depends(week_forecast),month:month_forecast = Depends(month_forecast),year:year_forecast = Depends(year_forecast)):
  return {**load,**day,**week,**month,**year}


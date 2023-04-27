from app.models import Balancing
from fastapi import Depends
from src.helpers.api_process.request_to_api import request
from datetime import datetime,timedelta
from src.helpers.external.utiliy import date_list_creator


def parse_params(balancing: Balancing = Depends(Balancing)):
  start_period = datetime.strptime(balancing.periodStart, '%Y-%m-%d %H:%M')
  end_period = datetime.strptime(balancing.periodEnd, '%Y-%m-%d %H:%M')
  params_dict = dict(balancing)
  params_dict['periodStart'] = start_period.strftime("%Y") + start_period.strftime("%m") + start_period.strftime(
    "%d") + start_period.strftime("%H") + start_period.strftime("%M")
  params_dict['periodEnd'] = end_period.strftime("%Y") + end_period.strftime("%m") + end_period.strftime(
    "%d") + end_period.strftime("%H") + end_period.strftime("%M")
  return params_dict


def accepted_offers(parsed_params: parse_params = Depends(parse_params)):
  if parsed_params['balancingType'] != 'accOff':
    return {}
  params_to_request = parsed_params.copy()
  params_to_request.pop("balancingType")
  params_to_request['documentType'] = "A82"
  params_to_request['businessType'] = "A96"
  resp = request(params_to_request)
  if resp['status'] == False:
    return resp
  obj_list = [resp.get("data")] if type(resp.get("data")) != type([]) else resp.get("data")
  up_obj_list = [d for d in obj_list if d["flowDirection.direction"] == "A01"]
  down_obj_list = [d for d in obj_list if d["flowDirection.direction"] == "A02"]
  returning_obj = {"data": [],"status":True}
  for up_obj,down_obj in zip(up_obj_list,down_obj_list):
    start_date_str = up_obj.get("Period").get("timeInterval").get("start")
    end_date_str = up_obj.get("Period").get("timeInterval").get("end")
    resolution = up_obj.get("Period").get("resolution")
    date_list = date_list_creator(start_date_str, end_date_str, resolution)
    up_data_list = up_obj.get("Period").get("Point")
    down_data_list = down_obj.get("Period").get("Point")

    for up_data_, down_data_, date_ in zip(up_data_list,down_data_list, date_list):
      returning_obj["data"].append(
        {"date": date_, "up_value": up_data_.get("quantity"),"down_value": up_data_.get("quantity")})
  return returning_obj



def balancing(accOff: accepted_offers = Depends(accepted_offers)):
  return {**accOff}


from app.models import Transmission
from fastapi import Depends
from src.helpers.api_process.request_to_api import request
from datetime import datetime,timedelta
from src.helpers.external.utiliy import date_list_creator
from src.configs.datasources import psrType

def parse_params(transmission: Transmission = Depends(Transmission)):
  start_period = datetime.strptime(transmission.periodStart, '%Y-%m-%d %H:%M')
  end_period = datetime.strptime(transmission.periodEnd, '%Y-%m-%d %H:%M')
  params_dict = dict(transmission)
  params_dict['periodStart'] = start_period.strftime("%Y") + start_period.strftime("%m") + start_period.strftime(
    "%d") + start_period.strftime("%H") + start_period.strftime("%M")
  params_dict['periodEnd'] = end_period.strftime("%Y") + end_period.strftime("%m") + end_period.strftime(
    "%d") + end_period.strftime("%H") + end_period.strftime("%M")
  return params_dict


def forecasted_capacity(parsed_params: parse_params = Depends(parse_params)):
  if "AhForCap" not in  parsed_params['transmissionType']:
    return {}
  elif parsed_params['transmissionType'] == 'dayAhForCap':
    contact_market_aggrement_key = "A01"
  elif parsed_params['transmissionType'] == 'weekAhForCap':
    contact_market_aggrement_key = "A02"
  elif parsed_params['transmissionType'] == 'monthAhForCap':
    contact_market_aggrement_key = "A03"
  else:
    return {}
  params_to_request = parsed_params.copy()
  params_to_request.pop("transmissionType")
  params_to_request['contract_MarketAgreement.Type'] = contact_market_aggrement_key
  params_to_request['documentType'] = "A61"
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
      date_list = date_list_creator(start_date_str, end_date_str, resolution)
      data_list = obj.get("Period").get("Point")
      for data_, date_ in zip(data_list, date_list):
        returning_obj["data"].append(
          {"date": date_, "value": data_.get("quantity")})
    return returning_obj


def offered_capacity(parsed_params: parse_params = Depends(parse_params)):
  if parsed_params['transmissionType'] != 'offCap':
    return {}
  params_to_request = parsed_params.copy()
  params_to_request.pop("transmissionType")
  params_to_request['contract_MarketAgreement.Type'] = "A01"
  params_to_request['documentType'] = "A31"
  params_to_request['auction.Type'] = "A01"
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
      date_list = date_list_creator(start_date_str, end_date_str, resolution)
      data_list = obj.get("Period").get("Point")
      key = datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M%z').strftime('%Y-%m-%d') + "-" + datetime.strptime(
        end_date_str, '%Y-%m-%dT%H:%M%z').strftime('%Y-%m-%d')
      for data_, date_ in zip(data_list, date_list):
        returning_obj["data"].append(
          {"date": date_, "value": data_.get("quantity")})
    return returning_obj



def intraday_transfer_limits(parsed_params: parse_params = Depends(parse_params)):
  if parsed_params['transmissionType'] != 'inTrLim':
    return {}
  params_to_request = parsed_params.copy()
  params_to_request.pop("transmissionType")
  params_to_request['documentType'] = "A93"
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
      date_list = date_list_creator(start_date_str, end_date_str, resolution)
      data_list = obj.get("Period").get("Point")
      for data_, date_ in zip(data_list, date_list):
        returning_obj["data"].append(
          {"date": date_, "value": data_.get("quantity")})
    return returning_obj


def cross_border_physical_flow(parsed_params: parse_params = Depends(parse_params)):
  if parsed_params['transmissionType'] != 'crBorPhyFl':
    return {}
  params_to_request = parsed_params.copy()
  params_to_request.pop("transmissionType")
  params_to_request['documentType'] = "A11"

  resp = request(params_to_request)
  if resp['status'] == False:
    return resp

  returning_obj = {"data": [],"status":True}
  data_list = resp.get("data").get("Period").get("Point")
  start_date_str = resp.get("data").get("Period").get("timeInterval").get("start")
  end_date_str = resp.get("data").get("Period").get("timeInterval").get("end")
  resolution =  resp.get("data").get("Period").get("resolution")
  date_list = date_list_creator(start_date_str,end_date_str,resolution)
  for data_,date_ in zip(data_list,date_list):
    returning_obj["data"].append({"date":date_,"value":data_.get("quantity")})
  return returning_obj


def scheduled_commercial_exchanges(parsed_params: parse_params = Depends(parse_params)):
  if parsed_params['transmissionType'] != 'schComEx':
    return {}
  params_to_request = parsed_params.copy()
  params_to_request.pop("transmissionType")
  params_to_request['documentType'] = "A09"
  params_to_request["contract_MarketAgreement.Type"] = "A05"
  resp = request(params_to_request)
  if resp['status'] == False:
    return resp
  obj_list = [resp.get("data")] if type(resp.get("data")) != type([]) else resp.get("data")
  returning_obj = {"data": [],"status":True}
  for obj in obj_list:
    start_date_str = obj.get("Period").get("timeInterval").get("start")
    end_date_str = obj.get("Period").get("timeInterval").get("end")
    resolution = resp.get("Period").get("resolution")
    date_list = date_list_creator(start_date_str, end_date_str, resolution)
    data_list = obj.get("Period").get("Point")
    for data_, date_ in zip(data_list, date_list):
      returning_obj["data"].append({"date": date_, "value": data_.get("quantity")})
  return returning_obj

def day_ahead_prices(parsed_params: parse_params = Depends(parse_params)):
  if parsed_params['transmissionType'] != 'dayAhPr':
    return {}
  params_to_request = parsed_params.copy()
  params_to_request.pop("transmissionType")
  params_to_request['documentType'] = "A44"
  resp = request(params_to_request)
  if resp['status'] == False:
    return resp
  obj_list = [resp.get("data")] if type(resp.get("data")) != type([]) else resp.get("data")
  returning_obj = {"data": [],"status":True}
  for obj in obj_list:
    start_date_str = obj.get("Period").get("timeInterval").get("start")
    end_date_str = obj.get("Period").get("timeInterval").get("end")
    resolution = obj.get("Period").get("resolution")
    date_list = date_list_creator(start_date_str, end_date_str, resolution)
    data_list = obj.get("Period").get("Point")
    for data_, date_ in zip(data_list, date_list):
      returning_obj["data"].append({"date": date_, "value": data_.get("price.amount")})
  return returning_obj


def transmission(forCap: forecasted_capacity = Depends(forecasted_capacity),
                 offCap: offered_capacity = Depends(offered_capacity),
                 inTrLim: intraday_transfer_limits = Depends(intraday_transfer_limits),
                 crBorPhyFl: cross_border_physical_flow = Depends(cross_border_physical_flow),
                 schComEx: scheduled_commercial_exchanges = Depends(scheduled_commercial_exchanges),
                 dayAhPr: day_ahead_prices = Depends(day_ahead_prices)):
  return {**forCap,**offCap,**inTrLim,**crBorPhyFl,**schComEx,**dayAhPr}


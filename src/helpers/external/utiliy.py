from datetime import datetime, timedelta


def date_list_creator(start_str,end_str,process):
  process_quantity = int(''.join(filter(str.isdigit, process)))
  process_type = process[-1]
  if process_type == "M":
    start_date = datetime.strptime(start_str, '%Y-%m-%dT%H:%M%z')
    end_date = datetime.strptime(end_str, '%Y-%m-%dT%H:%M%z')
    hours = int((end_date - start_date) / timedelta(minutes=process_quantity))
    start_date += timedelta(hours=1)
    return [(start_date + timedelta(minutes=i*process_quantity)).strftime('%Y-%m-%d %H:%M') for i in range(0, hours )]
  elif process_type == "D":
    start_date = datetime.strptime(start_str, '%Y-%m-%dT%H:%M%z')
    end_date = datetime.strptime(end_str, '%Y-%m-%dT%H:%M%z')
    days = int((end_date - start_date) / timedelta(days=process_quantity))
    return [(start_date + timedelta(days=i*process_quantity)).strftime('%Y-%m-%d') for i in range(1, days + 1)]
  elif process_type == "week":
    start_date = datetime.strptime(start_str, '%Y-%m-%dT%H:%M%z')
    end_date = datetime.strptime(end_str, '%Y-%m-%dT%H:%M%z')
    days = int((end_date - start_date) / timedelta(days=7))
    return [(start_date + timedelta(days=i*7)).strftime('%Y-%m-%d') for i in range(1, days + 1)]



import csv

route_ids = []
with open('gtfs/routes.txt', 'r') as routes:
  routes_reader = csv.DictReader(routes)
  for i, row in enumerate(routes_reader):
    if i > 0:
      route_ids.append(row["route_id"])
  
trip_ids = []
with open('gtfs/trips.txt', 'r+') as trips:
  newtrips = []
  trips_reader = csv.DictReader(trips)
  data = list(trips_reader)
  before_size = len(data)
  for row in data:
    if row['route_id'] in route_ids:
      newtrips.append(row)
      trip_ids.append(row['trip_id'])

  trips.seek(0)
  trips.truncate()
  trips_writer = csv.DictWriter(trips, fieldnames=trips_reader.fieldnames)
  trips_writer.writeheader()
  trips_writer.writerows(newtrips)
  print(f'Removed {before_size - len(newtrips)} rows from trips.txt (out of {before_size}).')

stop_ids = []
with open('gtfs/stop_times.txt', 'r+') as stop_times:
  new_stop_times = []
  stop_times_reader = csv.DictReader(stop_times)
  data = list(stop_times_reader)
  before_size = len(data)
  for row in data:
    if row['trip_id'] in trip_ids:
      new_stop_times.append(row)
      stop_ids.append(row['stop_id'])

  stop_times.seek(0)
  stop_times.truncate()
  stop_times_writer = csv.DictWriter(stop_times, fieldnames=stop_times_reader.fieldnames)
  stop_times_writer.writeheader()
  stop_times_writer.writerows(new_stop_times)
  print(f'Removed {before_size - len(new_stop_times)} rows from stop_times.txt (out of {before_size}).')

with open('gtfs/stops.txt', 'r+') as stops:
  new_stops = []
  stops_reader = csv.DictReader(stops)
  data = list(stops_reader)
  before_size = len(data)
  for row in data:
    if row['stop_id'] in stop_ids:
      new_stops.append(row)
  stops.seek(0)
  stops.truncate()
  stops_writer = csv.DictWriter(stops, fieldnames=stops_reader.fieldnames)
  stops_writer.writeheader()
  stops_writer.writerows(new_stops)
  print(f'Removed {before_size - len(new_stops)} rows from stops.txt (out of {before_size}).')

with open('gtfs/transfers.txt', 'r+') as transfers:
  new_transfers = []
  transfers_reader = csv.DictReader(transfers)
  data = list(transfers_reader)
  before_size = len(data)
  for row in data:
    if row['to_stop_id'] in stop_ids and row['from_stop_id'] in stop_ids:
      new_transfers.append(row)
  transfers.seek(0)
  transfers.truncate()
  transfers_writer = csv.DictWriter(transfers, fieldnames=transfers_reader.fieldnames)
  transfers_writer.writeheader()
  transfers_writer.writerows(new_transfers)
  print(f'Removed {before_size - len(new_transfers)} rows from transfers.txt (out of {before_size}).')


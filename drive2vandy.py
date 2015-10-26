'''
Script takes a list of addresses and calculates the driving distance and duration of those addresses
to a destination. Afterwards, it calculates the corresponding zipcodes to that
destination
'''

import json
import urllib2
import csv
import time

apiKey = 'AIzaSyCU2GxBn2C4KnLX3tGOvw2NBkFTAXStkIA' #Alex's API can get 2500 elements/day, 100 elements/query, 100 elements/10 seconds

addresses = []
zipcodes = []
f = open('nashville_hc_addresses_only.txt','U')
for line in f:
    line = line.strip()
    addresses.append(line)
    if line[-5] == '-':  ### extract 5 digit zip from 9 digits
        zipcodes.append(line[-10:-5])
    else:
        zipcodes.append(line[-5:])
        
destination = '719 Thompson Lane, Nashville, TN 37204' ### 100 oaks address
mode = 'driving' ### can also take 'transit' or 'walking'
units = 'imperial' ### Value of distance is always in meters! Time is in seconds

limit = 40  # limit of addresses per query determined by trial and error (may be character based)

with open('drive2vandy.csv', 'wb') as f:
    writer = csv.writer(f)
    rowcount=0
    addresses = addresses + zipcodes
    for n in range(len(addresses)/limit+1):
        listStart = n*limit
        listEnd = (n+1)*limit
        origins = ''
        for address in addresses[listStart:listEnd]:
            origins = origins + '|' + address
        request =   'https://maps.googleapis.com/maps/api/distancematrix/json?origins=' \
                    + origins \
                    + '&destinations=' + destination \
                    + '&mode=' + mode \
                    + '&units=' + units \
                    + '&key=' + apiKey
        request = request.replace(" ", "_") ### URL request does not take # sign or spaces
        request= request.replace('#','') 
        data = json.load(urllib2.urlopen(request))
        time.sleep(1) # need a small time delay not to exceed rate-limit
        i = 0
        for element in data['rows']:
            status = element['elements'][0]['status']
            if status != 'OK':
                row = [addresses[i],status,status] #usually means address not found, use original address
            else:
                originAddress = data['origin_addresses'][i]
                drivingDistance = element['elements'][0]['distance']['value']
                drivingDuration = element['elements'][0]['duration']['value']
                row = [originAddress,drivingDistance,drivingDuration]
            writer.writerow(row) 
            rowcount+=1
            i += 1


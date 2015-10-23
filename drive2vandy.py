# -*- coding: utf-8 -*-

import json
import urllib2
import csv

apiKey = 'AIzaSyCU2GxBn2C4KnLX3tGOvw2NBkFTAXStkIA'

addresses = []
zipcodes = []
f = open('nashville_hc_addresses_only.txt','U')
for line in f:
    line = line.strip()
    line = line.replace('#','') ### URL request does not take # sign
    addresses.append(line)
    if line[-5] == '-':  ### extract 5 digit zip from 9 digits
        zipcodes.append(line[-10:-5])
    else:
        zipcodes.append(line[-5:])
        
destination = '719 Thompson Lane, Nashville, TN 37204' ### 100 oaks addres
mode = 'driving' ### can also take 'transit' or 'walking'
units = 'metric' ### Value of distance is always in meters! Time is in seconds

limit = 40  # limit of addresses per query determined by trial and error (may be character based)

with open('drive2vandy.csv', 'wb') as f:
    writer = csv.writer(f)
    rowcount=0
    addresses = addresses + zipcodes
    output = []
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
        request = request.replace(" ", "_")
        data = json.load(urllib2.urlopen(request))
        print data
        i = 0
        for element in data['rows']:
            status = element['elements'][0]['status']
            if status != 'OK':
                row = [addresses[i],status,status]
            else:
                row = [data['origin_addresses'][i],element['elements'][0]['distance']['value'],element['elements'][0]['duration']['value']]
            output.append(row)
            print output
            writer.writerow(row) 
            rowcount+=1
            i += 1


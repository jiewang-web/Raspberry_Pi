#! /usr/bin/env python

import server_fun

data = server_fun.socket_receive()
#data = '22.34,22.3,55.1'
strlist = data.split(',')
distance = strlist[0]
humidity = strlist[1]
temperature = strlist[2]
#print(temperature)
for value in strlist:
    print (value)

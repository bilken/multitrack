#!/usr/bin/python

import sys
import time
import urllib
import urllib2
import json

import pprint

try:
    appid = sys.argv[1]
except:
    print "Please specify your trimet appID"
    exit(-1)

toWork = {
    13720:{'name':"Max Park"},
    3783:{'name':"Concord and 99"},
    4195:{'name':"Oatfield and Roethe"},
    6211:{'name':"Webster and Thiessen"},
}
toHome = {
    7608:{'name':"Jefferson and 5th", 'lines':[290]},
    3639:{'name':"Madison and 4th", 'lines':[30]},
    7616:{'name':"Market and 5th", 'lines':[99]},
    13776:{'name':'Milwaukie', 'lines':[32]},
}
times = {
    'Work' : toWork,
    'Home' : toHome,
}


def date_to_time(strFull):
    t = strFull[11:19]
    return t

def date_to_day(strFull):
    d = strFull[8:10]
    return d

def get_times(locations):
    csvLocations = ','.join(str(l) for l in locations)
    params = {
        "appID":appid,
        "json":"true",
        "locIDs":csvLocations,
        "arrivals":4,
        "minutes":50,
    }
    args = urllib.urlencode(params)
    url = 'http://developer.trimet.org/ws/V1/arrivals?' + args

    r = urllib2.urlopen(url)
    m = json.load(r)

    today = time.strftime("%d")

    lines = []
    raw_arrivals = m['resultSet']['arrival']
    for a in raw_arrivals:
        id = int(a['locid'])
        loc = locations[id]
        name = loc['name']
        when = "%s (scheduled)" % (date_to_time(a['scheduled']))
        if 'estimated' in a:
            when = date_to_time(a['estimated'])
        d = date_to_day(a['scheduled'])
        if d != today:
            when = 'x%s %s' % (d, when)
        route = a['route']
        if 'lines' in loc and route not in loc['lines']:
            continue
        lines.append("%s: %d at %s" % (when, route, name))

    return sorted(lines)

for k in times:
    print "To %s:" % (k)
    tlist = get_times(times[k])
    for l in tlist:
        print "  %s" % (l)


from typing import Pattern
import requests
import datetime
import re
import json


def list_index_exception_catch(key, value):
    try:
        return value[0].get(key)
    except (IndexError, TypeError):
        return None


async def fetch_resources(userQuery):
    print('q fetch resource: ', userQuery.lower())
    q = userQuery.lower()
    # try:
    #     q1 = q.split('+',1)[1]
    #     print
    # except Exception as e:
    #     print('Exception: ', e)
    #     q1 = None
    my_headers = {'Authorization': 'token 2bf301f9220adcbc665a9b17198ba0b889394121',
                  'Content-Type': 'application/json'}
    stat = None
    tdate = None

    pattern = re.compile(r'(\d\d\d\d-\d\d-\d\d),(\d\d-\d\d-\d\d\d\d)')
    mo = pattern.search(userQuery.lower())
    if mo:
        tdate = mo.group()
        # print('tdate: ', tdate)
    params = {'location': 6875}
    response = requests.get(
        'https://local.veris.in/api/v4/organization/56/resources/list/', headers=my_headers, params=params)
    ty = response.json()
    ty1 = ty.get('results')
    # print('ty1: ',ty1)
    items = []
    for ty2 in ty1:
        rid = ty2.get('id')
        name = ty2.get('name')
        venue1 = ty2.get('ancestors')[0].get('name')
        venue2 = ty2.get('ancestors')[1].get('name')
        venue3 = ty2.get('ancestors')[2].get('name')
        venue = f'{venue1}, {venue2}, {venue3}'
        status = ty2.get('resource_availability_status').get('status')
        venue_type = ty2.get('venue_type')
        if q == "availability":
            if status == "available":
                print('status: ', status)
                dict = {
                    "rid": rid,
                    "name": name,
                    "venue": venue,
                    "status": status,
                    "venue_type": venue_type,
                }
        else:
            dict = {
                "rid": rid,
                "name": name,
                "venue": venue,
                "status": status,
                "venue_type": venue_type,
            }
        items.append(dict)
    dict_items = {
        "resources": items
    }
    # print(items)
    return items


async def resource_details(userQuery):
    print('q_resource: ', userQuery.lower())
    q = userQuery.lower()
    my_headers = {'Authorization': 'token 2bf301f9220adcbc665a9b17198ba0b889394121',
                  'Content-Type': 'application/json'}
    stat = None
    tdate = None

    pattern = re.compile(r'(\d\d\d\d-\d\d-\d\d),(\d\d-\d\d-\d\d\d\d)')
    mo = pattern.search(userQuery.lower())
    if mo:
        tdate = mo.group()
        print('tdate: ', tdate)
    params = {'location': 6875}
    response = requests.get(
        'https://local.veris.in/api/v4/organization/56/resources/list/', headers=my_headers, params=params)
    ty = response.json()
    ty1 = ty.get('results')
    my_date1 = datetime.datetime.now()
    my_date = datetime.datetime.strftime(my_date1, '%Y-%m-%dT%H:%M:%SZ')
    my_iso_date = datetime.datetime.strptime(my_date, '%Y-%m-%dT%H:%M:%SZ')
    items = []
    if next(item for item in ty1 if item["name"] == q):
        abc = next(item for item in ty1 if item["name"] == q)
        # print('index: ', abc)
        rid = abc.get('id')
        am_len = abc.get('amenities')
        id = abc.get('id')
        name = abc.get('name')
        venue_type = abc.get('venue_type')
        amen = []
        for ln in am_len:
            am_name = ln.get('amenity__label')
            am_quantity = ln.get('quantity')
            am_item = {
                "am_name": am_name,
                "am_quantity": am_quantity
            }
            amen.append(am_item)
        venue1 = abc.get('ancestors')[0].get('name')
        venue2 = abc.get('ancestors')[1].get('name')
        venue3 = abc.get('ancestors')[2].get('name')
        venue = f'{venue1}, {venue2}, {venue3}'
        status = abc.get('availability_status').get('status')

        booking1 = abc.get('bookings')
        print("booking f: ", booking1)
        if booking1:
            if booking1[0]:
                bkfm = datetime.datetime.strptime(
                    booking1[0].get('valid_from'), '%Y-%m-%dT%H:%M:%SZ')
                delta = bkfm - my_iso_date
                print('Delta: ', delta)
        bk1 = []
        for bk in booking1:
            items = {
                "valid_from": bk.get('valid_from'),
                "valid_till": bk.get('valid_till'),
                "host_name": bk.get('host_name')
            }
            bk1.append(items)
        next_booking = {
            "next_booking_from": abc.get('availability_status').get('next_booking_from'),
            "next_booking_till": abc.get('availability_status').get('next_booking_till')
        }
        dict = {
            "rid": rid,
            "name": name,
            "venue_type": venue_type,
            "venue": venue,
            "status": status,
            "amenities": amen,
            "bookings": bk1,
            "next_booking": next_booking
        }
    return dict


async def availability_details(userQuery):
    print('q: ', userQuery.lower())
    q = userQuery.lower()
    my_headers = {'Authorization': 'token 2bf301f9220adcbc665a9b17198ba0b889394121',
                  'Content-Type': 'application/json'}
    stat = None
    tdate = None

    pattern = re.compile(r'(\d\d\d\d-\d\d-\d\d),(\d\d-\d\d-\d\d\d\d)')
    mo = pattern.search(userQuery.lower())
    if mo:
        tdate = mo.group()
        print('tdate: ', tdate)
    params = {'location': 6875}
    response = requests.get(
        'https://local.veris.in/api/v4/organization/56/resources/list/', headers=my_headers, params=params)
    ty = response.json()
    ty1 = ty.get('results')
    my_date = datetime.datetime.now()
    my_iso_date = my_date.strptime('%Y-%m-%dT%H:%M:%S.%f%Z')
    items = []
    if next(item for item in ty1 if item["name"] == q):
        abc = next(item for item in ty1 if item["name"] == q)
        # print('index: ', abc)
        am_len = abc.get('amenities')
        id = abc.get('id')
        name = abc.get('name')
        venue_type = abc.get('venue_type')
        amen = []
        for ln in am_len:
            am_name = ln.get('amenity__label')
            am_quantity = ln.get('quantity')
            am_item = {
                "am_name": am_name,
                "am_quantity": am_quantity
            }
            amen.append(am_item)
        venue1 = abc.get('ancestors')[0].get('name')
        venue2 = abc.get('ancestors')[1].get('name')
        venue3 = abc.get('ancestors')[2].get('name')
        venue = f'{venue1}, {venue2}, {venue3}'
        status = abc.get('availability_status').get('status')

        booking1 = abc.get('bookings')
        bkfm = datetime.datetime.strptime(
            booking1[0].get('valid_from'), '%Y-%m-%dT%H:%M:%S.%f%Z')
        delta = bkfm - my_iso_date
        print('Delta: ', delta)
        bk1 = []
        for bk in booking1:
            items = {
                "valid_from": bk.get('valid_from'),
                "valid_till": bk.get('valid_till'),
                "host_name": bk.get('host_name')
            }
            bk1.append(items)
        next_booking = {
            "next_booking_from": abc.get('availability_status').get('next_booking_from'),
            "next_booking_till": abc.get('availability_status').get('next_booking_till')
        }
        dict = {
            "name": name,
            "venue_type": venue_type,
            "venue": venue,
            "status": status,
            "amenities": amen,
            "bookings": bk1,
            "next_booking": next_booking
        }
    return dict


async def book_resource(userQuery):
    my_headers = {'Authorization': 'token 2bf301f9220adcbc665a9b17198ba0b889394121',
                  'Content-Type': 'application/json'}
    print('venue: ', userQuery.bvenue)
    params = {'name': userQuery.bvenue, "location":6875}
    response1 = requests.get(
        'https://local.veris.in/api/v4/organization/56/resources/list/', headers=my_headers, params=params)
    ty = response1.json()
    ty1 = ty.get('results')
    print('query: ', ty1[0]['id'])
    # room = userQuery.
    fdate1 = datetime.datetime.strptime(userQuery.fdate, "%Y-%m-%d %H:%M:%S")
    fdate = datetime.datetime.strftime(fdate1, "%Y-%m-%dT%H:%M:%SZ")
    # print('fdate: ', fdate)
    tdate1 = datetime.datetime.strptime(userQuery.tdate, "%Y-%m-%d %H:%M:%S")
    tdate = datetime.datetime.strftime(tdate1, "%Y-%m-%dT%H:%M:%SZ")
    # print('tdate: ', tdate)
    q = userQuery
    

    # pattern = re.compile(r'(\d\d\d\d-\d\d-\d\d),(\d\d-\d\d-\d\d\d\d)')
    # mo = pattern.search(userQuery.lower())
    # if mo:
    #     tdate = mo.group()
    #     print('tdate: ', tdate)
    params = {'location': 7150}
    body = {
        "guest": [],
        "host": 1072,
        "room": ty1[0]['id'],
        "valid_from": fdate,
        "valid_till": tdate,
        "agenda": "",
        "extra_instructions": "",
        "creation_source": 3,
        "resource_utilization": {
            "percentage": 1,
            "status": 0
        },
        "status": "assigned"
    }
    # print("body: ", json.dumps(body))
    response = requests.post(
        'https://local.veris.in/api/v4/organization/56/bookings/', headers=my_headers, data=json.dumps(body))
    ty = response.json()
    # print('ty: ', ty)
    return ty

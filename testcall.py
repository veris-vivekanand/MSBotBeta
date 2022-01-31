from typing import Pattern
import requests
import datetime
import re

def list_index_exception_catch(key, value):
    try:
        return value[0].get(key)
    except (IndexError, TypeError):
        return None


async def fetch_users(userQuery):
    print('q: ', userQuery.lower())
    my_headers = {'Authorization': 'token 2bf301f9220adcbc665a9b17198ba0b889394121',
                  'Content-Type': 'application/json'}
    stat = None
    tdate = None
    if 'health' in userQuery.lower():
        stat = 2
    elif 'work' in userQuery.lower():
        print('in work')
        stat = 1
    if 'today' in userQuery.lower():
        my_date = datetime.datetime.now()
        tdate = my_date.strftime('%Y-%m-%d')
        print('tdate: ', tdate)
        print(tdate.strftime("%A"))
    elif 'tommorow' in userQuery.lower() or 'tomorrow' in userQuery.lower():
        my_date = datetime.datetime.now() + datetime.timedelta(1)
        tdate = my_date.strftime('%Y-%m-%d')
        print('tdate: ', tdate)
    
    pattern = re.compile(r'(\d\d\d\d-\d\d-\d\d),(\d\d-\d\d-\d\d\d\d)')
    mo = pattern.search(userQuery.lower())
    if mo:
        tdate = mo.group()
        print('tdate: ', tdate)
    # elif mo.group(2):
    #     tdate = mo.group(2)
    #     print('tdate: ', tdate)
    # for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y'):
    #     try:
    #         return datetime.strptime(possible_date, fmt)
    #     except ValueError:
    #         pass
    # raise ValueError(f"Non-valid date format for field {field}: '{possible_date}'")
    params = {'status_type':stat, 'member_id':1072}
    response = requests.get(
        'https://ndl.veris.in/api/v4/organization/56/bulk-member-status/', headers=my_headers, params=params)
    ty = response.json()
    ty1 = ty.get('results')
    # print('result: ', ty1)
    items = []
    if tdate is not None:
        for ty2 in ty1:
            id = ty2.get('id')
            status = ty2.get('status')
            status_type = ty2.get('status_type')
            member = ty2.get('member')
            from_date = ty2.get('from_datetime')
            to_date = ty2.get('to_datetime')
            name = ty2.get('member_info').get('name')
            email = ty2.get('member_info').get('contacts').get('email')
            phone = ty2.get('member_info').get('contacts').get('phone')

            # print('type: ', type(from_date))

            if status_type == 1:
                status_type = 'WORK_STATUS'
            elif status_type == 2:
                status_type = 'HEALTH_STATUS'

            if status == 1:
                status = 'NOT_WORKING'
            elif status == 2:
                status = 'WORK_FROM_HOME'
            elif status == 3:
                status = 'AT_OFFICE'
            elif status == 4:
                status = 'APPROVED_FOR_WORK'
            elif status == 5:
                status = 'NOT_APPROVED_FOR_WORK'

            dict = {
                # "id": id,
                "name": name,
                "from_date":from_date,
                "to_date":to_date,
                # "email": email,
                # "phone": phone,
                "status": status,
                # "status_type": status_type,
                # "member": member,
            }
            if tdate in from_date:
                items.append(dict)
    else:
        for ty2 in ty1:
            id = ty2.get('id')
            status = ty2.get('status')
            status_type = ty2.get('status_type')
            member = ty2.get('member')
            from_date = ty2.get('from_datetime')
            to_date = ty2.get('to_datetime')
            name = ty2.get('member_info').get('name')
            email = ty2.get('member_info').get('contacts').get('email')
            phone = ty2.get('member_info').get('contacts').get('phone')

            # print('type: ', type(from_date))

            if status_type == 1:
                status_type = 'WORK_STATUS'
            elif status_type == 2:
                status_type = 'HEALTH_STATUS'

            if status == 1:
                status = 'NOT_WORKING'
            elif status == 2:
                status = 'WORK_FROM_HOME'
            elif status == 3:
                status = 'AT_OFFICE'
            elif status == 4:
                status = 'APPROVED_FOR_WORK'
            elif status == 5:
                status = 'NOT_APPROVED_FOR_WORK'

            dict = {
                # "id": id,
                "name": name,
                "from_date":from_date,
                "to_date":to_date,
                # "email": email,
                # "phone": phone,
                "status": status,
                # "status_type": status_type,
                # "member": member,
            }

            items.append(dict)
    dict_items = {
        "items": items
    }
    return items

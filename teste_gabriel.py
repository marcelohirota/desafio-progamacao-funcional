from datetime import datetime
from operator import itemgetter

records = [
    {'source': '48-996355555', 'destination': '48-666666666', 'end': 1564610974, 'start': 1564610674},
    {'source': '41-885633788', 'destination': '41-886383097', 'end': 1564506121, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-886383097', 'end': 1564630198, 'start': 1564629838},
    {'source': '48-999999999', 'destination': '41-885633788', 'end': 1564697158, 'start': 1564696258},
    {'source': '41-833333333', 'destination': '41-885633788', 'end': 1564707276, 'start': 1564704317},
    {'source': '41-886383097', 'destination': '48-996384099', 'end': 1564505621, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '48-996383697', 'end': 1564505721, 'start': 1564504821},
    {'source': '41-885633788', 'destination': '48-996384099', 'end': 1564505721, 'start': 1564504821},
    {'source': '48-996355555', 'destination': '48-996383697', 'end': 1564505821, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '41-886383097', 'end': 1564610750, 'start': 1564610150},
    {'source': '48-996383697', 'destination': '41-885633788', 'end': 1564505021, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-885633788', 'end': 1564627800, 'start': 1564626000}
]


def classify_by_phone_number(records):
    arr = []
    for dic in records:
        result = calculate_total_price(dic, arr)
        if type(result) == dict:
            arr.append(result)

    answer = sorted(arr, key=itemgetter('total'), reverse=True)

    print(f'Answer: {answer}')
    return answer


def calculate_total_price(dic, arr):
    end = datetime.utcfromtimestamp(dic['end']).strftime("%H %M %S")
    start = datetime.utcfromtimestamp(dic['start']).strftime("%H %M %S")

    equivalent_seconds_start = (int(start[0:2])*60*60) + (int(start[6:])) + (int(start[3:5])*60)
    equivalent_seconds_end = (int(end[0:2])*60*60) + (int(end[6:])) + (int(end[3:5])*60)

    price = apply_rules(dic, equivalent_seconds_end, equivalent_seconds_start)

    if(len(arr) > 0):
        for i in range(len(arr)):
            if dic['source'] == arr[i]['source']:
                return add_to_a_existing_dict(dic, price, i, arr)
        return create_new_dict(dic, price)
    else:
        return create_new_dict(dic, price)


def add_to_a_existing_dict(dic, price, i, arr):
    arr[i]['total'] = round(arr[i]['total'] + price, 2)

    return arr[i]['total']


def create_new_dict(dic, price):
    total = round(price, 2)
    dic_total = {'source': dic['source'], 'total': total}

    return dic_total


def apply_rules(dic, equivalent_seconds_end, equivalent_seconds_start):
    switch_price_night = 22 * 60 * 60
    switch_price_day = 6 * 60 * 60
    if equivalent_seconds_start > switch_price_day and equivalent_seconds_start < switch_price_night:
        price_to_pay = 0.36 + (min(abs(equivalent_seconds_end-equivalent_seconds_start), abs(switch_price_night - equivalent_seconds_start))//60)*0.09

    elif equivalent_seconds_start > switch_price_night or equivalent_seconds_start < switch_price_day:
        unpaid = min(abs(equivalent_seconds_end-equivalent_seconds_start), abs(switch_price_day-equivalent_seconds_start))
        if(unpaid == equivalent_seconds_end-equivalent_seconds_start):
            price_to_pay = 0.36
        else:
            price_to_pay = 0.36 + (((equivalent_seconds_end - equivalent_seconds_start)-unpaid)//60)*0.09

    return price_to_pay


classify_by_phone_number(records)
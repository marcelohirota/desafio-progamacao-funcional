from datetime import datetime
import pandas as pd

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

# Calculo do custo por ligação
def call_fee (start_time, end_time):
    
    start_time = datetime.fromtimestamp(start_time)
    end_time = datetime.fromtimestamp(end_time)

    if (int(start_time.hour) >= 6) and (int(end_time.hour) <= 22):
        fee = 0.36 + (((end_time - start_time).seconds//60)*0.09)
        return float(fee)
    else:
        return 0.36

# Adição da coluna 'cost' dentro do records
def get_costs(records):
    for calls in records:
        calls.update({'cost': call_fee(calls['start'], calls['end'])})
    return records

def classify_by_phone_number(records):
    
    final_results = []

    df_results = pd.DataFrame(get_costs(records))

    group_results = df_results.groupby('source')['cost'].sum().reset_index().rename(columns={'cost':'total_cost'})\
        .sort_values(by='total_cost', ascending=False)

    sources = [source for source in group_results['source']]

    totals = [total for total in group_results['total_cost']]

    for results in zip(sources, totals):
        final_results.append({'source': results[0], 'total_cost': round(results[1],2)})

    return final_results








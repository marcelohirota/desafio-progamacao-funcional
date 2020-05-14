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

# Calculo tarifa diurna
def dayFee(start_time,end_time):
    return 0.36 + (((end_time - start_time).seconds//60)*0.09)

# Calculo do custo por ligação
def call_fee (start_time, end_time):
    
    start_time = datetime.fromtimestamp(start_time)
    end_time = datetime.fromtimestamp(end_time)

    # Ligações com tarifa diurna
    if start_time.hour > 6 and end_time.hour < 22:
        return float(dayFee(start_time, end_time))

    # Ligações com tarifa noturna
    elif ((start_time.hour >= 22 and end_time.hour >= 22) or (start_time.hour < 6 and end_time.hour < 6)):
        return 0.36

    # Tarifa mista
    else: 
        if (end_time.hour >= 22, end_time.minute >=1):
            end_time = datetime(end_time.year, end_time.month, end_time.day, hour=22, minute=00, second=59)

        if (start_time.hour < 6):
            start_time = datetime(start_time.year, start_time.month, start_time.day, hour=6)

        mix_fee = dayFee(start_time, end_time) + 0.36
        return mix_fee
        

# Adição da coluna 'cost' dentro do records
def get_costs(records):
    for calls in records:
        calls.update({'cost': call_fee(calls['start'], calls['end'])})
    return records

def classify_by_phone_number(records):
    
    final_results = []

    df_results = pd.DataFrame(get_costs(records))

    ordered_results = df_results.groupby('source')['cost'].sum().reset_index().rename(columns={'cost':'total'}).sort_values(by='total', ascending=False)

    sources = ordered_results['source'].values.tolist()

    totals = ordered_results['total'].values.tolist()

    for results in zip(sources, totals):
        final_results.append({'source': results[0], 'total': round(results[1],2)})

    return final_results
    print(f'Final results: {final_results}')


test = classify_by_phone_number(records)
print(test)





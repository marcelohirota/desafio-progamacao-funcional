from datetime import datetime
import math

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
    lista = calcular_sumarizado(records)
    
    lista = sorted(lista, key=lambda k: k['total'], reverse = True) 

    print(f'Lista: {lista}')
    return lista


def calcular_individual(records):

  retorno = []

  hora_limitI = datetime.strptime('22:00:00', '%H:%M:%S')
  hora_limitF = datetime.strptime('06:00:00', '%H:%M:%S')

  for registro in records:
      
      total = 0
      end = datetime.fromtimestamp(registro['end'])
      start = datetime.fromtimestamp(registro['start'])
      FMT = '%Y-%m-%d %H:%M:%s'

      if  start.strftime('%H:%M:%S') > hora_limitI.strftime('%H:%M:%S'):
          #print(f'Inicio_Noturno: {start}')
          total = 0.36
          #print(total)
      elif start.strftime('%H:%M:%S') < hora_limitF.strftime('%H:%M:%S'):
          #print(f'Inicio_Noturno: {start}')
          total = 0.36
          #print(total)
      else:
          #print(f" \nInicio_Diurno: {start}")
          if end.strftime('%H:%M:%S') < hora_limitI.strftime('%H:%M:%S'):
              #print(f'Fim_Diurno: {end}')
              tempo = ( registro['end'] - registro['start'] ) / 60
              total = round( 0.36 + (tempo * 0.09), 2)
              #print(total)
          else:
              #print(f'Fim_Noturno: {end}')
              
              calc = ( datetime.strptime(hora_limitI.strftime('%H:%M:%S'), FMT) - datetime.strptime(start.strftime('%H:%M:%S'), FMT) )
              tempo = calc.seconds/60
              total = round( 0.36 + (tempo * 0.09), 2)
              #print(f'Tarifa: {tarifa}')
          #print('\n')

      retorno.append({'source': registro['source'], 'total': total})
                  
  return retorno


def calcular_sumarizado(records):  
  calculado_individual = calcular_individual(records)
 
  calculado_final = []

  for individual in calculado_individual:
    #print(individual['source'])
    
    if(len(calculado_final) == 0):
      calculado_final.append({'source':individual['source'], 'total':individual['total']})
    else:
      cont = 0
      for item in calculado_final:
          if(individual['source'] is item['source'] ):          
            item['total'] = item['total'] + individual['total']
            cont = 1     
            break 
          
                    
      if( cont == 0):     
        calculado_final.append({'source':individual['source'], 'total':individual['total']})
              
  return calculado_final

classify_by_phone_number(records)
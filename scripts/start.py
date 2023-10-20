from datetime import date
from . import refresh 

def run():
    today = date.today()
    # Definim el where
    t_date = today.strftime('%Y-%m-%d') + 'T00:00:00'
    refresh.getEventsDadesObertes("data_inici>='" + t_date + "'")
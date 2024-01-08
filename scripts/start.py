from datetime import date
from scripts import refresh

def run():
    today = date.today()
    # Definim el where
    t_date = today.strftime('%Y-%m-%d') + 'T00:00:00'
    refresh.get_events_dades_obertes("data_inici>='" + t_date + "'")
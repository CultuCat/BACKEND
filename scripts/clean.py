import psycopg2

# Conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
    database='cultucatbd',
    user='postgres',
    password='pes04',
    host="34.31.77.244",
    port='5432'
)
cursor = conn.cursor()

# Ejecutar una consulta SQL para reemplazar "&nbsp;" por un espacio en blanco
update_query = """
    UPDATE events_event
    SET descripcio = REPLACE(descripcio, '&nbsp;', '')
    WHERE descripcio LIKE '%&nbsp;%';

    UPDATE events_event
    SET preu = REPLACE(preu, '&nbsp;', '')
    WHERE preu LIKE '%&nbsp;%';

    UPDATE events_event
    SET descripcio = regexp_replace(descripcio, '\s+', ' ', 'g')
    WHERE descripcio ~ '\s+';

"""

cursor.execute(update_query)

# Commit y cierre de la conexión
conn.commit()
conn.close()
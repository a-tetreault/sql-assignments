import psycopg2
import hidden
import requests
import json

# Load the secrets
secrets = hidden.secrets()

conn = psycopg2.connect(host=secrets['host'],
        port=secrets['port'],
        database=secrets['database'],
        user=secrets['user'],
        password=secrets['pass'],
        connect_timeout=10)

cur = conn.cursor()

print('If you want to restart the spider, run')
print('DROP TABLE IF EXISTS pokeapi CASCADE;')
print(' ')

sql = '''
CREATE TABLE IF NOT EXISTS pokeapi
(id serial, body JSONB);
'''
print(sql)
cur.execute(sql)
for i in range(1,101):
    url = f'https://pokeapi.co/api/v2/pokemon/{i}'
    print('=== Url is', url)
    response = requests.get(url)
    if response.status_code == 200:
        body = response.json()
        cur.execute('INSERT INTO pokeapi (body) VALUES (%s);', (json.dumps(body),))
print('Closing database connection...')
conn.commit()
cur.close()
conn.close()


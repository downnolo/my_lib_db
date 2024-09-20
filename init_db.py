import psycopg2

conn = psycopg2.connect(database="lib_db", host="localhost", user="postgres", password="admin")

cur  = conn.cursor()

cur.execute(''' SELECT * from story ''')
data = cur.fetchall()
print(data)
conn.commit()
cur.close()
conn.close()



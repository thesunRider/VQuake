import sqlite3 
import pandas


INSERT = ''' INSERT INTO  ip_filter (start,first,last) VALUES (?,?,?)'''

conn = sqlite3.connect('filtered.db')
conn.execute('''CREATE TABLE IF NOT EXISTS ip_filter
             (start int ,first int ,last int )''')

df= pandas.read_csv('db/tor_filter.csv')
df.sort_values(by='first')

df.to_sql("tor_filter",conn)

conn.close()

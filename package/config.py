import mysql.connector


my_db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="data_scrape"
)

my_cursor = my_db.cursor()


from bs4 import BeautifulSoup
import requests
import mysql.connector
import config
import datetime

# Create variables
source = "Wings"
ct = datetime.datetime.now()

# Fetch mortgage rates
URL = "https://www.wingsfinancial.com/rates/mortgages-purchase"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
table = soup.find_all('td')

fr30 = float(str(table[0])[4:9])
fr30pt = float(str(table[2])[4:6])
ARM71 = float(str(table[25])[4:9])
ARM71pt = float(str(table[7])[4:6])

# Connect to database
db = mysql.connector.connect(
    host = config.host,
    user = config.user,
    password = config.pw,
    database = config.db
)
cursor = db.cursor()

# Write to database
sql = "INSERT INTO `daily_rates` (source, timestamp, 30_year_fixed_rate, 30_year_fixed_points, 71_arm_rate,71_arm_point) VALUES (%s,%s,%s,%s,%s,%s)"
val = (source,ct,fr30,fr30pt,ARM71,ARM71pt)
cursor.execute(sql,val)

db.commit()

# Close database connection
cursor.close()
db.close()


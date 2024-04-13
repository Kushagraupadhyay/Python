import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv 

load_dotenv()
config = {
  'host': os.getenv('DB_HOST'),
  'user': os.getenv('DB_USER'),
  'password': os.getenv('DB_PASSWORD'),
  'database': os.getenv('DB_NAME')
}

# Construct connection string

try:
   conn = mysql.connector.connect(**config)
   print("Connection established")
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with the user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cursor = conn.cursor()

## Drop previous table of same name if one exists
#cursor.execute("DROP TABLE IF EXISTS pcmsmapping")
#print("Finished dropping table (if existed).")
#
#  ## Create Table
#
#cursor.execute("""
#      CREATE TABLE pcmsmapping (
#               engineerAlias VARCHAR(255) NOT NULL PRIMARY KEY,
#               alignedEngineerAlias VARCHAR(255) NOT NULL          
#      );""")
#
#print("Finished creating table.")
#
#  
## Insert data into table
#
#cursor.execute("""
#               INSERT INTO pcmsmapping (
#               engineerAlias, 
#               alignedEngineerAlias
#               ) VALUES (%s, %s)""",
#               (
#                'sugamgupta','girishshet,v-chicreddy,v-himchauhan,v-astasneem,v-jadhavpra,mahaleamol,v-rabishek,v-sviswanth,v-fashariff,v-jkhare,v-srahul1,v-vjaina,kuupadh,pravinraju,simranbodhak,sugamgupta' 
#               )
#              )
#print("Data inserted into table.")

# Cleanup
conn.commit()
cursor.close()
conn.close()
print("Done.")
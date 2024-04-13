import pandas as pd
import os
from dotenv import load_dotenv 
import re
import numpy as np
from io import StringIO
import lxml
from sqlalchemy import create_engine
import mysql.connector
from mysql.connector import errorcode

# Read data from a file
file_path = "C:/Users/kuupadh/Downloads/emailData"

with open(file_path,'r') as f:
    email_data = f.read()

email_data_io = StringIO(email_data)
tables = pd.read_html(email_data_io)

# concatenate all the tables into a single dataframe
all_tables = pd.concat(tables)

# Assuming 'all_tables' is your DataFrame and 'CaseCreatedTime' is the column with the date and time
all_tables['CaseCreatedTime'] = pd.to_datetime(all_tables['CaseCreatedTime'], format='%m/%d/%Y %I:%M:%S %p')
all_tables['CaseCreatedTime'] = all_tables['CaseCreatedTime'].dt.strftime('%Y-%m-%d %H:%M:%S')
all_tables['LastPCMSReview'] = pd.to_datetime(all_tables['LastPCMSReview'], format='%m/%d/%Y %I:%M:%S %p')
all_tables['LastPCMSReview'] = all_tables['LastPCMSReview'].dt.strftime('%Y-%m-%d %H:%M:%S')
all_tables['LastModifiedTime'] = pd.to_datetime(all_tables['LastModifiedTime'], format='%m/%d/%Y %I:%M:%S %p')
all_tables['LastModifiedTime'] = all_tables['LastModifiedTime'].dt.strftime('%Y-%m-%d %H:%M:%S')

# changing 354.2 days to 354.2 in 'CaseAge' column
all_tables['CaseAge'] = all_tables['CaseAge'].str.replace(' days', '')
all_tables.loc[all_tables['CaseAge'].str.contains('hours'),'CaseAge'] = all_tables['CaseAge'].str.replace('hours','').astype(float)/24
all_tables['CaseAge'] = all_tables['CaseAge'].astype(float).round(1) # rounding off case age to nearest integer
all_tables['CaseIdle'] = all_tables['CaseIdle'].str.replace(' days', '')
all_tables.loc[all_tables['CaseIdle'].str.contains('hours'),'CaseIdle'] = all_tables['CaseIdle'].str.replace('hours','').astype(float)/24
all_tables['CaseIdle'] = all_tables['CaseIdle'].astype(float).round(1) # rounding off case idle to nearest integer

# replacing NaN values 
all_tables['LastPCMSReview']=all_tables['LastPCMSReview'].fillna('1970-01-01 00:00:00') 
all_tables['CsatRiskReasonText'] = all_tables['CsatRiskReasonText'].fillna('No Reason Provided')
all_tables['LastPCMSReviewBy'] = all_tables['LastPCMSReviewBy'].fillna('NotReviewedYet')
all_tables['InternalTitle'] = all_tables['InternalTitle'].fillna('NoInternalCaseTitle')
all_tables['OwnershipCount'] = all_tables['OwnershipCount'].fillna(0)
all_tables['ServiceLevel2'] = all_tables['ServiceLevel2'].fillna('NA')
all_tables['ServiceLevel'] = all_tables['ServiceLevel'].fillna('NA')

#Adding review range columns
all_tables['TimeSinceLastReview'] = (pd.Timestamp.now() - pd.to_datetime(all_tables['LastPCMSReview'])).dt.days 
all_tables.loc[all_tables['TimeSinceLastReview']>10000, 'TimeSinceLastReview'] = all_tables['CaseAge'].astype('int64') # setting the value to 0 if the value is greater than 10000
all_tables['LessThan7Days'] = (all_tables['TimeSinceLastReview'] < 7).astype(int)
all_tables['Between7And21Days'] = (all_tables['TimeSinceLastReview'].between(7,21)).astype(int)
all_tables['MoreThan21Days'] = (all_tables['TimeSinceLastReview'] > 21).astype(int)

# Adding tag & $$ processing
tag_values = {'(OnTrack)': 'On Track', '(NOT)':'Not On Track', '(CPE)':'Customer partner experience is gone for toss or in compromised state', '(Outage)':'Outage related incident', '(SolDel)':'Solution Delivered', '(MREC) ':'Manager recovery', '(TREC) ':'Technical recovery', '(REC)':'Case is pending on recovery', '(Archive)':'3rd strike process/archival process', '(Closure)':'pending closure ','(Close)':'pending closure ', '(DTS)':'DTS already created', '(EEE)':'EEE are engaged ', '(PG)':'Case pending/driven at PG level', '(Admin)':'M1 discussion before closure', '(Eng-OT)':'Case is pending on the Engineer where they are researching, analyzing logs or reproducing the issue and the case is on track.', '(ENG-NOT)':'Case is pending on engineer and it needs attention', '(Cx-OT)':'Case is pending on cx (waiting for logs or responses) and the case is on track', '(Cx-NOT)':'Case is pending on cx (waiting for logs or responses) and is not on track (idle, unresponsive cx etc)', '(PG-OT)':'Case is pending on PG team and is on track', '(PG-NOT)':'Case is pending on PG team but would need follow-ups to the PG team (Ideal candidates to be brought to PG team’s attention)', '(Oth-OT)':'Case is pending on other teams and is on track', '(Oth-NOT)':'Case is pending on other teams and is not on track', '(TA-OT)':'Case is pending on TA/Escalation and is on track', '(TA-NOT)':'Case is pending on TA/Escalation and is not on track', '(IM-OT)':'Case is pending on IM/CSAM/CSA engagement and is on track', '(IM-NOT)':'Case is pending on IM/CSAM/CSA engagement and is not on track', '(BCD: Name)' :'Buddy Connect Done', '(SME: Name)' : 'Subject Matter Expert Engaged', '(Collab: TeamName)' :'Cases pending on collab team', '(OX: TeamName)' :'Case needs to be transferred to different team (ownership transfer)'}
all_tables['CurrentStatusTag'] = all_tables['InternalTitle'].apply(lambda x: ' '.join([tag_values[tag] for tag in tag_values if tag.lower() in x.lower()])) # applying tag values to the column 'InternalTitle' and storing the result in 'CurrentStateTag'
all_tables['CurrentStatusTag']= all_tables['CurrentStatusTag'].replace('','No Tag - Tag updation required')

def find_dollar_text(s):
   matches = re.findall(r'\$(.*?)\$',s)
   return ''.join(matches)

all_tables['CurrentStatusTag']+= ' ' + all_tables['InternalTitle'].apply(find_dollar_text)


# adding a column to check if review is needed or not
all_tables['ReviewNeeded'] = all_tables['TimeSinceLastReview'].apply(lambda x: 'Yes' if x==0 or x>10 else 'No') 

# function to export the table as CSV
#all_tables.to_csv("C:/Users/kuupadh/Downloads/emailData.csv")

#function to print the table
#for table in tables:
#    print(table)

# Obtain connection string information from the portal
# Load environment variables from .env file
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

# Drop previous table of same name if one exists
cursor.execute("DROP TABLE IF EXISTS pcmsdata;")
print("Finished dropping table (if existed).")

## Create table
cursor.execute("""
CREATE TABLE pcmsdata (
    id SERIAL PRIMARY KEY,
    Tools VARCHAR(255),
    IncidentNumber BIGINT,
    CaseCreatedTime DATETIME,
    IncidentState VARCHAR(255),
    OwnerAlias VARCHAR(255),
    OwnershipCount INTEGER,
    OwnerCompanyName VARCHAR(255),
    CustomerCountry VARCHAR(255),
    CaseAge INTEGER,
    CaseIdle INTEGER,
    ServiceLevel2 VARCHAR(255),
    InternalTitle VARCHAR(255),
    OwnerM1Alias VARCHAR(255),
    IsPCMSReviewed VARCHAR(255),
    LastPCMSReview DATETIME,
    LastPCMSReviewBy VARCHAR(255),
    CurrentSeverity VARCHAR(255),
    IsStrategicFlag VARCHAR(255),
    LastModifiedTime TIMESTAMP,
    OwnerM2Alias VARCHAR(255),
    CsatRiskProbability INTEGER,
    CsatAtRisk VARCHAR(255),
    CsatRiskReasonText VARCHAR(1000),
    IncidentStatus VARCHAR(255),
    ServiceLevel VARCHAR(255),
    SAPPath VARCHAR(255),
    ServiceName VARCHAR(255),
    TimeSinceLastReview INTEGER,
    LessThan7Days INTEGER,
    Between7And21Days INTEGER,
    MoreThan21Days INTEGER,
    CurrentStatusTag VARCHAR(255),
    ReviewNeeded VARCHAR(255)
);
""")
print("Finished creating table.")

# Insert data into table
for i,row in all_tables.iterrows():
    cursor.execute("""INSERT INTO pcmsdata (
                   Tools, 
                   IncidentNumber, 
                   CaseCreatedTime, 
                   IncidentState, 
                   OwnerAlias, 
                   OwnershipCount, 
                   OwnerCompanyName, 
                   CustomerCountry, 
                   CaseAge, 
                   CaseIdle, 
                   ServiceLevel2, 
                   InternalTitle, 
                   OwnerM1Alias, 
                   IsPCMSReviewed, 
                   LastPCMSReview, 
                   LastPCMSReviewBy, 
                   CurrentSeverity, 
                   IsStrategicFlag, 
                   LastModifiedTime, 
                   OwnerM2Alias, 
                   CsatRiskProbability, 
                   CsatAtRisk, 
                   CsatRiskReasonText, 
                   IncidentStatus, 
                   ServiceLevel, 
                   SAPPath,
                   ServiceName,
                   TimeSinceLastReview,
                   LessThan7Days,
                   Between7And21Days,
                   MoreThan21Days,
                   CurrentStatusTag,
                   ReviewNeeded
                   ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s , %s, %s, %s, %s, %s, %s)""", 
                   (
                      row.Tools , 
                      row.IncidentNumber , 
                      row.CaseCreatedTime	, 
                      row.IncidentState , 
                      row.OwnerAlias , 
                      row.OwnershipCount , 
                      row.OwnerCompanyName , 
                      row.CustomerCountry	, 
                      row.CaseAge , 
                      row.CaseIdle , 
                      row.ServiceLevel2 , 
                      row.InternalTitle , 
                      row.OwnerM1Alias , 
                      row.IsPCMSReviewed , 
                      row.LastPCMSReview , 
                      row.LastPCMSReviewBy , 
                      row.CurrentSeverity	, 
                      row.IsStrategicFlag	, 
                      row.LastModifiedTime , 
                      row.OwnerM2Alias , 
                      row.CsatRiskProbability	, 
                      row.CsatAtRisk , 
                      row.CsatRiskReasonText, 
                      row.IncidentStatus , 
                      row.ServiceLevel , 
                      row.SAPPath ,
                      row.ServiceName	,
                      row.TimeSinceLastReview,
                      row.LessThan7Days,
                      row.Between7And21Days,
                      row.MoreThan21Days,
                      row.CurrentStatusTag,
                      row.ReviewNeeded
                      ))
print("Data inserted into table.")

## Cleanup
conn.commit()
cursor.close()
conn.close()
print("Done.")
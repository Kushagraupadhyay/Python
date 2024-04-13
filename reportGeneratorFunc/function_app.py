import azure.functions as func
import logging
import mysql.connector
from mysql.connector import errorcode
import smtplib
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart
from getpass import getpass
import os
from dotenv import load_dotenv 

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="http_trigger_report_generator_to_email_buddy_mapping")
def http_trigger_report_generator_to_email_buddy_mapping(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    load_dotenv()
    # SMTP server setup
    smtp_host = "smtp.office365.com"
    smtp_port = 587
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')
    
    # Obtain connection string information from the portal
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
    
    # Get all entries from pcmsmapping table
    cursor.execute("SELECT * FROM pcmsmapping")
    rows = cursor.fetchall()
    
    # Create a list of dictionaries to store the mapping data where alignedEngineerAlias is a list inside the dictonary
    mapping_data = []
    for row in rows:
      mapping_data.append({
        'engineerAlias': row[0],
        'alignedEngineerAlias': row[1].split(',')
      })
    
    #print(mapping_data)
    
    for each_mapping in mapping_data:
      engineer_alias = each_mapping['engineerAlias']
      aligned_engineer_alias = each_mapping['alignedEngineerAlias']
      email_body = ''
      # Get all entries from pcmsdata table where OwnerAlias is engineer_alias
      for each_aligned_engineer_alias in aligned_engineer_alias:
        cursor.execute(f"""SELECT IncidentNumber,IsStrategicFlag,ReviewNeeded,LastPCMSReviewBy,CurrentStatusTag,TimeSinceLastReview,CaseIdle,CaseAge,IncidentStatus,InternalTitle,SAPPath,OwnerAlias
                       FROM pcmsdata 
                       WHERE OwnerAlias = '{each_aligned_engineer_alias}'
                       ORDER BY TimeSinceLastReview DESC
                       """)
        case_rows = cursor.fetchall()
    
        # Start a new table for each alignedEngineerAlias
        email_body += """
                  <style>
                  @import url(https://fonts.googleapis.com/css?family=Open+Sans:400,600);
    
                  *, *:before, *:after {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                  }
                  
                  body,h2 {
                    background: #105469;
                    font-family: 'Open Sans', sans-serif;
                  }
                  table {
                    background: #012B39;
                    border-radius: 0.25em;
                    /* border-collapse: collapse ; */
                    margin: 1em; 
                    border: 2px solid black;  
                    font-size: 0.9em;
                  }
                  th,td {
                    border-bottom: 1px solid black;
                    border : 1px solid black;
                    color: #E2B842;
                    font-size: 0.95em;
                    font-weight: 600;
                    padding: 0.3em 0.5em;
                    text-align: center;
                  }
                  td {
                    color: #fff;
                    font-weight: 400;
                  }
                  </style>
                  """
        email_body += f"<h3>Case List for : {each_aligned_engineer_alias}</h3>"
        email_body += "<table><tr><th>IncidentNumber</th><th>IsStrategicFlag</th><th>ReviewNeeded</th><th>LastPCMSReviewBy</th><th>CurrentStatusTag</th><th>TimeSinceLastReview</th><th>CaseIdle</th><th>CaseAge</th><th>IncidentStatus</th><th>InternalTitle</th><th>SAPPath</th><th>OwnerAlias</th></tr>"
    
        # Add each case row to the table
        for each_case_row in case_rows:
          casebuddy_hyperlink = f"mscb:review?{each_case_row[0]}"
          review_needed = each_case_row[2]
          if review_needed == 'Yes':
            review_needed = f"<td style='color: red; font-weight: bold;'>{review_needed}</td>"
          else:
            review_needed = f"<td style='color: green;'>{review_needed}</td>"
          strategic_flag = each_case_row[1]
          if strategic_flag == 'Yes':
            strategic_flag = f"<td style='color: green;'>{strategic_flag}</td>"
          else:
            strategic_flag = f"<td>{strategic_flag}</td>"
          email_body += f"<tr><td><a href='{casebuddy_hyperlink}'>{each_case_row[0]}</a></td>{strategic_flag}{review_needed}<td>{each_case_row[3]}</td><td>{each_case_row[4]}</td><td>{each_case_row[5]}</td><td>{each_case_row[6]}</td><td>{each_case_row[7]}</td><td>{each_case_row[8]}</td><td>{each_case_row[9]}</td><td>{each_case_row[10]}</td><td>{each_case_row[11]}</td></tr>"
          
        email_body += "</table>"
    
      #print(email_body) 
      # Send email
      msg = MIMEMultipart('alternative')
      msg['Subject'] = 'Daily case review Report'
      msg['From'] = smtp_user
      msg['To'] = f"{engineer_alias}@microsoft.com"
      part1 = MIMEText(email_body, 'html')
      msg.attach(part1)
    
      s = smtplib.SMTP(host=smtp_host, port=smtp_port)
      s.starttls()
      s.login(smtp_user, smtp_password)
      s.send_message(msg)
      s.quit()
      print(f"Email sent to {engineer_alias}")
    
    ## Cleanup
    conn.commit()
    cursor.close()
    conn.close()
    print("Done.")

    return func.HttpResponse(
             "This HTTP triggered function executed successfully. Email reports sent to all SMEs ",
             status_code=200
        )
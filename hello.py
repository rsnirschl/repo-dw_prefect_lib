import env_vars
from prefect import flow, task
from datetime import date
from prefect_dbt.cloud import DbtCloudJob
from prefect_dbt.cloud import DbtCloudCredentials
from prefect_dbt.cloud.jobs import run_dbt_cloud_job, trigger_dbt_cloud_job_run_and_wait_for_completion
from prefect_dbt.cloud.models import TriggerJobRunOptions
from prefect import variables
from prefect import flow

import smtplib
from json import dumps
import pprint

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Import the email modules we'll need
from email.message import EmailMessage

#job variables:
vJob_Combined_Message = ""
vJob_Count_After = 0
vJob_Count_Before = 0	
vJob_Current_Date = date.today()	
vJob_Date = date.today()	
vJob_DBT_Run_Completed = ""
vJob_Job_Names = ""	
vJob_job_start = ""	 
vJob_Row_Count = 0
vJob_Run_Type = ""
vJob_Success_Failure = ""

#grid variables:
vJob_Row_Count_Rows = ""

@flow
def Macs_Import():
    print('starting macs import')
    Snowflake_Copy_Into()
    if (Get_Row_Count()):
        Log_Success_Message()
    #Run_DBT_Cloud_Job(env_vars.vEnv_Dbt_Job_ID)
    dbt_creds = DbtCloudCredentials.load(env_vars.vEnv_DBT_Credential_Block)
    dbt_cloud_job = DbtCloudJob(dbt_cloud_credentials=dbt_creds, job_id =env_vars.vEnv_Dbt_Job_ID)
    dbt_cloud_job_run = dbt_cloud_job.trigger()
    dbt_cloud_job_run.wait_for_completion()
    dbt_result = dbt_cloud_job_run.fetch_result()
    #print(dbt_result)
    #print(dbt_cloud_job_run.get_status_code())
    #print(dbt_cloud_job_run.get_run())
    Send_HTML_Email('rnirschl@mutualofenumclaw.com','Prefect Run Result:' + env_vars.vEnv_Dbt_Job_ID,pprint.pformat(dbt_result))

 #   run_result = trigger_dbt_cloud_job_run_and_wait_for_completion(
 #       dbt_cloud_credentials=dbt_creds,
 #       job_id=env_vars.vEnv_Dbt_Job_ID,
 #       trigger_job_run_options=TriggerJobRunOptions(
 #           timeout_seconds_override=10)
 #  )
    #print(run_result["status"])

@flow
def Heritage_Import():
    print("heritage import")

@task
def Snowflake_Copy_Into():
    print("copy into")

@task
def Get_Row_Count():
    print("get row count")
    return True

@task
def Log_Success_Message():
    print("log success message")
    vJob_Combined_Message = ""

    def listKey1(e):
        return e[0]
    t = "S3 Load History\n"
    t = t + "File Date\tNew Rows\tReport Date\n"
    vJob_Row_Count = 0
  
    if vJob_Row_Count > 0:
## use v to sort the result set
        v = vJob_Row_Count_Rows
        v.sort(key=listKey1, reverse=True)
  
        for l in v:
            d = l[0]
            r = l[1]
            t = t + str(d) + "\t" + str(r) + "\t" + str(l[2])
            t = t + "\n"
            vJob_Row_Count += 1

#t = " Balances Summary:<br>Count: " + str(vJob_Row_Count) + "<br>" + t
    vJob_Combined_Message = t
    #print(vJob_Row_Count)
    #print(len(t))

    print(vJob_Combined_Message)
    vJob_Success_Failure = "Success"

@task
def Run_DBT_Cloud_Job(job_ID):
    print("running dbt cloud job: " + job_ID)
    #print(DbtCloudCredentials.load("dbt-cloud-creds"))

@task
def Send_Email(recipient, subject, body):
    email_address = recipient

    msg = EmailMessage()
    msg['Subject'] = subject
    msg.set_content(body)
    msg['From'] = 'prefect-dw@mutualofenumclaw.com'
    msg['To'] = email_address

# Send the message via our own SMTP server.
    s = smtplib.SMTP(host='prdsmtp01.mutualofenumclaw.net', port=25)
    s.send_message(msg)
    s.quit()

@task
def Send_HTML_Email(recipient, subject, body):
    link = 'https://app.sigmacomputing.com/mutual-of-enumclaw/workbook/workbook-4TQMro542rzIR7REgZOfmO?:explore=92e4cb1c-0b1c-4b61-87b3-46d56524b7b9'
# Prep the recipient list by stripping unneeded characters
# and converting to a comma separated string
# then create a Python list by splitting on the comma
    recipient_list = recipient.rstrip().replace(';', ',')

    if recipient_list.endswith(','):
        recipient_list = recipient_list[:-1]

    recip_list = recipient_list.split(",")
# me == my email address
# you == recipient's email address
    me = 'prefect-dw@mutualofenumclaw.com'
    you = recip_list

# Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = recipient_list

# Create the body of the message (a plain-text and an HTML version).
    text = body
# double qoute all of html message
    html = "<html><head></head><body><p>The <a href=\"{}\">Tst Month-End Premium & Commissions Report</a> is now available.</p></body></html>".format(link)

# Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

# Send the message via local SMTP server.
    s = smtplib.SMTP(host='prdsmtp01.mutualofenumclaw.net', port=25)
# sendmail function takes 3 arguments: sender's address, recipient's address
# and message to send - here it is sent as one string.
    s.sendmail(me, you, msg.as_string())
    s.quit()

if __name__ == "__main__":
    Macs_Import()
#print(env_vars.env)
#print(env_vars.vEnv_Analytics_DB)
#print(env_vars.vEnv_SNS_Teams_Channel)
from impersonation import *
from datetime import datetime, timedelta
from datetime import date
from pytz import timezone
from google.cloud import logging

# logging sa to impersonate
service_acount = "logging-sa@cf-data-analytics.iam.gserviceaccount.com"
# token scope
scope = "https://www.googleapis.com/auth/logging.read"
audience = "iap.googleapis.com"
project_id = "cf-data-analytics"

tz = timezone('America/New_York')
current_time = datetime.now(tz)

# return token from logging-sa
token = accesstoken_from_impersonated_credentials(service_acount, scope)

# show token - test in postman
print(token.token)

client = logging.Client(project=project_id, credentials=token)

# create timestamp to filter logs
time_minus_4h = (current_time.replace(
    minute=0, second=0, microsecond=0) - timedelta(hours=4)).strftime("%Y-%m-%dT%H:%M:%SZ")

logging_client = logging.Client()

# return logs iterable
logger = logging_client.logger(
    "dataform.googleapis.com%2Fworkflow_invocation_completion")

FILTER = 'AND timestamp>=' + '\"' + time_minus_4h + '\"'

print("Listing entries for logger {}:".format(logger.name))

for entry in logger.list_entries():
    timestamp = entry.timestamp.isoformat()
    print("* {}: {}".format(timestamp, entry.payload))

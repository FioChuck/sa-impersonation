from impersonation import *
from datetime import datetime, timedelta
from datetime import date
from pytz import timezone
from google.cloud import logging

service_acount = "logging-sa@cf-data-analytics.iam.gserviceaccount.com"
scope = "https://www.googleapis.com/auth/logging.read"
audience = "iap.googleapis.com"
project_id = "cf-data-analytics"

tz = timezone('America/New_York')
current_time = datetime.now(tz)

token = accesstoken_from_impersonated_credentials(service_acount, scope)

print(token.token)

client = logging.Client(project=project_id, credentials=token)

time_minus_4h = (current_time.replace(
    minute=0, second=0, microsecond=0) - timedelta(hours=4)).strftime("%Y-%m-%dT%H:%M:%SZ")

logging_client = logging.Client()
logger = logging_client.logger(
    "dataform.googleapis.com%2Fworkflow_invocation_completion")

FILTER = 'AND timestamp>=' + '\"' + time_minus_4h + '\"'

print("Listing entries for logger {}:".format(logger.name))

for entry in logger.list_entries():
    timestamp = entry.timestamp.isoformat()
    print("* {}: {}".format(timestamp, entry.payload))

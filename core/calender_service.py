# import datetime
# import os.path

# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build

# SCOPES = ['https://www.googleapis.com/auth/calendar']

# class CalendarService:
#     def __init__(self):
#         self.service = self._authenticate()

#     def _authenticate(self):
#         creds = None

#         if os.path.exists('token.json'):
#             creds = Credentials.from_authorized_user_file('token.json', SCOPES)

#         if not creds or not creds.valid:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)

#             with open('token.json', 'w') as token:
#                 token.write(creds.to_json())

#         return build('calendar', 'v3', credentials=creds)

#     def add_event(self, summary, start_time, end_time):
#         event = {
#             'summary': summary,
#             'start': {
#                 'dateTime': start_time,
#                 'timeZone': 'Asia/Kolkata',
#             },
#             'end': {
#                 'dateTime': end_time,
#                 'timeZone': 'Asia/Kolkata',
#             },
#         }

#         event = self.service.events().insert(
#             calendarId='primary', body=event).execute()

#         return event.get('htmlLink')

#     def get_today_events(self):
#         now = datetime.datetime.utcnow().isoformat() + 'Z'

#         events_result = self.service.events().list(
#             calendarId='primary',
#             timeMin=now,
#             maxResults=5,
#             singleEvents=True,
#             orderBy='startTime'
#         ).execute()

#         return events_result.get('items', [])

# # class CalendarService:
# #     def __init__(self):
# #         self.events = []

# #     def add_event(self, summary, start, end):
# #         event = {
# #             "summary": summary,
# #             "start": start,
# #             "end": end
# #         }
# #         self.events.append(event)
# #         return "local_event_created"

# #     def get_today_events(self):
# #         return self.events

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import datetime

SCOPES = ["https://www.googleapis.com/auth/calendar"]

class CalendarService:
    def __init__(self):
        self.creds = None

        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        if not self.creds or not self.creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            self.creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(self.creds.to_json())

        self.service = build("calendar", "v3", credentials=self.creds)

    def add_event(self, summary, start, end):
        event = {
            "summary": summary,
            "start": {"dateTime": start, "timeZone": "Asia/Kolkata"},
            "end": {"dateTime": end, "timeZone": "Asia/Kolkata"},
        }

        event = self.service.events().insert(calendarId="primary", body=event).execute()
        return event.get("htmlLink")

    def get_today_events(self):
        now = datetime.datetime.utcnow().isoformat() + "Z"

        events_result = self.service.events().list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        ).execute()

        return events_result.get("items", [])
from ics import Calendar
import requests
import arrow
import json
import azure.functions as func

def get_calendar():
    # Adding headers to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Parse the URLs
    airbnb_url = "https://www.airbnb.com/calendar/ical/54151941.ics?s=bb9e64f8505da96059cbf497632913d3"
    vrbo_url = "http://www.vrbo.com/icalendar/25d7d6f9c6da48c5af029ead9cd878be.ics?nonTentative"

    airbnb_cal = Calendar(requests.get(airbnb_url, headers=headers).text)
    vrbo_cal = Calendar(requests.get(vrbo_url, headers=headers).text)

    # Combine calendars
    merged_cal = Calendar()

    for event in vrbo_cal.events:
        merged_cal.events.add(event)

    for event in airbnb_cal.events:
        merged_cal.events.add(event)

    # Sort events
    sorted_events = sorted(merged_cal.events, key=lambda event: event.begin, reverse=False)

    # Create JSON data
    events_list = []

    for event in sorted_events:
        if event.begin >= arrow.now() and "Airbnb" not in event.name:
            events_list.append({
                "title": event.name,
                "start": event.begin.isoformat(),
                "end": event.end.isoformat(),
                "description": event.description,
                "uid": event.uid,
                "length": event.duration.days,
                "status": event.status
            })

    return events_list

# Serve as an Azure Function
def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        events = get_calendar()
        return {
            "statusCode": 200,
            "body": json.dumps(events),
            "headers": {
                "Content-Type": "application/json"
            }
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

if __name__ == "__main__":
    # For local testing
    events = get_calendar()
    print(json.dumps(events, indent=2))

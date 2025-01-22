from ics import Calendar
import requests
import arrow

def get_calendar():
    #adding headers because it mimics a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Parse the URL
    airbnb_url = "https://www.airbnb.com/calendar/ical/54151941.ics?s=bb9e64f8505da96059cbf497632913d3"
    airbnb_cal = Calendar(requests.get(airbnb_url, headers=headers).text)

    vrbo_url = "http://www.vrbo.com/icalendar/25d7d6f9c6da48c5af029ead9cd878be.ics?nonTentative"
    vrbo_cal = Calendar(requests.get(vrbo_url, headers=headers).text)
    
    #combine calendars
    merged_cal = Calendar()

    for event in vrbo_cal.events:
        merged_cal.events.add(event)

    for event in airbnb_cal.events:
        merged_cal.events.add(event)

    # sort events
    events = merged_cal.events
    sorted_events = sorted(events, key=lambda event: event.begin, reverse = False)

    # Iterate over each event in the calendar
    current_date = arrow.now().format('MMMM D, YYYY')
    events_list = []

    for event in sorted_events:
        if event.begin >= arrow.now() and "Airbnb" not in event.name:
            start_date = event.begin.format('MMMM D, YYYY')
            end_date = event.end.format('MMMM D, YYYY')
            uid = event.uid
            description = event.description
            name = event.name
            length = event.duration.days
            other = event.status
            
            # Append the extracted details to the events list
            events_list.append((start_date, end_date, description, uid, name, length, other, current_date))

    return events_list
    # for event in events_list:
    #     print(f"ID: {event[2]} \nName: {event[4]} \nStart Date: {event[0]} 3:00 PM \nEnd Date: {event[1]} 10:00 AM \nLength: {event[5]}\n")

if __name__=="__main__":
    events = get_calendar()
    for event in events:
        print(event[7])
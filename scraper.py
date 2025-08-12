import datetime
import json
import logging
from typing import List
from bs4 import BeautifulSoup
from bs4.element import Tag
import requests

from database import get_course, insert_course, update_course_events
from models.classes import EventInfo

logger = logging.getLogger(__name__)
BASE_URL = 'https://discgolfmetrix.com'


def parse_row(row: Tag) -> EventInfo | None:
    columns = row.find_all('td')
    if len(columns) <= 0:
        return

    date = columns[0].get_text()
    event = columns[1].get_text()
    return EventInfo(event, date)

def get_course_layouts(course_id: int) -> list[str]:
    session = requests.Session()
    layouts: List[str] = []

    r = session.get(f"{BASE_URL}/course/{course_id}")

    soup = BeautifulSoup(r.text, 'html.parser')

    for course in soup.find_all('a', class_='button'):
        if type(course) is Tag:
            href = str(course.get('href'))
            if href and 'course' in href:
                layouts.append(href)

    return layouts

def get_layout_details(layout_url: str) -> List[EventInfo]:
    events: List[EventInfo] = []
    session = requests.Session()
    r = session.get(f"{BASE_URL}{layout_url}")
    soup = BeautifulSoup(r.text, 'html.parser')

    title = soup.find('h2', string='Upcoming events')

    if title is None:
        return []
    
    upcomingEvents = title.find_next('table')

    if upcomingEvents is None:
        return []
    
    tableRows = upcomingEvents.find_all_next('tr')

    for row in tableRows:
        if type(row) is not Tag:
            continue
        parsed_row = parse_row(row)
        if parsed_row is None:
            continue
        events.append(parsed_row)

    return events

def update_course(layout_ids: List[int], metrix_id: int):
    events: List[EventInfo] = []
    for layout in layout_ids:
        layout_details = get_layout_details(f'/course/{layout}')
        events = layout_details
    update_course_events(json.dumps(events), metrix_id)
    return

def get_course_details(course_name: str) -> List[EventInfo]:
    logger.info(f'Getting course details for course: {course_name}')
    timestamp = datetime.datetime.now(datetime.timezone.utc)
    course_details = get_course(course_name)
    
    if course_details is None:
        return []

    last_update_at = course_details[5]
    metrix_id = int(course_details[2])
    cache_time = datetime.datetime.fromisoformat(last_update_at) + datetime.timedelta(days=1)

    # If cache time is lower than time now update course
    if cache_time < datetime.datetime.now(datetime.timezone.utc):
        logger.info(f"Cache expired for course: {metrix_id}, updating course details....")
        layout_ids: List[int] = json.loads(str(course_details[3]))
        update_course(layout_ids, metrix_id)

    events: List[EventInfo] = json.loads(str(course_details[4]))
    upcoming_events: List[EventInfo] = []

    for event in events:
        if datetime.datetime.fromisoformat(event[1]).replace(tzinfo=datetime.timezone.utc) < timestamp:
            continue
        upcoming_events.append(event)
    return upcoming_events

def create_course(course_id: int) -> None:
    session = requests.Session()
    r = session.get(f"{BASE_URL}/course/{course_id}")
    soup = BeautifulSoup(r.text, 'html.parser')
    layouts = get_course_layouts(course_id)
    page_title = soup.find('h1')
    if page_title is None:
        return

    course_name = page_title.find_next('a')
    if course_name is None:
        # unable to find course name
        return

    layout_ids: List[int] = []
    events: List[EventInfo] = []

    for layout in layouts:
        layout_details = get_layout_details(layout)
        for layout_detail in layout_details:
            events.append(layout_detail)
        layout_ids.append(int(layout.removeprefix("/course/")))
    insert_course(course_name.get_text(), course_id, json.dumps(layout_ids), json.dumps(events))
    return
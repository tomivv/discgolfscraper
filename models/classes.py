from typing import NamedTuple

class Course(NamedTuple):
    id: int
    name: str
    metrix_id: int
    layout_ids: str
    events: str
    updated_at: str

class EventInfo(NamedTuple):
    event_name: str
    date: str
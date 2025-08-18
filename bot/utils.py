def check_valid_course_name(course: str, name: str):
    if course.lower() == name.lower():
        return True
    if course.lower().startswith(name.lower()):
        return True
    return False
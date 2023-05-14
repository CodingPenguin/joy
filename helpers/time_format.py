from datetime import datetime

def date_to_str(d: datetime):
    return datetime.strftime(d, format="%Y-%m-%dT%H:%M:%S.%fZ")

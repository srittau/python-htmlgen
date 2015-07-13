import datetime
import re


def parse_rfc3339_partial_time(value):
    matches = re.match(r"^(\d\d):(\d\d):(\d\d)(\.(\d+))?$", value)
    if not matches:
        return None
    fractions = int(matches.group(5)) if matches.group(4) else 0
    return datetime.time(int(matches.group(1)), int(matches.group(2)),
                         int(matches.group(3)), fractions)

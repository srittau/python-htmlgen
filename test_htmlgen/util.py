import re
from typing import Dict

_short_tag_re = re.compile(r'^<([a-z0-9]+)(( [a-z0-9-]+="[^"]*")*)/>$')
_attribute_re = re.compile(r' ([a-z0-9-]+)="([^"]*)"')


def parse_short_tag(string):
    matches = _short_tag_re.match(string)
    assert matches is not None
    tag = Tag(matches.group(1))
    attribute_string = matches.group(2)
    for match in _attribute_re.findall(attribute_string):
        tag.add_attribute(*match)
    return tag


class Tag(object):

    def __init__(self, name):
        self.name = name
        self.attributes = {}  # type: Dict[str, str]

    def add_attribute(self, name, value):
        if name in self.attributes:
            raise AssertionError("duplicate attribute '" + name + "'")
        self.attributes[name] = value

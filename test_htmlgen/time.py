from datetime import datetime, date
from unittest import TestCase

from asserts import assert_equal

from htmlgen import Time


class TimeTest(TestCase):

    def test_date(self):
        time = Time(date(2013, 11, 3))
        time.append("Test")
        assert_equal(
            [b'<time datetime="2013-11-03">', b"Test", b"</time>"],
            list(iter(time)))

    def test_datetime(self):
        time = Time(datetime(2013, 4, 14, 12, 4, 13))
        time.append("Test")
        assert_equal(
            [b'<time datetime="2013-04-14T12:04:13Z">', b"Test", b"</time>"],
            list(iter(time)))

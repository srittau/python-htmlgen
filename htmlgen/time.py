from htmlgen.element import Element


class Time(Element):

    """An HTML date/time (<time>) element.

    >>> from datetime import date, datetime
    >>> time1 = Time(date(2014, 12, 31))
    >>> time1.append("new year's eve")
    >>> str(time1)
    '<time datetime="2014-12-31">new year&#x27;s eve</time>'
    >>> time2 = Time(datetime(2014, 5, 17, 13, 15, 0))
    >>> time2.append("May 17th, quarter past one")
    >>> str(time2)
    '<time datetime="2014-05-17T13:15:00Z">May 17th, quarter past one</time>'

    """

    def __init__(self, date):
        super(Time, self).__init__("time")
        if hasattr(date, "hour"):
            formatted = date.strftime("%Y-%m-%dT%H:%M:%SZ")
        else:
            formatted = date.strftime("%Y-%m-%d")
        self.set_attribute("datetime", formatted)

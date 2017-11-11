import datetime

from htmlgen.timeutil import parse_rfc3339_partial_time


class html_attribute(object):

    """Add an attribute to an HTML element.

        >>> from htmlgen import Element
        >>> class MyElement(Element):
        ...     url = html_attribute("data-url")
        >>> element = MyElement("div")
        >>> element.url
        >>> str(element)
        '<div></div>'
        >>> element.url = "http://www.example.com/"
        >>> str(element)
        '<div data-url="http://www.example.com/"></div>'

    If the optional default argument is given, the attribute will not be
    included if the value matches it.

        >>> class MyElement(Element):
        ...     value = html_attribute("data-value", default="hello")
        >>> element = MyElement("div")
        >>> element.value
        'hello'
        >>> str(element)
        '<div></div>'

    """

    def __init__(self, attribute_name, default=None):
        self._attribute_name = attribute_name
        self._default = default

    def __get__(self, obj, _=None):
        return obj.get_attribute(self._attribute_name, default=self._default)

    def __set__(self, obj, value):
        if value is None or value == self._default:
            obj.remove_attribute(self._attribute_name)
        else:
            obj.set_attribute(self._attribute_name, value)


class boolean_html_attribute(object):

    """Add a boolean attribute to an HTML element.

        >>> from htmlgen import Element
        >>> class MyElement(Element):
        ...     doit = boolean_html_attribute("data-doit")
        >>> element = MyElement("div")
        >>> element.doit
        False
        >>> str(element)
        '<div></div>'
        >>> element.doit = True
        >>> str(element)
        '<div data-doit="data-doit"></div>'

    """

    def __init__(self, attribute_name):
        self._attribute_name = attribute_name

    def __get__(self, obj, _=None):
        return obj.get_attribute(self._attribute_name) == self._attribute_name

    def __set__(self, obj, value):
        if value:
            obj.set_attribute(self._attribute_name, self._attribute_name)
        else:
            obj.remove_attribute(self._attribute_name)


class int_html_attribute(object):

    """Add an attribute to an HTML element that accepts only integers.

        >>> from htmlgen import Element
        >>> class MyElement(Element):
        ...     value = int_html_attribute("data-value")
        >>> element = MyElement("div")
        >>> element.value
        >>> str(element)
        '<div></div>'
        >>> element.value = 42
        >>> str(element)
        '<div data-value="42"></div>'

    If the optional default argument is given, the attribute will not be
    included if the value matches it.

        >>> class MyElement(Element):
        ...     value = int_html_attribute("data-value", default=0)
        >>> element = MyElement("div")
        >>> element.value
        0
        >>> str(element)
        '<div></div>'

    """

    def __init__(self, attribute_name, default=None):
        self._attribute_name = attribute_name
        self._default = default

    def __get__(self, obj, _=None):
        value = obj.get_attribute(self._attribute_name, default=self._default)
        if value is None:
            return None
        return int(value)

    def __set__(self, obj, value):
        if value is None or value == self._default:
            obj.remove_attribute(self._attribute_name)
        else:
            obj.set_attribute(self._attribute_name, str(value))


class float_html_attribute(object):

    """Add an attribute to an HTML element that accepts only numbers.

        >>> from htmlgen import Element
        >>> class MyElement(Element):
        ...     value = float_html_attribute("data-value")
        >>> element = MyElement("div")
        >>> element.value
        >>> str(element)
        '<div></div>'
        >>> element.value = 4.2
        >>> str(element)
        '<div data-value="4.2"></div>'

    If the optional default argument is given, the attribute will not be
    included if the value matches it.

        >>> class MyElement(Element):
        ...     value = float_html_attribute("data-value", default=0.4)
        >>> element = MyElement("div")
        >>> element.value
        0.4
        >>> str(element)
        '<div></div>'

    """

    def __init__(self, attribute_name, default=None):
        self._attribute_name = attribute_name
        self._default = default

    def __get__(self, obj, _=None):
        value = obj.get_attribute(self._attribute_name, default=self._default)
        if value is None:
            return None
        return float(value)

    def __set__(self, obj, value):
        if value is None or value == self._default:
            obj.remove_attribute(self._attribute_name)
        else:
            obj.set_attribute(self._attribute_name, str(value))


class time_html_attribute(object):

    """Add an attribute to an HTML element that accepts only time values.

    >>> from htmlgen import Element
    >>> class MyElement(Element):
    ...     time = time_html_attribute("data-time")
    >>> element = MyElement("div")
    >>> element.time
    >>> str(element)
    '<div></div>'
    >>> element.time = datetime.time(8, 15)
    >>> str(element)
    '<div data-time="08:15:00"></div>'

    If the optional default argument is given, the attribute will not be
    included if the value matches it.

    >>> class MyElement(Element):
    ...     value = time_html_attribute(
    ...         "data-value", default=datetime.time(8, 0))
    >>> element = MyElement("div")
    >>> element.value
    datetime.time(8, 0)
    >>> str(element)
    '<div></div>'

    """

    def __init__(self, attribute_name, default=None):
        self._attribute_name = attribute_name
        self._default = default

    def __get__(self, obj, _=None):
        value = obj.get_attribute(self._attribute_name)
        if value is None:
            return self._default
        return parse_rfc3339_partial_time(value)

    def __set__(self, obj, value):
        if value is None or value == self._default:
            obj.remove_attribute(self._attribute_name)
        else:
            obj.set_attribute(self._attribute_name, str(value))


class list_html_attribute(object):

    """Add an attribute to an HTML element that accepts a list of strings.

    >>> from htmlgen import Element
    >>> class MyElement(Element):
    ...     list = list_html_attribute("data-list")
    >>> element = MyElement("div")
    >>> element.list
    []
    >>> str(element)
    '<div></div>'
    >>> element.list = ["foo", "bar"]
    >>> str(element)
    '<div data-list="foo,bar"></div>'

    """

    def __init__(self, attribute_name):
        self._attribute_name = attribute_name

    def __get__(self, obj, _=None):
        value = obj.get_attribute(self._attribute_name)
        return value.split(",") if value else []

    def __set__(self, obj, value):
        if value:
            obj.set_attribute(self._attribute_name, ",".join(value))
        else:
            obj.remove_attribute(self._attribute_name)


class data_attribute(html_attribute):

    def __init__(self, data_name, default=None):
        attribute_name = "data-" + data_name
        super(data_attribute, self).__init__(attribute_name, default)


class css_class_attribute(object):

    """Add a boolean attribute to an HTML element that add a CSS class.

    >>> from htmlgen import Element
    >>> class MyElement(Element):
    ...     test = css_class_attribute("my-class")
    >>> element = MyElement("div")
    >>> element.add_css_classes("other-class")
    >>> element.test
    False
    >>> str(element)
    '<div class="other-class"></div>'
    >>> element.test = True
    >>> str(element)
    '<div class="my-class other-class"></div>'

    """

    def __init__(self, css_class):
        self._css_class = css_class

    def __get__(self, obj, _=None):
        return obj.has_css_class(self._css_class)

    def __set__(self, obj, value):
        if value:
            obj.add_css_classes(self._css_class)
        else:
            obj.remove_css_classes(self._css_class)

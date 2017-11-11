from htmlgen.attribute import html_attribute
from htmlgen.generator import Generator
from htmlgen.element import Element, NonVoidElement, VoidElement


MIME_JAVASCRIPT = "text/javascript"
MIME_JSON = "application/json"


class Document(Generator):

    """An HTML document.

    A document consists of a doctype declaration and the HTML root tag.

        >>> doc = Document(title="My Page")
        >>> doc.title
        'My Page'
        >>> str(doc)
        '<!DOCTYPE html><html lang="en" xml:lang="en" xmlns="http://www.w3.org/1999/xhtml"><head><title>My Page</title><meta charset="utf-8"/></head><body></body></html>'

    The default HTML root element can be overwritten:

        >>> doc = Document(title="Hello World!")
        >>> doc.root.head.title.title
        'Hello World!'
        >>> doc.root = HTMLRoot(title="Brave New World")
        >>> doc.root.head.title.title
        'Brave New World'

    Document objects provide several convenience methods for constructing
    documents:

        >>> doc.add_script("my-script.js")
        >>> doc.add_stylesheet("style.css")
        >>> doc.append_body(Element("div"))

    """

    def __init__(self, title=None, language="en"):
        super(Document, self).__init__()
        self.root = HTMLRoot(title=title, language=language)

    def generate(self):
        yield "<!DOCTYPE html>"
        yield self.root

    @property
    def title(self):
        return self.root.head.title.title

    @title.setter
    def title(self, title):
        self.root.head.title.title = title

    def add_stylesheets(self, *stylesheets):
        self.root.head.add_stylesheets(*stylesheets)

    def add_stylesheet(self, stylesheet):
        self.root.head.add_stylesheet(stylesheet)

    def add_scripts(self, *scripts):
        self.root.head.add_scripts(*scripts)

    def add_script(self, script):
        self.root.head.add_script(script)

    def append_head(self, child):
        self.root.head.append(child)

    def append_body(self, child):
        self.root.body.append(child)


class HTMLRoot(NonVoidElement):

    """HTML root (<html>) element.

        >>> root = HTMLRoot(title="My Page")
        >>> str(root)
        '<html lang="en" xml:lang="en" xmlns="http://www.w3.org/1999/xhtml"><head><title>My Page</title><meta charset="utf-8"/></head><body></body></html>'

    Head and body elements are constructed by default, but they can be
    overwritten:

        >>> root.head = Head()
        >>> root.body = Body()

    """

    def __init__(self, title="", language="en"):
        super(HTMLRoot, self).__init__("html")
        self.head = Head(title=title)
        self.body = Body()
        self.set_attribute("xmlns", "http://www.w3.org/1999/xhtml")
        self.set_attribute("lang", language)
        self.set_attribute("xml:lang", language)

    def generate_children(self):
        yield self.head
        yield self.body


class Head(Element):

    """HTML document head (<head>) element.

    A title element is provided by default, but it can be overwritten:

        >>> head = Head("My Page")
        >>> head.title.title
        'My Page'
        >>> head.title = Title("New Page")

    There are convenience methods for adding stylesheets and scripts:

        >>> head.add_stylesheet("style.css")
        >>> head.add_script("script.js")

    """

    def __init__(self, title=None):
        super(Head, self).__init__("head")
        self._title = Title(title)
        self.append(self._title)
        self.append(Meta.create_charset("utf-8"))

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self.remove(self._title)
        self.append(title)
        self._title = title

    def add_stylesheets(self, *stylesheets):
        for stylesheet in stylesheets:
            self.add_stylesheet(stylesheet)

    def add_stylesheet(self, stylesheet):
        self.append(HeadLink.create_stylesheet(stylesheet))

    def add_scripts(self, *scripts):
        for script in scripts:
            self.add_script(script)

    def add_script(self, script):
        self.append(Script(script))


class Body(Element):

    """HTML body (<body>) element."""

    def __init__(self):
        super(Body, self).__init__("body")


class Title(NonVoidElement):

    """HTML page title (<title>) element."""

    def __init__(self, title=None):
        super(Title, self).__init__("title")
        self.title = title or ""

    def generate_children(self):
        if self.title:
            yield self.title


class Meta(VoidElement):

    """HTML meta information (<meta>) element."""

    def __init__(self):
        super(Meta, self).__init__("meta")

    @classmethod
    def create_charset(cls, charset):
        meta = cls()
        meta.set_attribute("charset", charset)
        return meta


class Script(NonVoidElement):

    """HTML script (<script>) element.

    A script element can either point to an external script via the url
    attribute or it contains the script as element contents:

        >>> external_script = Script(url="http://www.example.com/script.js")
        >>> external_script.url
        'http://www.example.com/script.js'
        >>> external_script.script
        >>> internal_script = Script(script="alert('Hello World!');")
        >>> internal_script.url
        >>> internal_script.script
        "alert('Hello World!');"

    The type attribute can be overridden:

        >>> json_script = Script()
        >>> json_script.type = "application/json"

    It defaults to Javascript:

        >>> Script().type
        'text/javascript'

    """

    def __init__(self, url=None, script=None):
        assert url is None or script is None
        super(Script, self).__init__("script")
        if url:
            self.url = url
        self.script = script

    type = html_attribute("type", default=MIME_JAVASCRIPT)
    url = html_attribute("src")

    def generate_children(self):
        if self.script:
            yield self.script


def json_script(json):
    """Create a Script element with JSON payload.

        >>> script = json_script({"s": "test", "a": [1, 2]})
        >>> script.type
        'application/json'
        >>> script.script
        '{"s": "test", "a": [1, 2]}'

    """

    from json import dumps

    serialized = dumps(json)
    escaped = serialized.replace("</", "<\\/")  # XSS protection
    script = Script(script=escaped)
    script.type = MIME_JSON
    return script


class HeadLink(VoidElement):

    """HTML meta data link (<link>) element."""

    def __init__(self, relation, url):
        super(HeadLink, self).__init__("link")
        self.relation = relation
        self.url = url

    relation = html_attribute("rel")
    url = html_attribute("href")

    @classmethod
    def create_stylesheet(cls, stylesheet):
        return cls("stylesheet", stylesheet)


class Main(Element):

    """HTML main document content (<main>) element."""

    def __init__(self):
        super(Main, self).__init__("main")

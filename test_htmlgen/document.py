from typing import cast, List
from unittest import TestCase

from asserts import assert_equal, assert_is_not, assert_is, assert_is_none, \
    assert_is_instance

from htmlgen import (Element, Document, HTMLRoot, Head, Body,
                     Title, Meta, Script, HeadLink, Main)
from htmlgen.document import json_script


class _TestingHead(Head):

    def __init__(self):
        super(_TestingHead, self).__init__()
        self.stylesheets = []  # type: List[str]
        self.scripts = []  # type: List[str]

    def add_stylesheet(self, style):
        self.stylesheets.append(style)

    def add_stylesheets(self, *styles):
        self.stylesheets.extend(styles)

    def add_script(self, script):
        self.scripts.append(script)

    def add_scripts(self, *scripts):
        self.scripts.extend(scripts)


class DocumentTest(TestCase):

    def test_generate(self):
        doc = Document()
        doc.root = cast(HTMLRoot, Element("html"))
        assert_equal([b"<!DOCTYPE html>", b"<html>", b"</html>"],
                     list(iter(doc)))

    def test_title(self):
        doc = Document(title="Test Title")
        assert_equal("Test Title", doc.title)
        assert_equal("Test Title", doc.root.head.title.title)
        doc.title = "New Title"
        assert_equal("New Title", doc.title)
        assert_equal("New Title", doc.root.head.title.title)

    def test_default_title(self):
        doc = Document()
        assert_equal("", doc.title)
        assert_equal("", doc.root.head.title.title)

    def test_language(self):
        doc = Document(language="de")
        assert_equal("de", doc.root.get_attribute("lang"))
        assert_equal("de", doc.root.get_attribute("xml:lang"))

    def test_default_language(self):
        doc = Document()
        assert_equal("en", doc.root.get_attribute("lang"))
        assert_equal("en", doc.root.get_attribute("xml:lang"))

    def test_stylesheets(self):
        head = _TestingHead()
        doc = Document()
        doc.root.head = head
        doc.add_stylesheet("style.css")
        doc.add_stylesheets("style1.css", "style2.css")
        assert_equal(["style.css", "style1.css", "style2.css"],
                     head.stylesheets)

    def test_scripts(self):
        head = _TestingHead()
        doc = Document()
        doc.root.head = head
        doc.add_script("script.js")
        doc.add_scripts("script1.js", "script2.js")
        assert_equal(["script.js", "script1.js", "script2.js"], head.scripts)

    def test_append(self):
        doc = Document()
        old_child_count = len(doc.root.head)
        doc.append_head("Test Head")
        assert_equal(old_child_count + 1, len(doc.root.head))
        doc.append_body("Test Body")
        assert_equal(1, len(doc.root.body))


class HTMLRootTest(TestCase):

    def test_default_language(self):
        root = HTMLRoot()
        assert_equal(b'<html lang="en" xml:lang="en" '
                     b'xmlns="http://www.w3.org/1999/xhtml">',
                     next(iter(root)))

    def test_custom_language(self):
        root = HTMLRoot(language="de")
        assert_equal(b'<html lang="de" xml:lang="de" '
                     b'xmlns="http://www.w3.org/1999/xhtml">',
                     next(iter(root)))

    def test_title(self):
        root = HTMLRoot(title="Test Title")
        assert_equal("Test Title", root.head.title.title)


class HeadTest(TestCase):

    def test_element(self):
        head = Head()
        head_items = list(iter(head))
        assert_equal(b"<head>", head_items[0])
        assert_equal(b"</head>", head_items[4])

    def test_default_title(self):
        head = Head()
        assert_equal("", head.title.title)
        assert_equal([b"<title>", b"</title>"], list(iter(head))[1:3])

    def test_custom_title(self):
        head = Head(title="Test Title")
        assert_equal("Test Title", head.title.title)
        assert_equal([b"<title>", b"Test Title", b"</title>"],
                     list(iter(head))[1:4])

    def test_charset(self):
        head = Head()
        assert_equal(b'<meta charset="utf-8"/>', list(iter(head))[3])

    def test_custom_title_element(self):
        head = Head()
        old_title = head.title
        old_child_count = len(head)
        new_title = Title()
        head.title = new_title
        assert_equal(old_child_count, len(head))
        assert_is_not(old_title, head.title)
        assert_is(new_title, head.title)

    def test_stylesheets(self):
        head = Head()
        head.add_stylesheet("style.css")
        head.add_stylesheets("style1.css", "style2.css")
        style1 = cast(HeadLink, head.children.children[-3])
        assert_equal("link", style1.element_name)
        assert_equal("style.css", style1.get_attribute("href"))
        style2 = cast(HeadLink, head.children.children[-1])
        assert_equal("link", style2.element_name)
        assert_equal("style2.css", style2.get_attribute("href"))

    def test_scripts(self):
        head = Head()
        head.add_script("script.js")
        head.add_scripts("script1.js", "script2.js")
        script1 = cast(Script, head.children.children[-3])
        assert_equal("script", script1.element_name)
        assert_equal("script.js", script1.get_attribute("src"))
        script2 = cast(Script, head.children.children[-1])
        assert_equal("script", script2.element_name)
        assert_equal("script2.js", script2.get_attribute("src"))


class BodyTest(TestCase):

    def test_element(self):
        body = Body()
        assert_equal([b"<body>", b"</body>"], list(iter(body)))


class TitleTest(TestCase):

    def test_custom_title(self):
        title = Title(title="Test Title")
        assert_equal("Test Title", title.title)
        title.title = "New Title"
        assert_equal([b"<title>", b"New Title", b"</title>"],
                     list(iter(title)))

    def test_default_title(self):
        title = Title()
        assert_equal("", title.title)
        assert_equal([b"<title>", b"</title>"], list(iter(title)))


class MetaTest(TestCase):

    def test_default(self):
        meta = Meta()
        assert_equal([b"<meta/>"], list(iter(meta)))

    def test_create_charset(self):
        meta = Meta.create_charset("utf-8")
        assert_equal("utf-8", meta.get_attribute("charset"))
        assert_equal([b'<meta charset="utf-8"/>'], list(iter(meta)))


class ScriptTest(TestCase):

    def test_url(self):
        script = Script(url="script.js")
        assert_equal("script.js", script.url)
        assert_is_none(script.script)
        assert_equal([b'<script src="script.js">', b'</script>'],
                     list(iter(script)))

    def test_script(self):
        script = Script(script='alert("foo");')
        assert_is_none(script.url)
        assert_equal('alert("foo");', script.script)
        assert_equal([b'<script>', b'alert("foo");', b'</script>'],
                     list(iter(script)))

    def test_type(self):
        script = Script()
        script.type = "application/json"
        assert_equal([b'<script type="application/json">', b'</script>'],
                     list(iter(script)))

    def test_type_default(self):
        script = Script()
        assert_equal("text/javascript", script.type)


class JSONScriptTest(TestCase):

    def test_element_type(self):
        script = json_script([])
        assert_is_instance(script, Script)

    def test_type(self):
        script = json_script([])
        assert_equal("application/json", script.type)

    def test_script(self):
        script = json_script([1, 2, "a"])
        assert_equal('[1, 2, "a"]', script.script)

    def test_serialized(self):
        script = json_script([1, 2, "a"])
        assert_equal('<script type="application/json">[1, 2, "a"]</script>',
                     str(script))

    def test_escape_slash(self):
        script = json_script(["</script>"])
        assert_equal(
            '<script type="application/json">["<\\/script>"]</script>',
            str(script))


class HeadLinkTest(TestCase):

    def test_attributes(self):
        link = HeadLink("next", "test.html")
        assert_equal("next", link.relation)
        assert_equal("test.html", link.url)
        assert_equal([b'<link href="test.html" rel="next"/>'],
                     list(iter(link)))

    def test_create_stylesheet(self):
        link = HeadLink.create_stylesheet("style.css")
        assert_equal("stylesheet", link.relation)
        assert_equal("style.css", link.url)


class MainTest(TestCase):

    def test_generate(self):
        main = Main()
        assert_equal([b'<main>', b'</main>'], list(iter(main)))

# -*- coding: utf-8 -*-

from unittest import TestCase

from asserts import assert_equal, assert_raises, assert_is_instance, assert_is

from htmlgen.generator import (Generator,
                               NullGenerator,
                               IteratorGenerator,
                               ChildGenerator,
                               HTMLChildGenerator,
                               JoinGenerator,
                               HTMLJoinGenerator, generate_html_string)


class _TestingGenerator(Generator):

    def __init__(self, items):
        self._items = items

    def generate(self):
        return iter(self._items)


class GeneratorTest(TestCase):

    def test_empty_generate(self):
        generator = _TestingGenerator([])
        assert_equal([], list(iter(generator)))

    def test_generate_strings_only(self):
        generator = _TestingGenerator([u"foo", u"bar", u"baz"])
        assert_equal([b"foo", b"bar", b"baz"], list(iter(generator)))

    # redundant for Python 3
    def test_generate_python2_strings(self):
        inner = _TestingGenerator(["bär"])
        generator = _TestingGenerator(["foo", inner])
        assert_equal([b"foo", b"b\xc3\xa4r"], list(iter(generator)))

    def test_generate_non_ascii(self):
        inner = _TestingGenerator([u"bär"])
        generator = _TestingGenerator([u"fooß", inner])
        assert_equal([b"foo\xc3\x9f", b"b\xc3\xa4r"], list(iter(generator)))

    def test_generate_bytes(self):
        inner = _TestingGenerator([b"bar"])
        generator = _TestingGenerator([b"foo", inner])
        assert_equal([b"foo", b"bar"], list(iter(generator)))

    def test_generate_sub_generators(self):
        inner1 = _TestingGenerator([u"bar"])
        inner2 = _TestingGenerator([u"foo", inner1])
        generator = _TestingGenerator([inner2, u"baz"])
        assert_equal([b"foo", b"bar", b"baz"], list(iter(generator)))

    def test_str(self):
        inner = _TestingGenerator([u"bar"])
        generator = _TestingGenerator([u"foo", inner, u"baz"])
        assert_equal("foobarbaz", str(generator))

    def test_invalid_class(self):
        generator = _TestingGenerator([5])
        with assert_raises(TypeError):
            str(generator)


class NullGeneratorTest(TestCase):
    
    def test_generate(self):
        assert_equal([], list(iter(NullGenerator())))


class IteratorGeneratorTest(TestCase):

    def test_generate(self):
        generator = IteratorGenerator(["foo", "bar"])
        assert_equal([b"foo", b"bar"], list(iter(generator)))


class ChildGeneratorTest(TestCase):

    def test_append(self):
        generator = ChildGenerator()
        generator.append(u"c1")
        generator.append(_TestingGenerator([u"c2", u"c3"]))
        assert_equal([b"c1", b"c2", b"c3"], list(iter(generator)))

    def test_extend(self):
        generator = ChildGenerator()
        generator.append(u"c1")
        generator.extend([_TestingGenerator([u"c2", u"c3"]), u"c4"])
        assert_equal([b"c1", b"c2", b"c3", b"c4"], list(iter(generator)))

    def test_remove_string(self):
        generator = ChildGenerator()
        generator.append("foo")
        generator.append("bar")
        generator.remove("foo")
        assert_equal([b"bar"], list(iter(generator)))

    def test_remove_generator(self):
        sub_generator = Generator()
        generator = ChildGenerator()
        generator.append("foo")
        generator.append(sub_generator)
        generator.remove(sub_generator)
        assert_equal([b"foo"], list(iter(generator)))

    def test_remove__not_found(self):
        generator = ChildGenerator()
        generator.append("foo")
        with assert_raises(ValueError):
            generator.remove("abc")

    def test_len(self):
        generator = ChildGenerator()
        generator.append(u"c1")
        generator.extend([u"c2", u"c3", NullGenerator()])
        assert_equal(4, len(generator))

    def test_empty(self):
        generator = ChildGenerator()
        generator.append(u"c1")
        generator.extend([u"c2", u"c3", NullGenerator()])
        generator.empty()
        assert_equal([], list(iter(generator)))

    def test_children(self):
        generator = ChildGenerator()
        generator.append("Foo")
        assert_equal(["Foo"], generator.children)
        generator.children.append("Bar")
        assert_equal(["Foo"], generator.children)


class HTMLChildGeneratorTest(TestCase):

    def test_append(self):
        generator = HTMLChildGenerator()
        generator.append(u"c1&c2")
        generator.append(_TestingGenerator([u"c3", u"<c4>"]))
        assert_equal([b"c1&amp;c2", b"c3", b"<c4>"], list(iter(generator)))

    def test_append_raw(self):
        generator = HTMLChildGenerator()
        generator.append_raw(u"c1&c2")
        generator.append_raw(_TestingGenerator([u"c3", u"<c4>"]))
        assert_equal([b"c1&c2", b"c3", b"<c4>"], list(iter(generator)))

    def test_extend(self):
        generator = HTMLChildGenerator()
        generator.append(u"c1")
        generator.extend([_TestingGenerator([u"c2", u"c&3"]), u"<c4>"])
        assert_equal([b"c1", b"c2", b"c&3", b"&lt;c4&gt;"],
                     list(iter(generator)))

    def test_extend_raw(self):
        generator = HTMLChildGenerator()
        generator.append(u"c1")
        generator.extend_raw([_TestingGenerator([u"c&2", u"c3"]), u"<c4>"])
        assert_equal([b"c1", b"c&2", b"c3", b"<c4>"], list(iter(generator)))

    def test_remove_not_found(self):
        generator = HTMLChildGenerator()
        generator.extend(["foo", "bar"])
        with assert_raises(ValueError):
            generator.remove("baz")

    def test_remove(self):
        generator = HTMLChildGenerator()
        generator.extend_raw(["foo", "bar", "lower &lt; than"])
        generator.remove("foo")
        generator.remove("lower < than")
        assert_equal([b"bar"], list(iter(generator)))

    def test_remove_generator(self):
        sub_generator = Generator()
        generator = HTMLChildGenerator()
        generator.append(sub_generator)
        generator.append("foo")
        generator.remove(sub_generator)
        assert_equal([b"foo"], list(iter(generator)))

    def test_remove_raw_not_found(self):
        generator = HTMLChildGenerator()
        generator.extend(["foo", "bar"])
        with assert_raises(ValueError):
            generator.remove_raw("baz")

    def test_remove_raw(self):
        generator = HTMLChildGenerator()
        generator.extend_raw(["foo", "bar", "lower < than"])
        generator.remove_raw("foo")
        generator.remove_raw("lower < than")
        assert_equal([b"bar"], list(iter(generator)))

    def test_remove_raw_generator(self):
        sub_generator = Generator()
        generator = HTMLChildGenerator()
        generator.append(sub_generator)
        generator.append("foo")
        generator.remove_raw(sub_generator)
        assert_equal([b"foo"], list(iter(generator)))

    def test_len(self):
        generator = HTMLChildGenerator()
        generator.append(u"c1")
        generator.extend([u"c2", u"c3", NullGenerator()])
        assert_equal(4, len(generator))

    def test_empty(self):
        generator = HTMLChildGenerator()
        generator.append(u"c1")
        generator.extend([u"c2", u"c3", NullGenerator()])
        generator.empty()
        assert_equal([], list(iter(generator)))

    def test_children(self):
        generator = HTMLChildGenerator()
        generator.append("Foo")
        generator.append("<tag>")
        assert_equal(["Foo", "&lt;tag&gt;"], generator.children)

    def test_children_readonly(self):
        generator = HTMLChildGenerator()
        generator.append("Foo")
        generator.children.append("Bar")
        assert_equal(["Foo"], generator.children)


class GenerateHTMLStringTest(TestCase):

    def test_wrap_string(self):
        generator = generate_html_string("Test")
        assert_is_instance(generator, HTMLChildGenerator)
        result = list(iter(generator))
        assert_equal([b"Test"], result)

    def test_escape_string(self):
        generator = generate_html_string("<br>")
        assert_is_instance(generator, HTMLChildGenerator)
        result = list(iter(generator))
        assert_equal([b"&lt;br&gt;"], result)

    def test_do_not_wrap_generator(self):
        other_gen = Generator()
        generator = generate_html_string(other_gen)
        assert_is(other_gen, generator)


class JoinGeneratorTest(TestCase):

    def test_no_pieces(self):
        generator = JoinGenerator(u"!")
        assert_equal([], list(iter(generator)))

    def test_supplied_pieces(self):
        generator = JoinGenerator(u"!", [u"foo", u"bar"])
        assert_equal([b"foo", b"!", b"bar"], list(iter(generator)))

    def test_append_extend(self):
        generator = JoinGenerator(u"!", [u"foo"])
        generator.append(u"bar")
        sub_generator = ChildGenerator()
        sub_generator.append(u"baz")
        generator.extend([sub_generator])
        assert_equal([b"foo", b"!", b"bar", b"!", b"baz"], list(iter(generator)))

    def test_glue_is_generator(self):
        glue = ChildGenerator()
        glue.append(u", ")
        generator = JoinGenerator(glue, [u"foo", u"bar", u"baz"])
        assert_equal([b"foo", b", ", b"bar", b", ", b"baz"],
                     list(iter(generator)))


class HTMLJoinGeneratorTest(TestCase):

    def test_no_pieces(self):
        generator = HTMLJoinGenerator(u"!")
        assert_equal([], list(iter(generator)))

    def test_supplied_pieces(self):
        generator = HTMLJoinGenerator(u"&", [u"<foo>", u"bar"])
        assert_equal([b"&lt;foo&gt;", b"&amp;", b"bar"], list(iter(generator)))

    def test_append_extend(self):
        generator = HTMLJoinGenerator(u"!", [u"foo"])
        generator.append(u"<bar>")
        sub_generator = ChildGenerator()
        sub_generator.append(u"<baz>")
        generator.extend([sub_generator])
        assert_equal([b"foo", b"!", b"&lt;bar&gt;", b"!", b"<baz>"],
                     list(iter(generator)))

    def test_glue_is_generator(self):
        glue = ChildGenerator()
        glue.append(u"<")
        generator = JoinGenerator(glue, [u"foo", u"bar", u"baz"])
        assert_equal([b"foo", b"<", b"bar", b"<", b"baz"],
                     list(iter(generator)))

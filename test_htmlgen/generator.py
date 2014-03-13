from unittest import TestCase

from asserts import assert_equal

from htmlgen.generator import (Generator,
                               NullGenerator,
                               ChildGenerator,
                               HTMLChildGenerator,
                               JoinGenerator,
                               HTMLJoinGenerator)


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
        generator = _TestingGenerator(["foo", "bar", "baz"])
        assert_equal(["foo", "bar", "baz"], list(iter(generator)))

    def test_generate_sub_generators(self):
        inner1 = _TestingGenerator(["bar"])
        inner2 = _TestingGenerator(["foo", inner1])
        generator = _TestingGenerator([inner2, "baz"])
        assert_equal(["foo", "bar", "baz"], list(iter(generator)))

    def test_str(self):
        inner = _TestingGenerator(["bar"])
        generator = _TestingGenerator(["foo", inner, "baz"])
        assert_equal("foobarbaz", str(generator))


class NullGeneratorTest(TestCase):
    
    def test_generate(self):
        assert_equal([], list(iter(NullGenerator())))


class ChildGeneratorTest(TestCase):

    def test_append(self):
        generator = ChildGenerator()
        generator.append("c1")
        generator.append(_TestingGenerator(["c2", "c3"]))
        assert_equal(["c1", "c2", "c3"], list(iter(generator)))

    def test_extend(self):
        generator = ChildGenerator()
        generator.append("c1")
        generator.extend([_TestingGenerator(["c2", "c3"]), "c4"])
        assert_equal(["c1", "c2", "c3", "c4"], list(iter(generator)))

    def test_len(self):
        generator = ChildGenerator()
        generator.append("c1")
        generator.extend(["c2", "c3", NullGenerator()])
        assert_equal(4, len(generator))

    def test_empty(self):
        generator = ChildGenerator()
        generator.append("c1")
        generator.extend(["c2", "c3", NullGenerator()])
        generator.empty()
        assert_equal([], list(iter(generator)))


class HTMLChildGeneratorTest(TestCase):

    def test_append(self):
        generator = HTMLChildGenerator()
        generator.append("c1&c2")
        generator.append(_TestingGenerator(["c3", "<c4>"]))
        assert_equal(["c1&amp;c2", "c3", "<c4>"], list(iter(generator)))

    def test_append_raw(self):
        generator = HTMLChildGenerator()
        generator.append_raw("c1&c2")
        generator.append_raw(_TestingGenerator(["c3", "<c4>"]))
        assert_equal(["c1&c2", "c3", "<c4>"], list(iter(generator)))

    def test_extend(self):
        generator = HTMLChildGenerator()
        generator.append("c1")
        generator.extend([_TestingGenerator(["c2", "c&3"]), "<c4>"])
        assert_equal(["c1", "c2", "c&3", "&lt;c4&gt;"], list(iter(generator)))

    def test_extend_raw(self):
        generator = HTMLChildGenerator()
        generator.append("c1")
        generator.extend_raw([_TestingGenerator(["c&2", "c3"]), "<c4>"])
        assert_equal(["c1", "c&2", "c3", "<c4>"], list(iter(generator)))

    def test_len(self):
        generator = ChildGenerator()
        generator.append("c1")
        generator.extend(["c2", "c3", NullGenerator()])
        assert_equal(4, len(generator))

    def test_empty(self):
        generator = ChildGenerator()
        generator.append("c1")
        generator.extend(["c2", "c3", NullGenerator()])
        generator.empty()
        assert_equal([], list(iter(generator)))


class JoinGeneratorTest(TestCase):

    def test_no_pieces(self):
        generator = JoinGenerator("!")
        assert_equal([], list(iter(generator)))

    def test_supplied_pieces(self):
        generator = JoinGenerator("!", ["foo", "bar"])
        assert_equal(["foo", "!", "bar"], list(iter(generator)))

    def test_append_extend(self):
        generator = JoinGenerator("!", ["foo"])
        generator.append("bar")
        sub_generator = ChildGenerator()
        sub_generator.append("baz")
        generator.extend([sub_generator])
        assert_equal(["foo", "!", "bar", "!", "baz"], list(iter(generator)))


class HTMLJoinGeneratorTest(TestCase):

    def test_no_pieces(self):
        generator = HTMLJoinGenerator("!")
        assert_equal([], list(iter(generator)))

    def test_supplied_pieces(self):
        generator = HTMLJoinGenerator("&", ["<foo>", "bar"])
        assert_equal(["&lt;foo&gt;", "&amp;", "bar"], list(iter(generator)))

    def test_append_extend(self):
        generator = HTMLJoinGenerator("!", ["foo"])
        generator.append("<bar>")
        sub_generator = ChildGenerator()
        sub_generator.append("<baz>")
        generator.extend([sub_generator])
        assert_equal(["foo", "!", "&lt;bar&gt;", "!", "<baz>"],
                     list(iter(generator)))

from unittest import TestCase

from asserts import assert_equal

from htmlgen import (Section, Article, Navigation, Aside, Header, Footer,
                     Heading)


class SectionTest(TestCase):

    def test_element(self):
        section = Section()
        assert_equal([b"<section>", b"</section>"], list(iter(section)))


class ArticleTest(TestCase):

    def test_element(self):
        section = Article()
        assert_equal([b"<article>", b"</article>"], list(iter(section)))


class NavigationTest(TestCase):

    def test_element(self):
        section = Navigation()
        assert_equal([b"<nav>", b"</nav>"], list(iter(section)))


class AsideTest(TestCase):

    def test_element(self):
        section = Aside()
        assert_equal([b"<aside>", b"</aside>"], list(iter(section)))


class HeaderTest(TestCase):

    def test_element(self):
        section = Header()
        assert_equal([b"<header>", b"</header>"], list(iter(section)))


class FooterTest(TestCase):

    def test_element(self):
        section = Footer()
        assert_equal([b"<footer>", b"</footer>"], list(iter(section)))


class HeadingTest(TestCase):

    def test_without_initial_content(self):
        highlight = Heading(3)
        highlight.append("Test")
        assert_equal([b"<h3>", b"Test", b"</h3>"], list(iter(highlight)))

    def test_with_initial_content(self):
        highlight = Heading(2, "Initial", "test")
        highlight.append("content")
        assert_equal([b"<h2>", b"Initial", b"test", b"content", b"</h2>"],
                     list(iter(highlight)))

    def test_default_depth(self):
        highlight = Heading()
        highlight.append("Test")
        assert_equal([b"<h1>", b"Test", b"</h1>"], list(iter(highlight)))

import sys

if sys.version_info[0] < 3:
    from cgi import escape
else:
    from html import escape


# TODO: Python 3: remove
if sys.version_info[0] >= 3:
    unicode = str


class Generator(object):

    """Base class for HTML generators.

    Sub-classes must implement the generate() method, which returns an
    iterable containing strings and further generator objects. __iter__()
    flattens this iterator and returns a list of UTF-8 encoded byte strings:

        >>> class InnerGenerator(Generator):
        ...     def generate(self):
        ...         yield "XXX"
        >>> class OuterGenerator(Generator):
        ...     def generate(self):
        ...         yield "Foo"
        ...         yield InnerGenerator()
        >>> generator = OuterGenerator()
        >>> list(iter(generator))
        [b'Foo', b'XXX']

    __str__() returns a concatenated version of the strings returned by
    __iter__():

        >>> str(generator)
        'FooXXX'

    """

    def __iter__(self):
        """Return a flat iterator over the elements returned by generate().

        __iter__() will only return UTF-8 encoded byte strings. Generators are
        flattened, Unicode strings are UTF-8 encoded.

        """
        self._iterator_stack = [self.generate()]
        while self._iterator_stack:
            iterator = self._iterator_stack[-1]
            try:
                item = next(iterator)
            except StopIteration:
                self._iterator_stack.pop()
            else:
                if hasattr(item, "generate"):
                    self._iterator_stack.append(item.generate())
                elif isinstance(item, bytes):
                    yield item
                elif isinstance(item, unicode):
                    yield item.encode("utf-8")
                else:
                    raise TypeError("can not generate {}".format(repr(item)))

    def __str__(self):
        """Return a concatenation of the strings returned by __iter__()."""
        return "".join(s.decode("utf-8") for s in self)

    def generate(self):
        """To be overridden by sub-classes. Return an iterator over strings,
        UTF-8-encoded bytes, and generator objects.

        """
        raise NotImplementedError()


class NullGenerator(Generator):

    """A generator that generates nothing."""

    def generate(self):
        return iter([])


class IteratorGenerator(Generator):

    """A generator that generates an item per item of an iterator.

        >>> generator = IteratorGenerator(["foo", "bar"])
        >>> list(iter(generator))
        [b'foo', b'bar']

    """

    def __init__(self, iterator):
        super(IteratorGenerator, self).__init__()
        self._iterator = iterator

    def generate(self):
        for item in self._iterator:
            yield item


class ChildGenerator(Generator):

    """A generator that generates children appended to it.

        >>> generator = ChildGenerator()
        >>> generator.append("String")
        >>> generator.extend(["Lis", "t"])
        >>> list(iter(generator))
        [b'String', b'Lis', b't']
        >>> sub_generator = ChildGenerator()
        >>> sub_generator.append("Sub")
        >>> generator.append(sub_generator)
        >>> list(iter(generator))
        [b'String', b'Lis', b't', b'Sub']

    """

    def __init__(self):
        super(ChildGenerator, self).__init__()
        self._children = []

    def __len__(self):
        """Return the number of children.

        This is not the number of items returned by __iter__.

        """
        return len(self._children)

    def append(self, child):
        """Append a string or sub generator."""
        if child is None:
            raise TypeError("child can not be None")
        self._children.append(child)

    def extend(self, children):
        """Append multiple strings and sub generators."""
        if any(child is None for child in children):
            raise TypeError("child can not be None")
        self._children.extend(children)

    def remove(self, child):
        """Remove a string or sub-generator.

        If the string or sub-generator is not found, raises a ValueError.

        """
        self._children.remove(child)

    def empty(self):
        """Remove all children."""
        self._children = []

    @property
    def children(self):
        """Return a copy of the list of children."""
        return self._children[:]

    def generate(self):
        """Return an iterator over all children, in order.

        Sub-classes are encouraged to override or enhance this method,
        if desired.

        """
        return iter(self._children)


class HTMLChildGenerator(Generator):

    """A generator that handles HTML safely.

    HTMLChildGenerator works similar to ChildGenerator, but reserved HTML
    characters in strings appended with append() or extend() are
    escaped:

        >>> generator = HTMLChildGenerator()
        >>> generator.append("<Test>")
        >>> generator.extend(["x", "&", "y"])
        >>> list(iter(generator))
        [b'&lt;Test&gt;', b'x', b'&amp;', b'y']

    It is also possible to append strings without processing:

        >>> generator = HTMLChildGenerator()
        >>> generator.append_raw("<Test>")
        >>> generator.extend_raw(["x", "&", "y"])
        >>> list(iter(generator))
        [b'<Test>', b'x', b'&', b'y']

    Strings in sub-generators are not affected:

        >>> sub_generator = ChildGenerator()
        >>> sub_generator.append("<sub>")
        >>> generator = HTMLChildGenerator()
        >>> generator.extend(["<base>", sub_generator])
        >>> list(iter(generator))
        [b'&lt;base&gt;', b'<sub>']

    """

    def __init__(self):
        super(HTMLChildGenerator, self).__init__()
        self._children = ChildGenerator()

    def __len__(self):
        """Return the number of children.

        This is not the number of items returned by __iter__.

        """
        return len(self._children)

    def append(self, child):
        """Append a string or sub generator.

        Strings are escaped to be HTML-safe.

        """
        if not hasattr(child, "generate"):
            child = escape(child)
        self.append_raw(child)

    def append_raw(self, child):
        """Append a string or sub generator without escaping it.

        Strings are NOT escaped! Therefore, you should use this method only
        with HTML from trusted sources.

        """
        self._children.append(child)

    def extend(self, children):
        """Append multiple strings and sub generators.

        Strings are escaped to be HTML-safe.

        """
        for child in children:
            self.append(child)

    def extend_raw(self, children):
        """Append multiple strings and sub generators, without escaping them.

        Strings are NOT escaped! Therefore, you should use this method only
        with HTML from trusted sources.

        """
        for child in children:
            self.append_raw(child)

    def remove(self, child):
        """Remove a string or sub-generator.

        If child is a string, it will be HTML-escaped before trying to
        remove it. Use this method for strings added with append() or
        extend().

        If the string or sub-generator is not found, raises a ValueError.

        """
        # if not hasattr(child, "generate"):
        if not hasattr(child, "generate"):
            child = escape(child)
        self._children.remove(child)

    def remove_raw(self, child):
        """Remove a string or sub-generator.

        If child is a string, it will not be HTML-escaped before trying to
        remove it. Use this method for strings added with append_raw() or
        extend_raw().

        If the string or sub-generator is not found, raises a ValueError.

        """
        self._children.remove(child)

    def empty(self):
        """Remove all children."""
        self._children.empty()

    @property
    def children(self):
        """Return a copy of the list of children.

        String children are already HTML-escaped.

        """
        return self._children.children

    def generate(self):
        """Return an iterator over all children, in order.

        Sub-classes are encouraged to override or enhance this method,
        if desired.

        """
        return self._children.generate()


def generate_html_string(s):
    """Wrap a string in a HTMLChildGenerator.

    >>> for s in generate_html_string("Test String"):
    ...     print(s)
    b'Test String'

    This will escape the string:

    >>> str(generate_html_string("<foo>"))
    '&lt;foo&gt;'

    If s is already a generator is will not get wrapped:

    >>> other_gen = IteratorGenerator("foo")
    >>> gen = generate_html_string(other_gen)
    >>> gen is other_gen
    True

    """
    if hasattr(s, "generate"):
        return s
    gen = HTMLChildGenerator()
    gen.append(s)
    return gen


class JoinGenerator(ChildGenerator):

    """Generate the supplied pieces, separated by glue.

        >>> generator = JoinGenerator(", ", ["Hello", "World"])
        >>> list(iter(generator))
        [b'Hello', b', ', b'World']

    Pieces can be strings or sub-generators:

        >>> generator = JoinGenerator(", ", ["Hello"])
        >>> sub_generator = ChildGenerator()
        >>> sub_generator.append("World")
        >>> generator.append(sub_generator)
        >>> list(iter(generator))
        [b'Hello', b', ', b'World']

    """

    def __init__(self, glue, pieces=None):
        super(JoinGenerator, self).__init__()
        self._glue = glue
        if pieces:
            self.extend(pieces)

    def generate(self):
        pieces = super(JoinGenerator, self).generate()
        first = True
        for piece in pieces:
            if not first:
                yield self._glue
            yield piece
            first = False


class HTMLJoinGenerator(HTMLChildGenerator):

    """Generate the supplied pieces, separated by glue.

    This works like JoinGenerator, but reserved HTML characters in glue and
    string pieces are escaped. Sub-generators are not escaped:

        >>> generator = HTMLJoinGenerator(" & ", ["<Hello>"])
        >>> sub_generator = ChildGenerator()
        >>> sub_generator.append("<World>")
        >>> generator.append(sub_generator)
        >>> list(iter(generator))
        [b'&lt;Hello&gt;', b' &amp; ', b'<World>']

    """

    def __init__(self, glue, pieces=None):
        super(HTMLJoinGenerator, self).__init__()
        self._glue = escape(glue)
        if pieces:
            self.extend(pieces)

    def generate(self):
        pieces = super(HTMLJoinGenerator, self).generate()
        first = True
        for piece in pieces:
            if not first:
                yield self._glue
            yield piece
            first = False

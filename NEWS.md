# News in version 2.0.0

## API Additions

* Add `Video` element.
* Add `Button.disabled`.
* Add `autocomplete` attribute to `Input`, `TextArea`, `Select`, and `Form`.
* Add `enum_attribute`.

## Incompatible Changes

* Drop support for Python 2.7 and 3.4.

# News in version 1.2.2

## API Additions

* Add `GenValue` and `GenValueGenerator` to `htmlgen`.

# News in version 1.2.1

## API Additions

* `from htmlgen import ElementBase` now works.

## Bug Fixes

* Add missing `ElementBase` to type stubs.

# News in version 1.2.0

## API Additions

* Make `ElementBase` public.
* Add `GenValue` and `GenValueGenerator` type aliases.
* Fix annotation of `Heading`.

# News in version 1.1.0

## Improvements

* PEP 561 support.
* Improve type hints.

# News in version 1.0.0

No changes.

# News in version 0.99.3

## API-Incompatible Changes

* Revert deriving from ABC classes.

# News in version 0.99.2

## API Additions

* `Element.data` does now derive from MutableMapping and implements all its
  methods.

## Improvements

* Derive `ChildGenerator`, `HTMLChildGenerator`, and `Element` from
  Sized.

## Bug Fixes

* Fix a few stubs.
* Fix incorrect usage of `AnyStr`.

# News in version 0.99.1

## API-Incompatible Changes

* `html_attribute()` at al. are now directly implemented using the descriptor
  protocol, and not derived from property.

## Improvements

* Add stub files.

# News in version 0.99.0

First Beta Release

## API Additions

* Add generate_html_string().
* Add css_class_attribute().
* Add Checkbox (&lt;input type="checkbox"&gt;), RadioButton (&lt;input type="radio"&gt;),
  and Label (&lt;label&gt;).

## API-Incompatible Changes

* Remove html_attribute() from htmlgen.element.

## Improvements

* Render CSS classes alphabetically for easier unit testing.

## Bug Fixes

* Fix PendingDeprecationWarnings.

# News in version 0.9

## API Additions

* Add IteratorGenerator.
* Add HiddenInput (&lt;input type="hidden"&gt;), FileInput (&lt;input type="file"&gt;),
  SearchInput (&lt;input type="search"&gt;), and TimeInput (&lt;input type="time"&gt;).
* Add LineBreak (&lt;br&gt;).
* Table now has two overridable generator methods generate_header_rows() and
  generate_rows().
* Add TextArea.placeholder property.
* Add NumberInput.number property.
* Add Form.target property and Form.set_blank_target().
* Add data_attribute(), list_html_attribute() and time_html_attribute().

## API-Incompatible Changes

* Improve Element.id handling and raise ValueError on invalid ids.
* The default name of all input elements has been changed from None to the
  empty string to match Input.name.
* NumberInput constructor: Replace value argument by number.

# News in version 0.8

## API Additions

* Add form elements TextArea (&lt;textarea&gt;), Select (&lt;select&gt;), OptionGroup
  (&lt;optgroup&gt;), and Option (&lt;option&gt;).
* Add is_element() to check whether an object is an element generator of
  a certain type.
* Forms now support multipart submissions using the Form.encryption_type and
  Form.multipart attributes.

## API-Incompatible Changes

* Fix the default HTTP method to be "GET" for forms as per HTML spec. This
  avoids unexpected behaviour and the need for problematic workarounds
  with "POST" forms.

# News in version 0.7

## API Additions

* Add input elements Button (&lt;button&gt;), NumberInput (&lt;input type="number"&gt;),
  PasswordInput (&lt;input type="password"&gt;), and DateInput (&lt;input
  type="date"&gt;).

## API-Incompatible Changes

* Move attribute functions from htmlgen.elements to htmlgen.attribute.
  (But you should import them directly from htmlgen anyway.)

## Improvements

* Improved error handling and reporting.

## Documentation

* Add element list document elements.rst.

## Bug Fixes

* Add float_html_attribute to htmlgen.

# News in version 0.6.1

## Bug Fixes

* Fixed error when passing elements to TableCell's and TableHeaderCell's
  constructor.

# News in version 0.6

## API Additions

* Add TableHeaderCell to htmlgen (missing from 0.5).
* Division constructor now accepts initial content arguments.

## API-Incompatible Changes

* All element constructors that took an initial content argument now take
  any number of content arguments, i.e. the following is now possible:
  &gt;&gt;&gt; Paragraph("This is ", Emphasis("initial"), " content.")

# News in version 0.5

## API Additions

* Add table elements Table (&lt;table&gt;), TableHead (&lt;thead&gt;),
  TableBody (&lt;tbody&gt;), TableRow (&lt;tr&gt;), TableHeaderCell (&lt;th&gt;),
  TableCell (&lt;td&gt;), ColumnGroup (&lt;colgroup&gt;), and Column (&lt;col&gt;).

# News in version 0.4

## API Additions

* Add data property to element classes. This provides an API to
  easily set and query data-* attributes.
* Add structural element Article (&lt;article&gt;).
* Add inline elements Link (&lt;a&gt;) and Time (&lt;time&gt;).
* Add description list elements DescriptionList (&lt;dl&gt;),
  DescriptionTerm (&lt;dt&gt;), and DescriptionDefinition (&lt;dd&gt;).

# News in version 0.3

## API Additions

* Add child-management methods and properties to ChildGenerator and
  HTMLChildGenerator:
  * remove()
  * remove_raw() (HTMLChildGenerator only)
  * children
* Add new base class NonVoidElement, derive Element from this class.
  This base class can be used for elements with content that do not
  support the usual container interface.
* Add document-level elements Document, HTMLRoot (&lt;html&gt;), Head (&lt;head&gt;),
  Body (&lt;body&gt;), Title (&lt;title&gt;), Meta (&lt;meta&gt;), Script (&lt;script&gt;),
  HeadLink (&lt;link&gt;), and Main (&lt;main&gt;).
* Add structural elements Section (&lt;section&gt;), Navigation (&lt;nav&gt;),
  Aside (&lt;aside&gt;), Header (&lt;header&gt;), Footer (&lt;footer&gt;), and Heading
  (&lt;h1&gt; to &lt;h6&gt;).
* Add list elements OrderedList (&lt;ol&gt;), UnorderedList (&lt;ul&gt;), and
  ListItem (&lt;li&gt;).
* Add has_css_class() method to elements.

## Improvements

* Element attributes are now always rendered in alphabetical order. This
  makes testing elements easier.

# News in version 0.2

## API Additions

* Add elements Paragraph (&lt;p&gt;), Preformatted (&lt;pre&gt;), Image (&lt;img&gt;),
  Highlight (&lt;b&gt;), Strong (&lt;strong&gt;), Alternate (&lt;i&gt;), Emphasis (&lt;em&gt;),
  and Small (&lt;small&gt;).
* Add float_html_attribute().
* Add remove_css_classes() method to elements.

## API-Incompatible Changes

* Rename ShortElement to VoidElement to conform to the HTML 5 standard.

# News in version 0.1.1

## API Additions

* Add ShortElement to htmlgen.

## Bug Fixes

* Elements are now always truthy.

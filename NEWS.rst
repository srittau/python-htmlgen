News in version 0.99.3
======================

News in version 0.99.2
======================

API Additions
-------------

* ``Element.data`` does now derive from MutableMapping and implements all its
  methods.

Improvements
------------

* Derive ``ChildGenerator``, ``HTMLChildGenerator``, and ``Element`` from
  Sized.

Bug Fixes
---------

* Fix a few stubs.
* Fix incorrect usage of ``AnyStr``.

News in version 0.99.1
======================

API-Incompatible Changes
------------------------

* ``html_attribute()`` at al. are now directly implemented using the descriptor
  protocol, and not derived from property.

Improvements
------------

* Add stub files.

News in version 0.99.0
======================

First Beta Release

API Additions
-------------

* Add generate_html_string().
* Add css_class_attribute().
* Add Checkbox (<input type="checkbox">), RadioButton (<input type="radio">),
  and Label (<label>).

API-Incompatible Changes
------------------------

* Remove html_attribute() from htmlgen.element.

Improvements
------------

* Render CSS classes alphabetically for easier unit testing.

Bug Fixes
---------

* Fix PendingDeprecationWarnings.

News in version 0.9
===================

API Additions
-------------

* Add IteratorGenerator.
* Add HiddenInput (<input type="hidden">), FileInput (<input type="file">),
  SearchInput (<input type="search">), and TimeInput (<input type="time">).
* Add LineBreak (<br>).
* Table now has two overridable generator methods generate_header_rows() and
  generate_rows().
* Add TextArea.placeholder property.
* Add NumberInput.number property.
* Add Form.target property and Form.set_blank_target().
* Add data_attribute(), list_html_attribute() and time_html_attribute().

API-Incompatible Changes
------------------------

* Improve Element.id handling and raise ValueError on invalid ids.
* The default name of all input elements has been changed from None to the
  empty string to match Input.name.
* NumberInput constructor: Replace value argument by number.

News in version 0.8
===================

API Additions
-------------

* Add form elements TextArea (<textarea>), Select (<select>), OptionGroup
  (<optgroup>), and Option (<option>).
* Add is_element() to check whether an object is an element generator of
  a certain type.
* Forms now support multipart submissions using the Form.encryption_type and
  Form.multipart attributes.

API-Incompatible Changes
------------------------

* Fix the default HTTP method to be "GET" for forms as per HTML spec. This
  avoids unexpected behaviour and the need for problematic workarounds
  with "POST" forms.

News in version 0.7
===================

API Additions
-------------

* Add input elements Button (<button>), NumberInput (<input type="number">),
  PasswordInput (<input type="password">), and DateInput (<input
  type="date">).

API-Incompatible Changes
------------------------

* Move attribute functions from htmlgen.elements to htmlgen.attribute.
  (But you should import them directly from htmlgen anyway.)

Improvements
------------

* Improved error handling and reporting.

Documentation
-------------

* Add element list document elements.rst.

Bug Fixes
---------

* Add float_html_attribute to htmlgen.

News in version 0.6.1
=====================

Bug Fixes
---------

* Fixed error when passing elements to TableCell's and TableHeaderCell's
  constructor.

News in version 0.6
===================

API Additions
-------------

* Add TableHeaderCell to htmlgen (missing from 0.5).
* Division constructor now accepts initial content arguments.

API-Incompatible Changes
------------------------

* All element constructors that took an initial content argument now take
  any number of content arguments, i.e. the following is now possible:
  >>> Paragraph("This is ", Emphasis("initial"), " content.")

News in version 0.5
===================

API Additions
-------------

* Add table elements Table (<table>), TableHead (<thead>),
  TableBody (<tbody>), TableRow (<tr>), TableHeaderCell (<th>),
  TableCell (<td>), ColumnGroup (<colgroup>), and Column (<col>).

News in version 0.4
===================

API Additions
-------------

* Add data property to element classes. This provides an API to
  easily set and query data-* attributes.
* Add structural element Article (<article>).
* Add inline elements Link (<a>) and Time (<time>).
* Add description list elements DescriptionList (<dl>),
  DescriptionTerm (<dt>), and DescriptionDefinition (<dd>).

News in version 0.3
===================

API Additions
-------------

* Add child-management methods and properties to ChildGenerator and
  HTMLChildGenerator:
  * remove()
  * remove_raw() (HTMLChildGenerator only)
  * children
* Add new base class NonVoidElement, derive Element from this class.
  This base class can be used for elements with content that do not
  support the usual container interface.
* Add document-level elements Document, HTMLRoot (<html>), Head (<head>),
  Body (<body>), Title (<title>), Meta (<meta>), Script (<script>),
  HeadLink (<link>), and Main (<main>).
* Add structural elements Section (<section>), Navigation (<nav>),
  Aside (<aside>), Header (<header>), Footer (<footer>), and Heading
  (<h1> to <h6>).
* Add list elements OrderedList (<ol>), UnorderedList (<ul>), and
  ListItem (<li>).
* Add has_css_class() method to elements.

Improvements
------------

* Element attributes are now always rendered in alphabetical order. This
  makes testing elements easier.

News in version 0.2
===================

API Additions
-------------

* Add elements Paragraph (<p>), Preformatted (<pre>), Image (<img>),
  Highlight (<b>), Strong (<strong>), Alternate (<i>), Emphasis (<em>),
  and Small (<small>).
* Add float_html_attribute().
* Add remove_css_classes() method to elements.

API-Incompatible Changes
------------------------

* Rename ShortElement to VoidElement to conform to the HTML 5 standard.

News in version 0.1.1
=====================

API Additions
-------------

* Add ShortElement to htmlgen.

Bug Fixes
---------

* Elements are now always truthy.

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

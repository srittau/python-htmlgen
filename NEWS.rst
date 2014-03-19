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

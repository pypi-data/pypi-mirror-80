sphinx-markdown-parser
======================

A ``docutils``-compatibility bridge to MarkdownParser and CommonMark.

This allows you to write markdown inside of docutils & sphinx projects.

This was built due to limitations of the existing markdown parsers
supported by sphinx, specifically recommonmark. Features such as support
for tables have been added to this extension.

Contents
--------

-  `API Reference <api_ref.md>`__
-  `AutoStructify Component <auto_structify.md>`__

Recommended Projects
--------------------

-  `sphinx-markdown-builder <https://github.com/codejamninja/sphinx-markdown-builder>`__
   - sphinx builder that outputs markdown files

Parsers
-------

The ``MarkdownParser`` is the recommonend parser for the following
reasons. \* It has more features such as tables and extensions \* It is
the parser officially supported by this project

If you insist on using the ``CommonMarkParser`` I recommnend using
`recommonmark <https://github.com/readthedocs/recommonmark>`__ directly
since we do not officially support that parser.

==================== ===========================================
**Parser**           **Source**
==================== ===========================================
``MarkdownParser``   https://github.com/Python-Markdown/markdown
``CommonMarkParser`` https://github.com/readthedocs/recommonmark
==================== ===========================================

Getting Started
---------------

To use ``sphinx-markdown-parser`` inside of Sphinx only takes 2 steps.
First you install it:

::

   pip install sphinx-markdown-parser

If using MarkdownParser, you may also want to install some extensions
for it:

::

   pip install pymdown-extensions

Then add this to your Sphinx conf.py:

::

   # for MarkdownParser
   from sphinx_markdown_parser.parser import MarkdownParser

   def setup(app):
       app.add_source_suffix('.md', 'markdown')
       app.add_source_parser(MarkdownParser)
       app.add_config_value('markdown_parser_config', {
           'auto_toc_tree_section': 'Content',
           'enable_auto_doc_ref': True,
           'enable_auto_toc_tree': True,
           'enable_eval_rst': True,
           'extensions': [
               'extra',
               'nl2br',
               'sane_lists',
               'smarty',
               'toc',
               'wikilinks',
               'pymdownx.arithmatex',
           ],
       }, True)

   # for CommonMarkParser
   from recommonmark.parser import CommonMarkParser

   def setup(app):
       app.add_source_suffix('.md', 'markdown')
       app.add_source_parser(CommonMarkParser)
       app.add_config_value('markdown_parser_config', {
           'auto_toc_tree_section': 'Content',
           'enable_auto_doc_ref': True,
           'enable_auto_toc_tree': True,
           'enable_eval_rst': True,
           'enable_inline_math': True,
           'enable_math': True,
       }, True)

In order to use reStructuredText in Markdown (for `enable_eval_rst` to work properly), you must add AutoStructify 
in ``conf.py``
::
  # At top on conf.py
  from sphinx_markdown_parser.transform import AutoStructify

  # in setup function after configuration of the parser
  app.add_transform(AutoStructify)

This allows you to write both ``.md`` and ``.rst`` files inside of the
same project.

Links
~~~~~

For all links in commonmark that aren’t explicit URLs, they are treated
as cross references with the
```:any:`` <http://www.sphinx-doc.org/en/stable/markup/inline.html#role-any>`__
role. This allows referencing a lot of things including files, labels,
and even objects in the loaded domain.

AutoStructify
~~~~~~~~~~~~~

AutoStructify makes it possible to write your documentation in Markdown,
and automatically convert this into rST at build time. See `the
AutoStructify
Documentation <http://recommonmark.readthedocs.org/en/latest/auto_structify.html>`__
for more information about configuration and usage.

To use the advanced markdown to rst transformations you must add
``AutoStructify`` to your Sphinx conf.py.

.. code:: python

   # At top on conf.py (with other import statements)
   from sphinx_markdown_parser.transform import AutoStructify

   # At the bottom of conf.py
   def setup(app):
       app.add_config_value('markdown_parser_config', {
               'url_resolver': lambda url: github_doc_root + url,
               'auto_toc_tree_section': 'Contents',
               }, True)
       app.add_transform(AutoStructify)

See https://github.com/rtfd/recommonmark/blob/master/docs/conf.py for a
full example.

AutoStructify comes with the following options. See
http://recommonmark.readthedocs.org/en/latest/auto_structify.html for
more information about the specific features.

-  **enable_auto_toc_tree**: enable the Auto Toc Tree feature.
-  **auto_toc_tree_section**: when True, Auto Toc Tree will only be
   enabled on section that matches the title.
-  **enable_auto_doc_ref**: enable the Auto Doc Ref feature.
   **Deprecated**
-  **enable_math**: enable the Math Formula feature.
-  **enable_inline_math**: enable the Inline Math feature.
-  **enable_eval_rst**: enable the evaluate embedded reStructuredText
   feature.
-  **url_resolver**: a function that maps a existing relative position
   in the document to a http link

Development
-----------

You can run the tests by running ``tox`` in the top-level of the
project.

We are working to expand test coverage, but this will at least test
basic Python 2 and 3 compatability.

Why a bridge?
-------------

Many python tools (mostly for documentation creation) rely on
``docutils``. But
`docutils <http://docutils.sourceforge.net/docs/ref/doctree.html>`__
only supports a ReStructuredText syntax.

For instance `this
issue <https://bitbucket.org/birkenfeld/sphinx/issue/825/markdown-capable-sphinx>`__
and `this StackOverflow
question <http://stackoverflow.com/questions/2471804/using-sphinx-with-markdown-instead-of-rst>`__
show that there is an interest in allowing ``docutils`` to use markdown
as an alternative syntax.

Why another bridge to docutils?
-------------------------------

recommonmark uses the `python
implementation <https://github.com/rtfd/CommonMark-py>`__ of
`CommonMark <http://commonmark.org>`__ while
`remarkdown <https://github.com/sgenoud/remarkdown>`__ implements a
stand-alone parser leveraging
`parsley <https://github.com/python-parsley/parsley>`__.

Both output a ```docutils`` document
tree <http://docutils.sourceforge.net/docs/ref/doctree.html>`__ and
provide scripts that leverage ``docutils`` for generation of different
types of documents.

Acknowledgement
---------------

recommonmark is mainly derived from
`remarkdown <https://github.com/sgenoud/remarkdown>`__ by Steve Genoud
and leverages the python CommonMark implementation.

It was originally created by `Luca
Barbato <https://github.com/lu-zero>`__, and is now maintained in the
Read the Docs (rtfd) GitHub organization.

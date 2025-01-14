# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'Triplexicon'
copyright = '2024, SchulzLab'
author = 'Kalk'

release = '0.1'
version = '0.1.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'rst2pdf.pdfbuilder', 
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'

pdf_documents = [('index', u'TripLexiconDocs', u'TripLexiconDocs', u'Timothy Warwick, Christina Kalk'),]


sphinx-build -b pdf source build/pdf

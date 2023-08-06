project = "testplates"
author = "Krzysztof Przybyła"

language = "en"
master_doc = "index"
source_suffix = ".rst"
html_theme = "sphinx_rtd_theme"
templates_path = [".templates"]
html_static_path = [".static"]
autodoc_member_order = "bysource"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
]

# -*- coding: utf-8 -*-
# Sage introspection build configuration file.
# See sage.server.notebook.cell.set_introspect_html() for details.

import sys, os
sys.path.append(os.environ['SAGE_DOC'])
from common.conf import *

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.jsmath', 'sphinx.ext.todo']

templates_path = ['templates']
html_static_path = ['static']

html_use_modindex = False
html_use_index = False
html_split_index = False
html_copy_source = False

todo_include_todos = True

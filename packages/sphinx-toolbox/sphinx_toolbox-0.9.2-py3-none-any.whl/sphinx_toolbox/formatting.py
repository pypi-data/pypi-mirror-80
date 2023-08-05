#!/usr/bin/env python3
#
#  formatting.py
"""
Directives, roles and nodes for text formatting.

This can be used as a standalone Sphinx extension. Enable it by adding the following
to the ``extensions`` variable in your ``conf.py``:

.. extensions:: sphinx_toolbox.formatting
	:no-preamble:
	:no-postamble:

.. versionadded:: 0.2.0
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#
#  Parts of the docstrings based on https://docutils.sourceforge.io/docs/howto/rst-roles.html
#

# stdlib
from typing import Any, Dict, List, Tuple

# 3rd party
from docutils import nodes
from docutils.nodes import Node, system_message
from docutils.parsers.rst import roles
from sphinx.application import Sphinx
from sphinx.roles import Abbreviation
from sphinx.writers.html import HTMLTranslator
from sphinx.writers.latex import LaTeXTranslator

# this package
from sphinx_toolbox import __version__

__all__ = [
		"ItalicAbbreviationNode",
		"ItalicAbbreviation",
		"visit_iabbr_node",
		"depart_iabbr_node",
		"latex_visit_iabbr_node",
		"latex_depart_iabbr_node",
		"setup"
		]


class ItalicAbbreviationNode(nodes.abbreviation):
	"""
	Docutils Node to show an abbreviation in italics.

	.. versionadded:: 0.2.0
	"""


class ItalicAbbreviation(Abbreviation):
	"""
	Docutils role to show an abbreviation in italics.

	.. versionadded:: 0.2.0
	"""

	def run(self) -> Tuple[List[Node], List[system_message]]:
		"""
		Process the content of the italic abbreviation role.

		.. versionadded:: 0.2.0
		"""

		options = self.options.copy()  # type: ignore
		matched = self.abbr_re.search(self.text)  # type: ignore

		if matched:
			text = self.text[:matched.start()].strip()  # type: ignore
			options["explanation"] = matched.group(1)
		else:
			text = self.text

		return [ItalicAbbreviationNode(self.rawtext, text, **options)], []  # type: ignore


def visit_iabbr_node(translator: HTMLTranslator, node: ItalicAbbreviationNode):
	"""
	Visit an :class:`~.ItalicAbbreviationNode`.

	:param translator:
	:param node: The node being visited.

	.. versionadded:: 0.2.0
	"""

	translator.body.append('<i class="abbreviation">')
	attrs = {}

	if node.hasattr("explanation"):
		attrs["title"] = node["explanation"]

	translator.body.append(translator.starttag(node, "abbr", '', **attrs))


def depart_iabbr_node(translator: HTMLTranslator, node: ItalicAbbreviationNode):
	"""
	Depart an :class:`~.ItalicAbbreviationNode`.

	:param translator:
	:param node: The node being visited.

	.. versionadded:: 0.2.0
	"""

	translator.body.append("</i></abbr>")


def latex_visit_iabbr_node(translator: LaTeXTranslator, node: ItalicAbbreviationNode):
	"""
	Visit an :class:`~.ItalicAbbreviationNode`.

	:param translator:
	:param node: The node being visited.

	.. versionadded:: 0.2.0
	"""

	abbr = node.astext()
	translator.body.append(r"\textit{\sphinxstyleabbreviation{")

	# spell out the explanation once
	if node.hasattr("explanation") and abbr not in translator.handled_abbrs:
		translator.context.append(f'}} ({translator.encode(node["explanation"])})')
		translator.handled_abbrs.add(abbr)
	else:
		translator.context.append("}")


def latex_depart_iabbr_node(translator: LaTeXTranslator, node: ItalicAbbreviationNode):
	"""
	Depart an :class:`~.ItalicAbbreviationNode`.

	:param translator:
	:param node: The node being visited.

	.. versionadded:: 0.2.0
	"""

	translator.body.append(translator.context.pop())
	translator.body.append("}")


def setup(app: Sphinx) -> Dict[str, Any]:
	"""
	Setup :mod:`sphinx-toolbox.formatting`.

	:param app:

	:return:

	.. versionadded:: 0.2.0
	"""

	roles.register_local_role("iabbr", ItalicAbbreviation())
	app.add_node(
			ItalicAbbreviationNode,
			html=(visit_iabbr_node, depart_iabbr_node),
			latex=(latex_visit_iabbr_node, latex_depart_iabbr_node),
			)

	return {
			"version": __version__,
			"parallel_read_safe": True,
			}

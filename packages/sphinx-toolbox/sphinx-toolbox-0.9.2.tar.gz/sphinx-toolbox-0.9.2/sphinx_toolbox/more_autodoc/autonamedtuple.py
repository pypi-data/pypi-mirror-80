#!/usr/bin/env python3
#
#  autonamedtuple.py
r"""
A Sphinx directive for documenting :class:`NamedTuples <typing.NamedTuple>` in Python.

Provides the :rst:dir:`autonamedtuple` directive to document a :class:`typing.NamedTuple`.
It behaves much like :rst:dir:`autoclass` and :rst:dir:`autofunction`.

.. versionadded:: 0.8.0

See also https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html .
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
#  Parts based on https://github.com/sphinx-doc/sphinx
#  |  Copyright (c) 2007-2020 by the Sphinx team (see AUTHORS file).
#  |  BSD Licensed
#  |  All rights reserved.
#  |
#  |  Redistribution and use in source and binary forms, with or without
#  |  modification, are permitted provided that the following conditions are
#  |  met:
#  |
#  |  * Redistributions of source code must retain the above copyright
#  |   notice, this list of conditions and the following disclaimer.
#  |
#  |  * Redistributions in binary form must reproduce the above copyright
#  |   notice, this list of conditions and the following disclaimer in the
#  |   documentation and/or other materials provided with the distribution.
#  |
#  |  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  |  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  |  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  |  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  |  HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  |  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  |  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  |  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  |  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  |  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  |  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# stdlib
from textwrap import dedent
from typing import Any, Dict, List, Tuple

# 3rd party
from sphinx.application import Sphinx
from sphinx.domains import ObjType
from sphinx.domains.python import PyClasslike, PyXRefRole
from sphinx.ext.autodoc import ClassDocumenter, Documenter
from sphinx.locale import _
from sphinx.pycode import ModuleAnalyzer

# this package
from sphinx_toolbox import __version__
from sphinx_toolbox.more_autodoc.typehints import format_annotation
from sphinx_toolbox.more_autodoc.utils import is_namedtuple, parse_parameters

__all__ = ["NamedTupleDocumenter", "setup"]


class NamedTupleDocumenter(ClassDocumenter):
	r"""
	Sphinx autodoc :class:`~sphinx.ext.autodoc.Documenter`
	for documenting :class:`typing.NamedTuple`\s.

	.. versionadded:: 0.8.0
	"""  # noqa D400

	objtype = "namedtuple"
	directivetype = "namedtuple"
	priority = 20

	@classmethod
	def can_document_member(cls, member: Any, membername: str, isattr: bool, parent: Any) -> bool:
		"""
		Called to see if a member can be documented by this documenter.

		:param member:
		:param membername:
		:param isattr:
		:param parent:
		"""

		return is_namedtuple(member)

	def add_content(self, more_content: Any, no_docstring: bool = True):
		"""
		Add extra content (from docstrings, attribute docs etc.), but not the NamedTuple's docstring.

		:param more_content:
		:param no_docstring:
		"""

		Documenter.add_content(self, more_content, True)

	def add_directive_header(self, sig: str) -> None:
		"""
		Add the directive's header, and the inheritance information if the ``:"show-inheritance:`` flag set.

		:param sig: The NamedTuple's signature.
		"""

		super().add_directive_header(sig)

		if "show-inheritance" in self.options and self.directive.result[-1] == "   Bases: :class:`tuple`":
			if hasattr(self.object, "__annotations__"):
				self.directive.result[-1] = "   Bases: :class:`~typing.NamedTuple`"
			else:
				self.directive.result[-1] = "   Bases: :func:`~collections.namedtuple`"

	def sort_members(
			self,
			documenters: List[Tuple[Documenter, bool]],
			order: str,
			) -> List[Tuple[Documenter, bool]]:
		"""
		Sort the NamedTuple's members.

		:param documenters:
		:param order:

		:return:
		"""

		# The documenters for the fields and method, in the desired order
		# The fields will be in bysource order regardless of the order option
		documenters = super().sort_members(documenters, order)

		# Size varies depending on docutils config
		a_tab = " " * self.env.app.config.docutils_tab_width  # type: ignore

		# Mapping of member names to docstrings (as list of strings)
		member_docstrings = {
				k[1]: v
				for k, v in ModuleAnalyzer.for_module(self.object.__module__).find_attr_docs().items()
				}

		# set sourcename and add content from attribute documentation
		sourcename = self.get_sourcename()

		# Size varies depending on docutils config
		tab_size = self.env.app.config.docutils_tab_width  # type: ignore

		if self.object.__doc__:
			docstring = dedent(self.object.__doc__).expandtabs(tab_size).split("\n")
		else:
			docstring = [":class:`typing.NamedTuple`."]

		docstring = list(self.process_doc([docstring]))

		params, pre_output, post_output = parse_parameters(docstring, tab_size=tab_size)

		for line in pre_output:
			self.add_line(line, sourcename)

		self.add_line('', sourcename)

		self.add_line(":Fields:", sourcename)
		self.add_line('', sourcename)

		fields = self.object._fields

		for pos, field in enumerate(fields):
			doc: List[str] = ['']
			arg_type: str = ''

			# Prefer doc from class docstring
			if field in params:
				doc, arg_type = params.pop(field).values()  # type: ignore

			# Otherwise use attribute docstring
			if not ''.join(doc).strip() and field in member_docstrings:
				doc = member_docstrings[field]

			# Fallback to namedtuple's default docstring
			if not ''.join(doc).strip():
				doc = [getattr(self.object, field).__doc__]

			# Prefer annotations over docstring types
			if hasattr(self.object, "__annotations__"):
				if field in self.object.__annotations__:
					arg_type = format_annotation(self.object.__annotations__[field])

			field_entry = [f"{a_tab}{pos})", "|nbsp|", f"**{field}**"]
			if arg_type:
				field_entry.append(f"({arg_type}\\)")
			field_entry.append("--")
			field_entry.extend(doc)

			self.add_line(" ".join(field_entry), sourcename)

		self.add_line('', sourcename)

		for line in post_output:
			self.add_line(line, sourcename)

		self.add_line('', sourcename)

		# Remove documenters corresponding to fields and return the rest
		return [d for d in documenters if d[0].name.split(".")[-1] not in fields]


def setup(app: Sphinx) -> Dict[str, Any]:
	"""
	Setup :mod:`sphinx_toolbox.more_autodoc.autonamedtuple`.

	:param app:

	.. versionadded:: 0.8.0
	"""

	app.registry.domains["py"].object_types["namedtuple"] = ObjType(_("namedtuple"), "namedtuple", "class", "obj")
	app.add_directive_to_domain("py", "namedtuple", PyClasslike)
	app.add_role_to_domain("py", "namedtuple", PyXRefRole())

	app.add_autodocumenter(NamedTupleDocumenter)

	return {
			"version": __version__,
			"parallel_read_safe": True,
			}

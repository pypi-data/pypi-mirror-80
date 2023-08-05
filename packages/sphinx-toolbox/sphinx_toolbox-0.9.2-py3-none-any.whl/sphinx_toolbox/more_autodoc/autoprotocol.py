#!/usr/bin/env python3
#
#  autoprotocol.py
"""
A Sphinx directive for documenting :class:`Protocols <typing.Protocol` in Python.

Provides the :rst:dir:`autoprotocol` directive to document a :class:`typing.Protocol`.
It behaves much like :rst:dir:`autoclass` and :rst:dir:`autofunction`.

.. versionadded:: 0.2.0

.. versionchanged:: 0.6.0

	Moved from :mod:`sphinx_toolbox.autoprotocol`.

See also https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
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
import sys
from typing import Any, Callable, Dict, List, Tuple

# 3rd party
from sphinx.application import Sphinx
from sphinx.domains import ObjType
from sphinx.domains.python import PyClasslike, PyXRefRole
from sphinx.ext.autodoc import INSTANCEATTR, ClassDocumenter, member_order_option
from sphinx.locale import _
from sphinx.util.inspect import getdoc, safe_getattr

# this package
from sphinx_toolbox import __version__
from sphinx_toolbox.more_autodoc.utils import allow_subclass_add, filter_members_warning
from sphinx_toolbox.utils import flag

if sys.version_info < (3, 8):  # pragma: no cover (>=py38)
	# 3rd party
	from typing_extensions import _ProtocolMeta  # type: ignore
else:  # pragma: no cover (<py38)
	# stdlib
	from typing import _ProtocolMeta  # type: ignore

__all__ = ["ProtocolDocumenter", "setup"]

globally_excluded_methods = {
		"__dict__",
		"__class__",
		"__dir__",
		"__weakref__",
		"__module__",
		"__annotations__",
		"__orig_bases__",
		"__parameters__",
		"__subclasshook__",
		"__init_subclass__",
		"__attrs_attrs__",
		"__init__",
		"__getnewargs__",
		"__abstractmethods__",
		"__doc__",
		"__abstractmethods__",
		"__args__",
		"__class__",
		"__delattr__",
		"__dir__",
		"__extra__",
		"__module__",
		"__next_in_mro__",
		"__orig_bases__",
		"__origin__",
		"__parameters__",
		"__subclasshook__",
		"__tree_hash__",
		}

runtime_message = (
		"This protocol is `runtime checkable "
		"<https://www.python.org/dev/peps/pep-0544/#runtime-checkable-decorator-and-narrowing-types-by-isinstance>`_."
		)


class ProtocolDocumenter(ClassDocumenter):
	r"""
	Sphinx autodoc :class:`~sphinx.ext.autodoc.Documenter`
	for documenting :class:`typing.Protocol`\s.

	.. versionadded:: 0.2.0
	"""  # noqa D400

	objtype = "protocol"
	directivetype = "protocol"
	priority = 20
	option_spec: Dict[str, Callable] = {
			"noindex": flag,
			"member-order": member_order_option,
			'show-inheritance': flag,
			}

	@classmethod
	def can_document_member(cls, member: Any, membername: str, isattr: bool, parent: Any) -> bool:
		"""
		Called to see if a member can be documented by this documenter.

		:param member:
		:param membername:
		:param isattr:
		:param parent:
		"""

		# _is_protocol = True
		return isinstance(member, _ProtocolMeta)

	def format_signature(self, **kwargs: Any) -> str:
		"""
		Protocols do not have a signature.
		"""

		return ''  # pragma: no cover

	def add_content(self, more_content: Any, no_docstring: bool = False):
		"""
		Add the autodocumenter content.

		:param more_content:
		:param no_docstring:
		"""

		super().add_content(more_content=more_content, no_docstring=no_docstring)

		sourcename = self.get_sourcename()

		if not getdoc(self.object):
			self.add_line(":class:`typing.Protocol`.", sourcename)
			self.add_line('', sourcename)

		if hasattr(self.object, "_is_runtime_protocol") and self.object._is_runtime_protocol:
			self.add_line(runtime_message, sourcename)
			self.add_line('', sourcename)

		self.add_line("Classes that implement this protocol must have the following methods:", sourcename)
		self.add_line('', sourcename)

	def document_members(self, all_members: bool = False) -> None:
		"""
		Generate reST for member documentation.

		All members are always documented.
		"""

		super().document_members(True)

	def filter_members(
			self,
			members: List[Tuple[str, Any]],
			want_all: bool,
			) -> List[Tuple[str, Any, bool]]:
		"""
		Filter the given member list.

		:param members:
		:param want_all:
		"""

		ret = []

		# process members and determine which to skip
		for (membername, member) in members:
			# if isattr is True, the member is documented as an attribute

			if safe_getattr(member, "__sphinx_mock__", False):
				# mocked module or object
				keep = False

			elif self.options.exclude_members and membername in self.options.exclude_members:
				# remove members given by exclude-members
				keep = False

			elif membername.startswith('_') and not (membername.startswith("__") and membername.endswith("__")):
				keep = False

			elif membername not in globally_excluded_methods:
				# Magic method you wouldn't overload, or private method.
				if membername in dir(self.object.__base__):
					keep = member is not getattr(self.object.__base__, membername)
				else:
					keep = True

			else:
				keep = False

			# give the user a chance to decide whether this member
			# should be skipped
			if self.env.app:
				# let extensions preprocess docstrings
				try:
					skip_user = self.env.app.emit_firstresult(
							"autodoc-skip-member",
							self.objtype,
							membername,
							member,
							not keep,
							self.options,
							)

					if skip_user is not None:
						keep = not skip_user

				except Exception as exc:
					filter_members_warning(member, exc)
					keep = False

			if keep:
				ret.append((membername, member, member is INSTANCEATTR))

		return ret


def setup(app: Sphinx) -> Dict[str, Any]:
	"""
	Setup :mod:`sphinx_toolbox.more_autodoc.autoprocotol`.

	:param app:

	.. versionadded:: 0.2.0
	"""

	app.registry.domains["py"].object_types["protocol"] = ObjType(_("protocol"), "protocol", "class", "obj")
	app.add_directive_to_domain("py", "protocol", PyClasslike)
	app.add_role_to_domain("py", "protocol", PyXRefRole())

	allow_subclass_add(app, ProtocolDocumenter)

	return {
			"version": __version__,
			"parallel_read_safe": True,
			}

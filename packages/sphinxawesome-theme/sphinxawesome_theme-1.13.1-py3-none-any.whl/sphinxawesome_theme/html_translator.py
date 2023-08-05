"""Modification of the Sphinx HTML5 translator with better handling of permalinks.

Instead of "permalink to this headline",
this returns "Copy link to section: *sectionname*".
Clicking on the permalink anchor will copy the link to the clipboard.
This is implemented in JavaScript.

:copyright: Copyright 2020, Kai Welke.
:license: MIT, see LICENSE for details.
"""

from docutils import nodes
from docutils.nodes import Element
from sphinx.locale import _
from sphinx.util import logging
from sphinx.writers.html5 import HTML5Translator

logger = logging.getLogger(__name__)


class AwesomeHTMLTranslator(HTML5Translator):
    """Override a few methods to improve the usability.

    By default, Sphinx permalinks have generic titles,
    such as: "Permalink to this section".
    In the sphinx awesome theme, clicking on a permalink
    copies the link to the clipboard. Therefore,
    the link title attributes are updated to be more
    specific.
    """

    def depart_title(self, node: Element) -> None:
        """Change the permalinks for headlines.

        - for headlines: "Copy link to section: <section title>"
        - for tables: "Copy link to this table"
        - for admonitions: "Copy link to this <type>"

        Admonitions don't have an ID by default.
        The AdmonitionID post-transform adds
        IDs to admonitions.
        """
        close_tag = self.context[-1]
        if (
            self.permalink_text
            and self.builder.add_permalinks
            and node.parent.hasattr("ids")
            and node.parent["ids"]
        ):
            # add permalink anchor
            if close_tag.startswith("</h"):
                self.add_permalink_ref(
                    node.parent, _(f"Copy link to section: {node.astext()}.")
                )
            elif close_tag.startswith("</a></h"):
                self.body.append(
                    f'</a><a class="headerlink" href="#{node.parent["ids"][0]}" '
                    f'title="{_("Copy link to section: {node.astext()}.")}">'
                    f"{self.permalink_text}"
                )
            elif isinstance(node.parent, nodes.table):
                self.body.append("</span>")
                self.add_permalink_ref(node.parent, _("Copy link to this table."))
            elif isinstance(node.parent, nodes.Admonition):
                admon_type = type(node.parent).__name__
                self.add_permalink_ref(
                    node.parent, _(f"Copy link to this {admon_type}.")
                )
        elif isinstance(node.parent, nodes.table):
            self.body.append("</span>")

        self.body.append(self.context.pop())
        if self.in_document_title:  # type: ignore
            self.title = self.body[self.in_document_title : -1]  # type: ignore
            self.in_document_title = 0
            self.body_pre_docinfo.extend(self.body)
            self.html_title.extend(self.body)
            del self.body[:]

    def depart_caption(self, node: Element) -> None:
        """Change the permalinks for captions.

        - for code blocks: Copy link to this code block
        - for images: Copy link to this image
        - for table of contents: Copy link to this table of contents.
        """
        self.body.append("</span>")

        # append permalink if available
        if isinstance(node.parent, nodes.container) and node.parent.get(
            "literal_block"
        ):
            self.add_permalink_ref(node.parent, _("Copy link to this code block."))
        elif isinstance(node.parent, nodes.figure):
            self.add_permalink_ref(node.parent, _("Copy link to this image."))
        elif node.parent.get("toctree"):
            self.add_permalink_ref(
                node.parent.parent, _("Copy link to this table of contents.")
            )

        if isinstance(node.parent, nodes.container) and node.parent.get(
            "literal_block"
        ):
            self.body.append("</div>\n")
        else:
            self.body.append("</p>\n")

    def depart_desc_signature(self, node: Element) -> None:
        """Change permalinks for code definitions.

        Functions, methods, command line options, etc.
        "Copy link to this definition"
        """
        if not node.get("is_multiline"):
            self.add_permalink_ref(node, _("Copy link to this definition."))
        self.body.append("</dt>\n")

    def depart_desc_signature_line(self, node: Element) -> None:
        """Change permalinks for code definitions."""
        if node.get("add_permalink"):
            self.add_permalink_ref(node.parent, _("Copy link to this definition."))
        self.body.append("<br />")

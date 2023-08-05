"""Post-process the HTML produced by Sphinx.

- wrap literal blocks in ``div.highlights`` in order to
- inject copy code buttons
- inject HTML for collapsible navigation links
- introduce semantic markup:
  - div.section -> section
  - div.figure -> figure

:copyright: Copyright 2020, Kai Welke.
:license: MIT, see LICENSE.
"""

import os
from typing import List, Optional

from bs4 import BeautifulSoup
from sphinx.application import Sphinx
from sphinx.locale import _
from sphinx.util import logging

logger = logging.getLogger(__name__)


def _get_html_files(outdir: str) -> List[str]:
    """Get a list of HTML files."""
    html_list = []
    for root, _dirs, files in os.walk(outdir):
        html_list.extend(
            [os.path.join(root, file) for file in files if file.endswith(".html")]
        )
    return html_list


def _wrap_literal_blocks(tree: BeautifulSoup) -> None:
    """Wrap literal blocks in ``div.highlight`` elements.

    This allows us to add 'copy code' buttons to all ``div.highlight``
    elements.
    """
    literal_blocks = tree("pre", class_="literal-block")

    [
        block.wrap(tree.new_tag("div", attrs={"class": "highlight"}))
        for block in literal_blocks
    ]


def _add_copy_button(tree: BeautifulSoup) -> None:
    """Add code copy button to all ``div.highlight`` elements."""
    for code in tree("div", class_="highlight"):
        # create the button
        btn = tree.new_tag("button", attrs={"class": "copy"})
        btn["aria-label"] = _("Copy this code block")

        # create the SVG icon
        svg = tree.new_tag(
            "svg", xmlns="http://www.w3.org/2000/svg", viewBox="0 0 20 20"
        )
        svg["aria-hidden"] = "true"

        # svg path
        path = tree.new_tag(
            "path",
            d="M6 6V2c0-1.1.9-2 2-2h10a2 2 0 012 2v10a2 2 0 01-2 2h-4v4a2 2 0 "
            "01-2 2H2a2 2 0 01-2-2V8c0-1.1.9-2 2-2h4zm2 0h4a2 2 0 012 "
            "2v4h4V2H8v4zM2 8v10h10V8H2z",
        )
        svg.append(path)
        btn.append(svg)
        code.append(btn)


def _collapsible_nav(tree: BeautifulSoup) -> None:
    """Restructure the navigation links to make them collapsible.

    First, all links in the navigation sidebar are wrapped in a ``div``.
    This allows them to be 'block' and 'position relative' for the
    'expand' icon to be positioned against. (Styling occurs in the CSS)
    Note: We don't use tailwind classes here, as this is out of reach
    for the PurgeCSS plugin.

    Second, a span with the icon is inserted right before the link.
    Adding the icon as separate DOM element allows click events to be
    captured separately between the icon and the link.
    """
    for link in tree.select("#nav-toc a"):
        # First, all links should be wrapped in a div.nav-link
        link.wrap(tree.new_tag("div", attrs={"class": "nav-link"}))
        # Next, insert a span.expand before the link, if the #nav-link
        # has any sibling elements (a ``ul`` in the navigation menu)
        if link.parent.next_sibling:
            span = tree.new_tag("span", attrs={"class": "expand"})
            span.string = "\u203a"
            link.insert_before(span)


def _divs_to_section(tree: BeautifulSoup) -> None:
    """Convert ``div.section`` to semantic ``section`` elements.

    With docutils 0.17, this should not be necessary anymore.
    """
    for div in tree("div", class_="section"):
        div.name = "section"
        del div["class"]


def _add_focus_to_headings(tree: BeautifulSoup) -> None:
    """Transform headlines so that they can receive focus.

    Sphinx has a default structure of:
    <h1>Title<a class="headerlink" href="...">#</a></h1>

    What I want is:
    <h1><a href="...">Title</a><a class="headerlink" href="...">#</a></h1>

    This allows the headings to receive focus with the TAB key, as well as
    allow logic to be applied on the headerlink '#' (click to copy).
    Keyboard users can just use Ctrl+C on the focussed heading to achieve
    the same goal.
    """
    for heading in tree.select(
        "main h1, main h2, main h3, main h4, main h5, main h6, .admonition-title,"
        "figcaption,.code-block-caption, table caption"
    ):
        headerlink = heading.find("a", class_="headerlink")
        # make headerlinks (#) unfocussable
        headerlink["tabindex"] = "-1"
        caption_text = heading.find("span", class_="caption-text")
        new_tag = tree.new_tag("a", href=headerlink["href"])
        # figures, tables, code blocks
        if caption_text:
            caption_text.wrap(new_tag)
        # h1-h6, admonitions
        else:
            heading.contents[0].wrap(new_tag)


def _divs_to_figure(tree: BeautifulSoup) -> None:
    """Convert ``div.figure`` to semantic ``figure`` elements.

    With docutils 0.17, this should not be necessary anymore.
    """
    for div in tree("div", class_="figure"):
        div.name = "figure"
        div["class"].remove("figure")
        caption = div.find("p", class_="caption")
        if caption:
            caption.name = "figcaption"
            del caption["class"]


def _expand_current(tree: BeautifulSoup) -> None:
    """Add the ``.expanded`` class to li.current elements."""
    for li in tree("li", class_="current"):
        li["class"] += ["expanded"]


def _remove_pre_spans(tree: BeautifulSoup) -> None:
    """Remove unnecessarily nested ``span.pre`` elements in inline ``code``."""
    for code in tree("code"):
        for span in code("span", class_="pre"):
            span.unwrap()


def _remove_xref_spans(tree: BeautifulSoup) -> None:
    """Remove unnecessarily nested ``span.std-ref`` elements in cross-references."""
    for link in tree("a"):
        for span in link("span", class_="std-ref"):
            span.unwrap()


def _modify_html(html_filename: str) -> None:
    """Modify a single HTML document.

    The HTML document is parsed into a BeautifulSoup tree.
    Then, the following operations are performed on the tree.

    - divs to sections
    - divs to figures
    - expand current
    - collapsible navs
    - wrap literal blocks
    - add copy button
    - add focus to headings
    - remove pre spans

    After these modifications, the HTML is written into a file,
    overwriting the original file.
    """
    with open(html_filename) as html:
        tree = BeautifulSoup(html, "html.parser")

    _divs_to_section(tree)
    _divs_to_figure(tree)
    _expand_current(tree)
    _collapsible_nav(tree)
    _wrap_literal_blocks(tree)
    _add_copy_button(tree)
    _add_focus_to_headings(tree)
    _remove_pre_spans(tree)
    _remove_xref_spans(tree)

    with open(html_filename, "w") as out_file:
        out_file.write(str(tree))


def post_process_html(app: Sphinx, exc: Optional[Exception]) -> None:
    """Perform modifications on the HTML after building.

    This is an extra function, that gets a list from all HTML
    files in the output directory, then runs the ``_modify_html``
    function on each of them.
    """
    if app.builder.name not in ["html", "dirhtml"]:
        return

    if exc is None:
        html_files = _get_html_files(app.outdir)

        for doc in html_files:
            _modify_html(doc)

from __future__ import annotations

import html
import urllib.parse

import lxml.html  # nosec  # noqa DUO107
from docutils import nodes
from sphinx.application import Sphinx
from sphinx.transforms.post_transforms import SphinxPostTransform

from .utils import Obfuscator


class EmailAutoObfuscate(SphinxPostTransform):
    builders = ("html")
    default_priority = 900

    def run(self) -> None:
        """Search html for 'mailto' links and obfuscate them"""
        for node in self.document.traverse(nodes.Referential):
            print(node.asdom().toprettyxml())

"""
        tree = lxml.html.fragment_fromstring(context["body"])
        links = tree.iterlinks()
        links = filter(lambda link: link[2].startswith("mailto:"), links)

        for link in links:
            old_node = link[0]
            old_node_str = lxml.html.tostring(old_node, encoding="unicode", with_tail=False)
            tail_str = old_node.tail

            obfuscated = Obfuscator().js_obfuscated_text(old_node_str)
            new_node = lxml.html.fragment_fromstring(obfuscated)
            new_node.tail = tail_str

            old_node.getparent().replace(old_node, new_node)
        context["body"] = lxml.html.tostring(tree, encoding="unicode")


        node = nodes.raw("", obfuscated, format="html")
"""

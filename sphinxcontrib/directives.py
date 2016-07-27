# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

from docutils.parsers.rst.directives.admonitions import BaseAdmonition
from docutils import nodes
from sphinx.util.compat import make_admonition

class NamedNoteDirective(BaseAdmonition):
    node_class = nodes.admonition
    css_class = 'note'
    #required_arguments = 1
    required_arguments = 0
    optional_arguments = 1

    def run(self):
        title = u''
        if self.arguments:
            title += self.arguments[0]

        if 'class' in self.options:
            self.options['class'].append(self.css_class)
        else:
            self.options['class'] = [self.css_class]

        ret = make_admonition(
            nodes.admonition, self.name, [title], self.options,
            self.content, self.lineno, self.content_offset, self.block_text,
            self.state, self.state_machine)
        ret[0].attributes['name'] = self.name
        return ret


class ColumnDirective(NamedNoteDirective):
    css_class = 'column'


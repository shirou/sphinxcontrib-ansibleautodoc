from .ansibleautodoc import *

def setup(app):
    classes = [
        AnsibleAutoTaskDirective,
    ]
    for directive_class in classes:
        app.add_directive(directive_class.directive_name, directive_class)

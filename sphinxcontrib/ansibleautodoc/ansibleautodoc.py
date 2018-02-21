# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

from six import StringIO, iteritems
import os.path
import os
import os
import re
import codecs
import pickle
from docutils import nodes
from docutils.parsers import rst
from docutils.parsers.rst import Directive
from docutils.statemachine import ViewList

import yaml

from .i18n import texts

def is_same_mtime(path1, path2):
    try:
        mtime1 = os.stat(path1).st_mtime
        mtime2 = os.stat(path2).st_mtime
        return mtime1 == mtime2
    except:
        return False


def basename(path, ext=None):
    filename = os.path.basename(path)
    if ext:
        basename, _ext = os.path.splitext(filename)
        filename = "%s.%s" % (basename, ext)

    return filename

class Task(object):
    role_name = ""
    def __init__(self, filename, name, args, role_name=None):
        self.filename = filename
        self.name = name
        self.args = args
        if role_name:
            self.role_name = role_name

    def __str__(self):
        return "{0}, {1}, {2}".format(self.filename, self.name, self.role_name)

    def make_arg_simple(self, key, value):
        name = nodes.field_name(text=key)
        body = nodes.field_body()
        body.append(nodes.emphasis(text=value))
        field = nodes.field()
        field += [name, body]
        return field

    def make_list_representation(self, value):
        bl = nodes.bullet_list()
        if isinstance(value, list):
            for v in value:
                body = nodes.literal(text=v)
                bl.append(nodes.list_item('', body))
        elif isinstance(value, dict):
            for k,v in value.items():
                body = nodes.literal(text="%s=%s" % (k, v))
                bl.append(nodes.list_item('', body))
        return bl

    def make_arg_complex(self, key, value):
        bl = self.make_list_representation(value)
        name = nodes.field_name(text=key)
        body = nodes.field_body()
        body.append(bl)
        field = nodes.field()
        field += [name, body]
        return field

    def make_node(self, lang='en'):
        if lang not in texts.keys():
            lang = 'en'
        arg_map = texts[lang]["arg_map"]
        task_title = texts[lang]["task_title"]
        module_title = texts[lang]["module_title"]

        module_args = {}

        # Search task definition for modules and associated arguments. 
        for key, value in self.args.items():
            if key not in arg_map.keys():
                module_args[key] = value

        # Create task node (using type: admonition)
        item = nodes.admonition()
        title = nodes.title(text=self.name)
        item.append(title)

        # Add modules and arguments to task node
        for module, args in module_args.items():
            field_list = nodes.field_list() # wrap module header in field_list
            field_list.append(self.make_arg_simple(module_title, module))
            item.append(field_list)
            if isinstance(args, str):
                item.append(nodes.literal_block(text=args))
            else:
                item.append(self.make_list_representation(args))

        # Handle non-module task parameters.
        field_list = nodes.field_list()
        for arg, txt in arg_map.items():
            if not txt:  # skip name etc...
                continue
            if arg not in self.args:
                continue
            value = self.args[arg]  # value of that task arg
            if isinstance(value, list) or isinstance(value, dict):
                field_list.append(self.make_arg_complex(txt, value))
            else:
                field_list.append(self.make_arg_simple(txt, value))

        item.append(field_list)

        return item

class AutodocCache(object):
    _cache = {}

    def parse_include(self, filename, include, role_name=None):
        d = os.path.dirname(filename)
        if role_name:
            i = os.path.join(d, "roles", role_name, 'tasks', include)
        else:
            i =  os.path.join(d, include)

        with open(i, "r") as f:
            for task in yaml.load(f):
                self.parse_task(filename, task, role_name)

    def parse_role(self, filename, role):
        if 'role' not in role:
            return
        d = os.path.dirname(filename)
        r = os.path.join(d, "roles", role['role'], 'tasks', 'main.yml')

        with open(r, "r") as f:
            for task in yaml.load(f):
                self.parse_task(filename, task, role['role'])

    def parse_task(self, filename, task, role_name=None):
        if 'include' in task:
            self.parse_include(filename, task['include'], role_name)
            return
        if 'name' not in task:
            return
        t = Task(filename, task['name'], task, role_name)
        self._cache[filename].append(t)

    def parse_play(self, filename, play):
        if 'tasks' in play:
            for task in play['tasks']:
                self.parse_task(filename, task)
        if 'roles' in play:
            for role in play['roles']:
                self.parse_role(filename, role)


    def walk(self, filename, role=None):
        if filename not in self._cache:
            # use list because there maight be same task name
            self._cache[filename] = []

        with open(filename, "r") as f:
            for play in yaml.load(f):
                self.parse_play(filename, play)

    def get(self, filename, taskname, role_name=None):
        if filename not in self._cache:
            return None
        for t in self._cache[filename]:
            if t.name == taskname:
                if role_name and t.role_name != role_name:
                    continue
                return t
        return None

    def parse(self, basedir, filename):
        cachename = os.path.join(basedir, basename(filename, 'parse'))
        if is_same_mtime(filename, cachename):
            self._cache = pickle.load(open(cachename, 'rb'))
        else:
            try:
                self.walk(filename)
                with open(cachename, 'wb') as f:
                    pickle.dump(self._cache, f)
                mtime = os.stat(filename).st_mtime
                os.utime(cachename, (mtime, mtime))
            except:
                raise

class AnsibleAutoTaskDirective(Directive):
    directive_name = "ansibleautotask"

    _cache = AutodocCache()

    has_content = True
    option_spec = {
        'playbook': rst.directives.unchanged_required,
        'role': rst.directives.unchanged,
    }

    def run(self):
        self.assert_has_content()
        env = self.state.document.settings.env

        if 'playbook' not in self.options:
            msg = 'playbook option is required '
            self.state_machine.reporter.warning(msg, line=self.lineno)
            return []

        basedir = env.doctreedir
        filename = self.options['playbook']
        self._cache.parse(basedir, filename)

        role = None
        if 'role' in self.options:
            role = self.options['role']

        taskname = "".join(self.content)
        task = self._cache.get(filename, taskname, role)
        if not task:
            msg = 'filename: %s, taskname: %s is not found' % (filename, taskname)
            self.state_machine.reporter.warning(msg, line=self.lineno)
            return []

        lang = env.config.language
        if not lang:
            lang = 'en'

        return [task.make_node(lang)]


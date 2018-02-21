# -*- coding: utf-8 -*-

# simple i18n

texts = {
    "en": {
        "task_title": 'task name',
        "module_title": 'module',
        "arg_map": {
            'when': 'condition',
            'become': 'sudo',
            'delegate_to': 'host',
            'register': 'register',
            'run_once': 'run once',
            'with_items': 'with items',
            'environment': 'envvars',
            'tags': 'tags',
            'name': None, # used for field skip
        },
    },
    "ja": {
        "task_title": u'タスク名',
        "module_title": u'モジュール',
        "arg_map": {
            'when': u'条件',
            'become': 'sudo',
            'delegate_to': u'実行ホスト',
            'run_once': u'一度だけ実行',
            'register': u'変数代入',
            'with_items': u'繰り返し',
            'environment': u'環境変数',
            'tags': u'タグ',
            'name': None, # used for field skip
        },
    },
}

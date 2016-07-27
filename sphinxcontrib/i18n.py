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
            'run_once': 'run once',
            'tags': 'tags',
            'name': None,
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
            'tags': u'タグ',
            'name': None,  # used for 
        },
    },
}

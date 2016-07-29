Welcome to ansibleautodoc test's documentation!
===============================================

I want to write this very important ansible task.

.. ansibleautotask:: first task
   :playbook: ../ansible/web.yml

If that task has some arguments like `when`, these are also listed as follows.

.. ansibleautotask:: condition
   :playbook: ../ansible/web.yml


If arguments are list, like this.

.. ansibleautotask:: multiple args
   :playbook: ../ansible/web.yml


You can see the avobe label. so we now use :ref:`condition_label` to the task.


.. ansibleautotask:: hoghgoe
   :playbook: ../ansible/web.yml

Welcome to ansibleautodoc test's documentation!
===============================================

Basics
------
Documenting tasks with ``ansibleautodoc`` is easy. Simply use the ``ansibleautotask`` directive. Here's what a simple task (no arguments) looks like:

.. ansibleautotask:: first task
   :playbook: ../ansible/web.yml

If that task has some arguments like `when`, these are also listed as follows:

.. ansibleautotask:: condition
   :playbook: ../ansible/web.yml

Complex Arguments
-------------------
If arguments are list, like this.

.. ansibleautotask:: multiple args
   :playbook: ../ansible/web.yml

Or like this:

.. ansibleautotask:: looping with a condition.
   :playbook: ../ansible/web.yml

If one or more arguments are a dictionary, then they are also rendered:

.. ansibleautotask:: looping task with lots of parameters
   :playbook: ../ansible/web.yml

Roles
-----
.. tip::
   This assumes that your roles follow the conventional Ansible role structure. Include paths for role YML files are based off the form ``<your_project>/roles/<role_name>/tasks/*.yml``. At this time, files outside of the ``tasks`` directory cannot be included.

Tasks available through an included role are also available for a specified playbook. For example, the ``second in role`` task is part of the ``three`` role, which is included in ``web.yml``:

.. ansibleautotask:: second in role
   :playbook: ../ansible/web.yml

Going even deeper, you can even access included tasks within an included role. The task ``role included`` is included by the ``three`` role:

.. ansibleautotask:: role included
   :playbook: ../ansible/web.yml
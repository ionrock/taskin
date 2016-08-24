======
taskin
======

.. image:: https://badge.fury.io/py/taskin.png
    :target: http://badge.fury.io/py/taskin

.. image:: https://travis-ci.org/ionrock/taskin.png?branch=master
        :target: https://travis-ci.org/ionrock/taskin


Taskin provides simple task management. Tasks are simple callables
that will be executed using a pool of resources. The pool can be a
process or thread pool in order to achieve the required
concurrency. The suite of tasks is called a `flow`. A flow is defined
by defining a list of functions to run.

Here is an example:

.. include:: ./example/flow.py



* Free software: BSD license
* Documentation: https://taskin.readthedocs.org.

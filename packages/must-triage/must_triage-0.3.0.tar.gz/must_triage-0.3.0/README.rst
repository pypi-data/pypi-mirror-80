
must-triage
===========

When things go wrong with `OpenShift <https://www.openshift.com/>`_ or `OpenShift Container Storage <https://www.openshift.com/products/container-storage/>`_\ , we sometimes use `\ ``must-gather`` <https://github.com/openshift/must-gather>`_ or `\ ``ocs-must-gather`` <https://github.com/openshift/ocs-operator/tree/master/must-gather>`_ to collect logfiles and other documents to diagnose issues. While those tools are useful in that they can show us a lot about the state of the system(s), they don't offer anything to help process that information.

``must-triage`` is a very small utility to aid in identifying problems recorded in ``must-gather`` output.

Features
--------

Currently, ``must-triage`` knows about the following potential issues:

OpenShift (OCP)
^^^^^^^^^^^^^^^


* Unparseable YAML files
* Pods not in ready state

OpenShift Container Storage (OCS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


* Empty JSON files
* Unparseable JSON files
* Ceph health not ``HEALTH_OK``

Teaching it to identify new issues is not difficult; PRs warmly welcomed!

Installation
------------

.. code-block::

   pip install must-triage

Usage
-----

.. code-block::

   must-triage /path/to/must-gather/output

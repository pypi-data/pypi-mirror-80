CHANGELOG
=========

2020-09-24 | v0.0.6
-------------------

* Added ``--clear-env`` to ``lxc-attach`` commands used in ``build`` so that there are no env vars issues.


2020-09-11 | v0.0.5
-------------------

* All commands now handle required input paramters correctly.
* Added ``prepare`` command which runs ``prepare.sh`` in given build directory to get the build directory ready for builds. This is for example usefull if you need to pull in secrets from vaults.
* Added ``-e``, ``--environment`` input parameter to ``build`` and ``prepare`` commands which is used as first argument for ``build.sh`` and ``prepare.sh`` scripts.


2020-09-11 | v0.0.4
-------------------

* ``build`` process can now work with build directory that does not match name of the container ie. this allows multi-step builds.


2020-09-02 | v0.0.3
-------------------

* ``build`` process now expects ``build.sh`` to be present in the build directory


2020-09-02 | v0.0.2
-------------------

* New commands ``ls`` and ``pack``
* ``build`` command now only builds
* Updated documentation


2020-08-28 | v0.0.1
-------------------

* Initial version

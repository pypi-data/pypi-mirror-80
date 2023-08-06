README
======

`Balič` (read `balitch`) is a command-line toolset for working with LXC containers.

| |license| |downloads|
| |status| |format| |wheel|
| |version| |pyversions| |implementation|
| |coverage|

.. |version| image:: https://img.shields.io/pypi/v/balic
   :target: https://pypi.org/project/balic/
   :alt: PyPI - Version

.. |pyversions| image:: https://img.shields.io/pypi/pyversions/balic
   :target: https://pypi.org/project/balic/
   :alt: PyPI - Python Versions

.. |implementation| image:: https://img.shields.io/pypi/implementation/balic
   :target: https://pypi.org/project/balic/
   :alt: PyPI - Implementation

.. |downloads| image:: https://img.shields.io/pypi/dm/balic
   :target: https://pypi.org/project/balic/
   :alt: PyPI - Downloads

.. |license| image:: https://img.shields.io/pypi/l/balic
   :target: https://pypi.org/project/balic/
   :alt: PyPI - License

.. |format| image:: https://img.shields.io/pypi/format/balic
   :target: https://pypi.org/project/balic/
   :alt: PyPI - Format

.. |status| image:: https://img.shields.io/pypi/status/balic
   :target: https://pypi.org/project/balic/
   :alt: PyPI - Status

.. |wheel| image:: https://img.shields.io/pypi/wheel/balic
   :target: https://pypi.org/project/balic/
   :alt: PyPI - Wheel

.. |coverage| image:: https://codecov.io/gl/markuz/balic/branch/master/graph/badge.svg
   :target: https://codecov.io/gl/markuz/balic
   :alt: coverage.io report

Installation
------------

Install ``balic`` via ``pip``::

    pip install balic


``Balic`` requires the following packages installed::

    appdirs
    cliff


Usage
-----

Create a new container::

    # create a new lxc container called test
    balic create -n test

Build setup::

    # create test build directory
    mkdir test

    # create build.sh that echos hello world inside the container
    echo 'echo "hello world"' > test/build.sh

    # copy test directory into the container and run build.sh
    balic build -n test -d test

In case you need to prepare anything in the build directory::

    # create prepare.sh which will be executed locally to prepare build dir
    echo 'echo "prepare something inside build dir: `dirname "$0"`"' > test/prepare.sh

    # run prepare.sh in given build dir
    balic prepare -n test -d test

Multi-step builds can be done as well::

    # create test_step2 build directory
    mkdir test_step2
    
    # create build.sh that echos "another step" inside the container
    echo 'echo "another step"' > test_step2/build.sh

    # copy test directory into container and run build.sh
    balic build -n test -d test_step2

Pack the built container::

    # pack test lxc container into rootfs.tar.gz
    balic pack -n test -o rootfs.tar.gz

Destroy the container when no longer needed::

    # destroy test lxc container
    balic destroy -n test


Full workflow::

    balic create -n test                 # creates lxc container names test
    balic prepare -n test -d build_dir   # run prepare.sh inside the build_dir
    balic build -n test -d build_dir     # builds test lxc container using content of build_dir
    balic build -n test -d build_dir2    # builds test lxc container using content of build_dir2
    balic build -n test -d build_dir3    # builds test lxc container using content of build_dir3
    ...
    balic pack -n test -o rootfs.tar.gz  # packs test lxc container into rootfs.tar.gz
    balic destroy -n test                # destroy test lxc container


Use ``environment`` input parameter for ``build`` and ``prepare`` commands::

    # to run `build.sh environment` or `prepare.sh environment` use -e input parameter
    balic prepare -n test -d test -e production
    balic build -n test -d test -e production

Ie. whatever you specify as environment ends up as ``$1`` in ``build.sh`` / ``prepare.sh``.


Documentation
-------------

Source of the documentaton is available in the `Balic` repository
https://gitlab.com/markuz/balic/tree/master/docs/source


Development
-----------

Pull requests welcomed.

``Balic`` git repository is available at https://gitlab.com/markuz/balic

For more information, see https://gitlab.com/markuz/balic/-/blob/master/docs/source/development.rst


License
-------

`BSD 3-clause Clear License <https://gitlab.com/markuz/balic/blob/master/LICENSE>`_

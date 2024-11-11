Installation
============

.. warning:: Directly calling `pip install radiantkit` or `pipx
   install radiantkit` will install an outdated version -- Always
   download the latest version from `github <https://www.github.com/BiCroLab/radiantkit/>`_.


Requirements
------------

``radiantkit`` has been tested with Python 3.12. The current
dependencies are listed in the `pyproject.toml` file and should in
most cases be handled automatically by pip/pipx/builddtools.

Install
-------

The main options are to install using pip or pipx, depending on your preferences.

Install with ``pipx`` (recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

   git clone https://github.com/BiCroLab/radiantkit.git
   cd radiantkit
   pipx install .


Install with ``pip``
^^^^^^^^^^^^^^^^^^^^

This is not recommended unless you know what you are doing. In most
cases you would like to set up an virtual enviroment first (something
that pipx handles automatically).

.. code:: bash

   git clone https://github.com/BiCroLab/radiantkit.git
   cd radiantkit
   pip install --user .


Check your installation
-----------------------

To check your installation, simply run:

.. code:: bash

   radiantkit --version

If you see the version of ``radiantkit`` that you installed, everything
went well! If you see an error or ``command not found``, try again or
`get in touch <https://github.com/BiCroLab/radiantkit/issues>`__!

When Python < 3.12
------------------

Python 3.12 or later is a hard requirement, however, in most cases you
can install that. For example: Ubuntu 22.04.5 LTS ships with Python
3.9 but Python 3.12 can be installed with commands like:

.. code:: bash

   sudo apt-get install python3.12-*

To make sure that the correct version of Python is used, the simplest
option is to create a virtual environment. It should be possible to
install and run radiantkit like this:

.. code:: bash

   # Assuming that you are in the root folder of the repository
   python3.12 -m venv .venv
   source .venv/bin/activate
   pip install pipx
   python -m pipx install .
   radiantkit -h

   # Or alternatively with pip:
   pip install .
   python -m radiantkit -h


Docker
------

If you prefer to use Docker, you can use the supplied `Dockerfile` to
assemble an image. From the root directory of the repository, run:

.. code:: shell

          $ docker build -t radiantkit -f Dockerfile .
          # And possibly
          $ docker tag radiantkit bicrolab/radiantkit:0.1.0


If everything went fine, there should now be an image:

.. code:: shell

   # Check if there is an image
   $ docker image ls
   REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
   radiantkit   latest    9a486800b424   35 seconds ago   858MB

   # It is not running yet
   $ docker ps
   CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

To start it and attach to it directly, you could use:

.. code:: shell

   $ docker run -it --rm -v '/my/local/data/':'/data/' radiantkit
   # See that it looks ok:
   $ root@7330fbf2843c:/# radiantkit --version
   $ ./root/.local/bin/radiantkit 0.1.0

And you are ready to radiantkit on your local data which you will find
under `/data` in the container.

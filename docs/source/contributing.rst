Contributing
============

Before you dive into contributing to stockAPI. You will need to setup your
environment so you are able to test your code changes before submitting a code
review.

Dev env
-------

Basically you need some extra packages installed in your machine and a python virtual 
environment. Currently all developers are running Fedora >= 26 so not sure how compatible 
this project will be with others OS and versions.

* clone project
* initialize python virtual env
* create your branch or fork the project
* create a PR and submit your code for code review

install required packages (vim is optional but good to have):

.. code:: bash

	sudo yum -y install git python-setuptools wget vim

install pip:

.. code:: bash

	# option 1
	sudo easy_install pip

	# option 2
	sudo wget https://bootstrap.pypa.io/get-pip.py
	sudo python get-pip.py
	
clone project:

.. code:: bash
	
	git clone git@github.com:eduardocerqueira/stockAPI.git


install pip modules (optional):

.. code:: bash
	
	sudo pip install -r stockAPI/requirements.txt

Initialize your project:

.. code:: bash

	cd stockAPI
	make init

.. note ::

	you might need to activate your virtualenv manually after make init, running:
	source venv/bin/activate
	
and get familiar with the make tasks.

#!/bin/bash

#
# bash script to handle python virtual environment
#
# Copyright (C) 2018
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# imports
source scripts/functions.sh

# global variables
PYTHON_VER=/usr/bin/python3.6
VENV_PATH="$(pwd)/venv"
PIP_ENV=$(pip -V)
REQ_MODULES="requirements.txt"

# create virtual environment
log_section "Creating python virtual env"

if [[ ! $PIP_ENV =~ "$VENV_PATH" ]]; then
	virtualenv -p $PYTHON_VER venv
	PYTHONPATH=$VENV_PATH
	export PYTHONPATH="$VENV_PATH"
	log "TRACE" "created at $VENV_PATH"
	log_section "Activating your virtual environment"
	source $VENV_PATH/bin/activate
	if [ $? ]; then
		log "TRACE" "activated"
		# virtualenv info
		log "INFO" "PATH: $VENV_PATH/bin/activate"
		log "INFO" "$(pip -V)"
	else
		log "ERROR" "virtualenv not activated, exit 1"
		exit 1
	fi
fi

# install python modules from requirements.txt
log_section "Installing/Updating modules in $VENV_PATH"
if [ ! -e requirements.txt ] ; then 
	log "ERROR" "requirements.txt not found, exit 1"
	exit 1
fi
$VENV_PATH/bin/pip install -U -r $REQ_MODULES
if [ $? ]; then
	log "TRACE" "all modules from $REQ_MODULES have been installed"
else
	log "ERROR" "could not install modules from $REQ_MODULES, exit 1"
	exit 1
fi
$VENV_PATH/bin/pip install -e .

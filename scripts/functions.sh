#!/bin/bash

#
# functions used by stockAPI.
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

# global variables
LINE="-------------------------------------------------------------------------"

# print log message at stdout
# parameters:
# 	$1: msg type, can be INFO, WARN, ERROR
#	$2: msg, the actual message to be displayed  
function log(){
	if [ "$1" == "INFO" ]; then
		echo -e "\e[0m$2\e[0m"
	fi
	if [ "$1" == "TRACE" ]; then
		echo -e "\e[32m$2\e[0m"
	fi
	if [ "$1" == "WARN" ]; then
		echo -e "\e[33m$2\e[0m"
	fi
	if [ "$1" == "ERROR" ]; then
		echo -e "\e[31m$2\e[0m"
	fi
	}

# print section message at stdout in a block format with line divisors
# parameters:
# 	$1: msg, the section name or any other info to be displayed
function log_section(){
	echo
	echo "$LINE"
	echo -e "\e[32m$1\e[0m"
	echo "$LINE"
	}

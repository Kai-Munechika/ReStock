# Variables -------------------------------------------------------------------

NO_COLOR    = \x1b[0m
OK_COLOR    = \x1b[32;01m
WARN_COLOR  = \x1b[50;01m
ERROR_COLOR = \x1b[31;01m
SHELL = bash
PYTHONPATH=$(PWD)

# Commands --------------------------------------------------------------------

help:
	@echo -e "Please use $(WARN_COLOR) \`make <target>\'$(NO_COLOR) where $(WARN_COLOR)<target>$(NO_COLOR) is one of"
	@echo -e "  $(OK_COLOR)--- setup ---$(NO_COLOR)"	
	@echo -e "  $(WARN_COLOR)init$(NO_COLOR)              to initialize project, install pip packages and create virtualenv"
	@echo -e "  $(OK_COLOR)--- doc ---$(NO_COLOR)"	
	@echo -e "  $(WARN_COLOR)docs$(NO_COLOR)              to make documentation in the default format"
	@echo -e "  $(WARN_COLOR)clean-docs$(NO_COLOR)        to remove docs and doc build artifacts"
	@echo -e "  $(OK_COLOR)--- code ---$(NO_COLOR)"	
	@echo -e "  $(WARN_COLOR)codecheck$(NO_COLOR)         to run code check on the entire project"
	@echo -e "  $(WARN_COLOR)clean-cache$(NO_COLOR)       to clean pytest cache files"
	@echo -e "  $(WARN_COLOR)clean-all$(NO_COLOR)         to clean cache, pyc, logs and docs"
	@echo -e "  $(WARN_COLOR)clean-pyc$(NO_COLOR)         to delete all temporary artifacts"
	@echo -e "  $(OK_COLOR)--- run tests ---$(NO_COLOR)"	
	@echo -e "  $(WARN_COLOR)tests$(NO_COLOR)             run all tests"
	@echo -e "  $(OK_COLOR)--- Database ---$(NO_COLOR)"
	@echo -e "  $(WARN_COLOR)db-import$(NO_COLOR)         database import"
	@echo -e "  $(WARN_COLOR)db-drop$(NO_COLOR)           database delete"
	@echo -e "  $(OK_COLOR)--- Application ---$(NO_COLOR)"
	@echo -e "  $(WARN_COLOR)run-app$(NO_COLOR)           run Flask application"
	@echo -e "$(NO_COLOR)"

# Targets ---------------------------------------------------------------------

.PHONY: help docs codecheck clean-docs clean-cache clean-all tests

init: clean_venv
	scripts/virtualenv.sh

clean_venv:
	rm -rf venv

docs:
	@cd docs; sphinx-apidoc -f -o source/ ../../stockAPI/src/
	@cd docs; $(MAKE) html

clean-docs:
	$(info "Cleaning docs...")
	@cd docs; $(MAKE) clean

codecheck: 
	@echo -e "$(WARN_COLOR)----Starting PEP8 code analysis----$(NO_COLOR)"
	find src/ -name "*.py" | xargs pep8 \
	--verbose --statistics --count --show-pep8 --exclude=.eggs
	@echo -e "$(WARN_COLOR)----Starting Pylint code analysis----$(NO_COLOR)"
	find src/ -name "*.py" | xargs pylint --rcfile=pylintrc
	@echo

clean-cache:
	$(info "Cleaning the .cache directory...")
	rm -rf .cache

clean-all: clean-docs clean-cache clean-pyc clean_venv

clean-pyc: ## remove Python file artifacts
	$(info "Removing unused Python compiled files, caches and ~ backups...")
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

tests:
	@echo -e "$(WARN_COLOR)----Running tests----$(NO_COLOR)"
	@pytest -v tests

db-import:
	@echo -e "$(WARN_COLOR)----Running DB data importer----$(NO_COLOR)"
	@export PYTHONPATH=$PWD
	@python restock/db/update_db_using_iex_API.py

db-drop:
	@echo -e "$(WARN_COLOR)----Drop DB----$(NO_COLOR)"
	@export PYTHONPATH
	@echo "set PYTHONPATH=$(PYTHONPATH)"
	@python restock/db/delete_db.py

run-app:
	@echo -e "$(WARN_COLOR)----Running Flask application----$(NO_COLOR)"
	@export PYTHONPATH
	@echo "set PYTHONPATH=$(PYTHONPATH)"
	@python restock/app.py

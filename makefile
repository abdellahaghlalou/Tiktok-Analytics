CURRENT_DIRECTORY := $(shell pwd)

help:
	@echo "Docker Compose Help"
	@echo "-----------------------"
	@echo ""
	@echo "Run tests to ensure current state is good:"
	@echo "    make test"
	@echo ""
	@echo "If tests pass, add fixture data and start up the api:"
	@echo "    make begin"
	@echo ""
	@echo "Really, really start over:"
	@echo "    make clean"
	@echo ""
	@echo "See contents of Makefile for more targets."

begin: migrate fixtures start

start:
	@docker-compose --file docker-compose.yml up -d --build

stop:
	@docker-compose stop

status:
	@docker-compose ps

restart: stop start

clean: stop
	@docker-compose rm --force
	@find . -name \*.pyc -delete

build:
	@docker-compose buildf ps

test:
	@docker-compose --file docker-compose.yml run --rm ps pytest ./test

testwarn:
	@docker-compose --file docker-compose.yml run --rm ps pytest  ./test -vvv
#? Activated when migration needed
#migrate:
#	@docker-compose run --rm api python ./manage.py migrate
#? Activated when fixtures needed
#fixtures:
#	@docker-compose run --rm api python ./manage.py runscript load_all_fixtures

cli:
	@docker-compose run --rm ps bash

tail:
	@docker-compose logs -f

#.PHONY: start stop status restart clean build test testwarn migrate fixtures cli tail
.PHONY: start stop status restart clean build test testwarn cli tail
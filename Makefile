#!/usr/bin/make
.PHONY: buildout cleanall test instance

bootstrap.py:
	wget http://downloads.buildout.org/2/bootstrap.py

bin/python:
	if [ -f /usr/bin/virtualenv-2.7 ] ; then virtualenv-2.7 .;else virtualenv -p python2.7 .;fi
	touch $@

bin/buildout: bootstrap.py buildout.cfg bin/python
	./bin/python bootstrap.py
	touch $@

buildout: bin/buildout
	./bin/buildout -t 7

test: buildout
	./bin/test

instance: buildout
	./bin/instance fg


cleanall:
	rm -rf bin develop-eggs downloads include lib parts .installed.cfg .mr.developer.cfg bootstrap.py parts/omelette

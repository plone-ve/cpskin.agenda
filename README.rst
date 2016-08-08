.. contents::

Introduction
============

Agenda developments for cpskin


Tests
=====

This package is tested using Travis CI. The current status is :

.. image:: https://travis-ci.org/IMIO/cpskin.agenda.png
    :target: http://travis-ci.org/IMIO/cpskin.agenda

.. image:: https://coveralls.io/repos/github/IMIO/cpskin.agenda/badge.svg?branch=master 
    :target: https://coveralls.io/github/IMIO/cpskin.agenda?branch=master 

Robot tests
===========


Run all tests
-------------

bin/test


Run specific tests
------------------

You can launch the robot server with the command:

    bin/robot-server cpskin.agenda.testing.CPSKIN_AGENDA_ROBOT_TESTING

And launch the tests:

    bin/robot cpskin/agenda/tests/robot/<yourfile>.robot

You can sandbox on http://localhost:55001/plone/

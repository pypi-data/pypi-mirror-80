#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

'''
https://logbook.readthedocs.io/en/stable/api/base.html

logbook.CRITICAL
logbook.ERROR
logbook.WARNING
logbook.NOTICE
logbook.INFO
logbook.DEBUG
logbook.TRACE
logbook.NOTSET
'''

import logbook

logger_group = logbook.LoggerGroup()
logger_group.level = logbook.INFO

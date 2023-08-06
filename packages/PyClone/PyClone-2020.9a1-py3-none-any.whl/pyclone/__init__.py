#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

# Logging
from logbook import Logger
from pyclone.log import logger_group
logger = Logger( __loader__.name )
logger_group.add_logger( logger )

from .pyclone import PyClone

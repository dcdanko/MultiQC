#!/usr/bin/env python

""" BioBitBot functions to plot a report beeswarm group """

import json
import logging
import os
import random

from biobitbot.utils import report, config
logger = logging.getLogger(__name__)

letters = 'abcdefghijklmnopqrstuvwxyz'


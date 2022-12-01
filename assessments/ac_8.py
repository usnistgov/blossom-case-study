#!/usr/bin/env python3
# Consumed by the oscal-workflow harness

import os
import textwrap
from urllib import request

from bs4 import BeautifulSoup

# The system use notification text
expected_use_notification = os.getenv('SSP_PARAM_AC_8_PRM_1')
if expected_use_notification is None:
    raise Exception('ac-8_prm_1 must be defined in the SSP')

# running via docker-compose.yaml
response = request.urlopen('http://127.0.0.1:10000')

soup = BeautifulSoup(response, 'html.parser')

# Drill into the element that the system use notification text lives
raw_use_notification = soup.body.div.p.text
clean_use_notification = textwrap.dedent(raw_use_notification).strip()

assert clean_use_notification == expected_use_notification

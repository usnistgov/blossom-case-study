#!/usr/bin/env python3
# Consumed by the oscal-workflow harness

import textwrap

import urllib3
from bs4 import BeautifulSoup

# The system use notification we expect
# TODO: source this from a passed in param/env var
expected_use_notification = '''You are accessing a U.S. Government information system, which includes: 1) this computer, 2) this computer network, 
3) all Government-furnished computers connected to this network, and 4) all Government-furnished devices and storage 
media attached to this network or to a computer on this network. You understand and consent to the following: you 
may access this information system for authorized use only; unauthorized use of the system is prohibited and subject 
to criminal and civil penalties; you have no reasonable expectation of privacy regarding any communication or data 
transiting or stored on this information system at any time and for any lawful Government purpose, the Government may 
monitor, intercept, audit, and search and seize any communication or data transiting or stored on this information system; 
and any communications or data transiting or stored on this information system may be disclosed or used for any lawful 
Government purpose. This information system may contain Controlled Unclassified Information (CUI) that is subject to 
safeguarding or dissemination controls in accordance with law, regulation, or Government-wide policy. Accessing and 
using this system indicates your understanding of this warning.'''

http = urllib3.PoolManager()
# running via docker-compose.yaml
response = http.request('GET', 'http://127.0.0.1:10000')

soup = BeautifulSoup(response.text, 'html.parser')

# Drill into the element that the system use notification text lives
raw_use_notification = soup.body.div.p.text
clean_use_notification = textwrap.dedent(raw_use_notification).strip()

assert clean_use_notification == expected_use_notification

#!/usr/bin/python3
#
# Retrieve port statistics from a TP-Link TL-SG1016DE switch
#
import requests
import sys
import re

from requests.exceptions import HTTPError

# Change to your needs
ipaddress = '192.168.178.X'
# Default values for the switch
username = 'admin'
password = 'admin'

class tplink_stats:
    """Class for retrieving port statistics from a TP-Link switch"""

    # descriptive port labels; can be modified to your installation
    port_label = [
        'Port 0',
        'Port 1',
        'Port 2',
        'Port 3',
        'Port 4',
        'Port 5',
        'Port 6',
        'Port 7',
        'Port 8',
        'Port 9',
        'Port 10',
        'Port 11',
        'Port 12',
        'Port 13',
        'Port 14',
        'Port 15'
    ]
    # Remaining parts do not need to be modified
    port_state = [
        'disabled',
        'enabled'
    ]
    link_speed = [
        '0',
        '0',
        '10',
        '10',
        '100',
        '100',
        '1000'
    ]
    duplex_info = [
        'none',
        'auto',
        'half',
        'full',
        'half',
        'full',
        'full'
    ]

    def __init__(self, ipaddress, username, password, debug):
        self.ipaddress = ipaddress
        self.referer = 'http://' + self.ipaddress + '/Logout.htm'
        self.username = username
        self.password = password
        self.debug = debug

    def login(self):
        url = 'http://' + self.ipaddress + '/logon.cgi'

        try:
            if self.debug:
                print(f'POST {url}')
            response = requests.post(url, headers={'Referer' : self.referer}, data={'username': self.username,'password': self.password, 'logon': 'Login'})

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            # For some weird reason the switch responds with 401 if authorisation suceeded
            if (http_err.response.status_code != 401):
                if (self.debug):
                    print(f'POST {url} failed with status {http_err.response.status_code}')
                return
        except Exception as err:
            if (self.debug):
                print(f'POST {url} exception {err}')
            return

        self.referer = url
        return url

    def port_stats(self):
        url = 'http://' + self.ipaddress + '/PortStatisticsRpm.htm'
        try:
            if (self.debug):
                print(f'GET {url}')
            response = requests.get(url, headers={'Referer' : self.referer})

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            if (self.debug):
                print(f'GET {url} failed with status {http_err.response.status_code}')
            return
        except Exception as err:
            if (self.debug):
                print(f'GET {url} exception {err}')
            return

        if (self.debug):
            print(f'Body text: {response.text}')
        self.referer = url
        body = response.text.replace('\n','')
        body.replace('\r','')

        m = re.search(r'var all_info = {(.*?)};', body)
        if (m):
            s = re.search(r'state:\[(.*?)\]', m.group(1))
            state = s.group(1).split(',')
            l = re.search(r'link_status:\[(.*?)\]', m.group(1))
            link = l.group(1).split(',')
            p = re.search(r'pkts:\[(.*?)\]', m.group(1))
            pkts = p.group(1).split(',')
            for i in range(0, 16):
                print(f'tplink_port_state,ipaddress="{self.ipaddress}",port={i} label="{self.port_label[i]}",state="{self.port_state[int(state[i])]}",link={self.link_speed[int(link[i])]},duplex="{self.duplex_info[int(link[i])]}",txgood={pkts[i * 4]},txbad={pkts[i * 4 + 1]},rxgood={pkts[i * 4 + 2]},rxbad={pkts[i * 4 + 3]}')
        return url

    def logout(self):
        url = 'http://' + self.ipaddress + '/Logout.htm'
        try:
            if (self.debug):
                print(f'GET {url}')
            response = requests.get(url, headers={'Referer' : self.referer})

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            # 401 Unauthorized is the 'normal' response code here
            if (http_err.response.status_code != 401):
                if (self.debug):
                    print(f'GET {url} failed with status {http_err.response.status_code}')
                return
        except Exception as err:
            if (self.debug):
                print(f'GET {url} exception {err}')
            return

        return url

t = tplink_stats(ipaddress, username, password, 0)
login_url = t.login()
if login_url:
    t.port_stats()
    t.logout()

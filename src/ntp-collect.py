#!/usr/bin/env python

import json
import sys
import subprocess
import socket
import shlex

NTPQ_BIN='/usr/bin/ntpq'

METRICS=[
        'stratum',
        'offset',
        'rootdelay',
        'clk_jitter',
        'sys_jitter',
        'clk_wander',
]

class NTPError(Exception): pass

class NTPCollector(object):
    def __init__(self):
        self.hostname = socket.getfqdn()
        self.metrics = {}


    def collect(self):
        ntq_command = shlex.split("{} -c 'rv 0 {}'".format(NTPQ_BIN, ','.join(METRICS)))
        data = subprocess.check_output(ntq_command)
        data = str(data).split(',')
        data = " ".join([ c.strip() for c in data]).replace("\\n", '')
        data = data.replace("'","").replace("b","")
        data = data.split(' ')

        for var in data:
            k, v = var.split("=")
            self.metrics["{}.{}".format(self.hostname, k)] = v

        print(json.dumps(self.metrics, indent=4))


def main():
    collector = NTPCollector()
    collector.collect()

    return 0

if __name__ == '__main__':
    sys.exit(main())

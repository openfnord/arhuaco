import sys
import time
import subprocess
import logging
import os.path
import time

from arhuaco.sensors.source.source import Source

class NetworkMetrics(Source):

    def __init__(self, dataPath):
        # Initialize entities
        super(NetworkMetrics, self).__init__()
        self.dataPath        = dataPath

    def get_data_iterator(self):
        # Collect network data by the bro network analyzer
        logging.info("Start network collection.")
        command_bro = ("/opt/bro/bin/broctl start")
        command_log = (" tail -f /opt/bro/logs/current/dns.log ")
        logging.info("Starting BRO %s" % command_bro)
        proc_bro = subprocess.Popen(["/opt/bro/bin/broctl","start"],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        while not os.path.exists("/opt/bro/logs/current/dns.log"):
            time.sleep(1)
        logging.info("Starting the log collection %s" % command_log)
        proc_log = subprocess.Popen(command_log,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    shell=True)
        # Extract data from the BRO logs
        while proc_log.poll() is None:
            line = proc_log.stdout.readline()
            fields = line.decode("utf-8").strip().split()
            if len(fields) > 14:
                line = fields[9]+" "+fields[10]+" "+fields[11]\
                       +" "+fields[12]+" "+fields[13]
                # logging.info(line)
                yield line
        logging.info(proc_log.poll())
        logging.info('Finalyzing BRO collection.')
        proc_bro.terminate()
        logging.info('Finalyzing log analysis.')
        proc_log.terminate()

    def get_data_source(self):
        return None

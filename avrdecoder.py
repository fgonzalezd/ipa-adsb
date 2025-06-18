# This script takes an avro formatted file and extracts the ADSB raw messages
# to a text file.
# The avro is obtained from https://opensky-network.org/datasets/adsb

# Author        : Fernando Gonzalez
# Created on    : 6/17/2025
# Last update   : 6/17/2025

import pyModeS as pms
from fastavro import reader

avro_scr_file = "raw20150421_sample.avro"
raw_data = "raw_messages.txt"

with open(avro_scr_file, 'rb') as f, open(raw_data, 'w') as out_file:
    avro_reader = reader(f)
    for record in avro_reader:
        msg = record["rawMessage"]
        if msg:
            out_file.write(msg + "\n")
        #if pms.df(msg) == 17:
        #    print("ICAO:", pms.icao(msg), "Type Code:", pms.adsb.typecode(msg))

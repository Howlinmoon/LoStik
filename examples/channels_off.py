#!/usr/bin/env python3
import io
import sys
import time
import argparse

import serial
from serial.threaded import LineReader, ReaderThread

parser = argparse.ArgumentParser(description='Blink the LEDs.')
parser.add_argument('port', help="Serial port descriptor")
parser.add_argument('--delay', '-d', help="Delay in seconds as a decimal number.", type=float, default=.5)
args = parser.parse_args()

class PrintLines(LineReader):
    def connection_made(self, transport):
        super(PrintLines, self).connection_made(transport)
        print("port opened")

    def handle_line(self, data):
        print(data)

    def connection_lost(self, exc):
        print("port closed")

ser = serial.Serial(args.port, baudrate=57600)
delay = args.delay
with ReaderThread(ser, PrintLines) as protocol:
    protocol.write_line("sys get ver")
    time.sleep(.5)
    for channel in range(0, 73):
        print(f"Attempting to disable channel: {channel}")
        protocol.write_line(f"mac set ch status {channel} off")
        time.sleep(delay)

    print("Saving changes to the MAC!")
    protocol.write_line(f"mac save")
    time.sleep(delay)

    print("Done! (I hope)")
    exit(1)

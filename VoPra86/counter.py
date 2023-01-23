# -*- coding: utf-8 -*-
import serial as ps
import time
import io


class counter:
    def __init__(self, port="/dev/ortec_counter"):
        self.port = port
        self.openCounter()

    def openCounter(self):
        self.ser = ps.Serial(self.port, timeout=1, baudrate=9600)
        self.ser.read(self.ser.inWaiting())
        self.ser_io = io.TextIOWrapper(
            io.BufferedRWPair(self.ser, self.ser, 1), newline="\r", line_buffering=True
        )
        self.ser_io.write(unicode("COMPUTER\r"))
        self.ser_io.readline()
        self.ser_io.write(unicode("EN_REM\r"))
        self.ser_io.readline()
        self.ser_io.write(unicode("STO\r"))
        self.ser_io.readline()
        self.ser_io.write(unicode("CL_ALL\r"))  # Clear all
        self.ser_io.readline()
        self.ser_io.write(unicode("SET_DISP\s0\r"))  # Set Display 0
        self.ser_io.readline()

    def counts(self):
        """Returns number of counts in both channels"""
        self.ser.read(self.ser.inWaiting())
        self.ser_io.write(unicode("SHOW_COUNTS\r"))
        self.antwort = self.ser_io.readline().split(";")
        self.iCounts = [int(x) for x in self.antwort[0:2]]
        self.err = self.ser_io.readline()
        return self.iCounts

    def start(self):
        """Starts the counter"""
        self.ser_io.write(unicode("START\r"))
        self.ser_io.readline()

    def stop(self):
        """Stops the counter"""
        self.ser_io.write(unicode("STOP\r"))
        self.ser_io.readline()

    def clear(self):
        """Clears the counter"""
        self.ser_io.write(unicode("CL_ALL\r"))
        self.ser_io.readline()

    def __del__(self):
        del self.ser_io
        del self.ser


if __name__ == "__main__":
    c = counter()
    c.start()
    time.sleep(1)
    c.stop()
    print(c.counts())

import serial
import time
import numpy as np

DEVICE_ADDRESS = "/dev/steprocker"


class steprocker(object):
    def __init__(self, port=DEVICE_ADDRESS):
        self.port = port
        self.motor = 0
        self.address = 1
        self.timeout = 1
        self.cmdASC = ""
        self.cmd = ""

        self.openport()
        self.enableLimitSwitch()
        self.setGeschwind(2023)

        # self.schrittProMm = 1.56e-5
        # print(self.ser.readline())
        # self.te = [1,6,3,0,0,0,0,0,10]

    def openport(self):
        self.ser = serial.Serial(self.port)
        self.ser.timeout = self.timeout

    def command(self, instruction=0, ctype=0, value=0):
        cmd = str(np.base_repr(np.uint8(self.address), base=16, padding=2)[-2:])
        cmd += str(np.base_repr(np.uint8(instruction), base=16, padding=2)[-2:])
        cmd += str(np.base_repr(np.uint8(ctype), base=16, padding=2)[-2:])
        cmd += str(np.base_repr(np.uint8(self.motor), base=16, padding=2)[-2:])
        hexvalue = np.base_repr(np.uint32(value), base=16, padding=8)[-8:]
        cmd += hexvalue
        numhv = [int(hexvalue[x * 2 : x * 2 + 2], 16) for x in range(4)]
        checksum = sum(
            numhv
            + [
                np.uint8(self.address),
                np.uint8(instruction),
                np.uint8(ctype),
                np.uint8(self.motor),
            ]
        )
        cmd += np.base_repr(np.uint8(checksum), base=16, padding=2)[-2:]
        self.cmdASC = cmd
        self.cmd = ""
        for i in range(9):
            self.cmd += chr(int(cmd[i * 2 : i * 2 + 2], base=16))
        return cmd

    def sendCommand(self, cmd=None):
        if cmd == None:
            cmd = self.cmd
        self.ser.write(cmd)  # .encode())
        # time.sleep(1)
        ant1 = self.ser.read(9)
        # time.sleep(1)
        ant1 = [hex(ord(ant1[x])) for x in range(9)]  ### Wurm drin?
        ant2 = self.ser.read(9)
        ant2 = [hex(ord(ant2[x])) for x in range(len(ant2))]
        # print(ant1)
        # print(ant2)
        if self.port == DEVICE_ADDRESS:
            return ant1
        else:
            return ant2

    def setGeschwind(self, value):
        self.command(instruction=5, ctype=4, value=value)
        self.sendCommand()

    def geschwind(self):
        self.command(instruction=6, ctype=3)
        ant = self.sendCommand()
        ant = np.int8(int(ant[6][2:4] + ant[7][2:4], base=16))
        return ant

    def setBeschl(self, value):
        self.command(instruction=5, ctype=5, value=value)
        self.sendCommand()

    def enableLimitSwitch(self):
        self.command(instruction=5, ctype=12, value=0)
        self.sendCommand()
        self.command(instruction=5, ctype=13, value=0)
        self.sendCommand()

    def statusLimitSwitch(self):
        self.command(instruction=6, ctype=10)
        ant1 = int(self.sendCommand()[7], base=16)
        self.command(instruction=6, ctype=11)
        ant2 = int(self.sendCommand()[7], base=16)
        return [ant1, ant2]

    def fahreSchritte(self, value):
        self.langsam()
        self.command(instruction=4, ctype=1, value=value)
        self.sendCommand()

    def posEreicht(self):
        self.command(instruction=6, ctype=8)
        ant = self.sendCommand()
        ant = int(ant[7], base=16)
        return ant

    def stop(self):
        self.command(instruction=3, ctype=0, value=0)
        self.sendCommand()

    def rotRechts(self, value=1024):
        self.command(instruction=1, value=value)
        self.sendCommand()

    def rotLinks(self, value=1024):
        self.command(instruction=2, value=value)
        self.sendCommand()

    def schnell(self):
        self.setMicroStepResolution(5)

    def langsam(self):
        self.setMicroStepResolution(8)

    def setMicroStepResolution(self, value=8):
        self.command(instruction=5, ctype=140, value=value)
        self.sendCommand()

    def test(self):
        cmd = ""
        for x in self.te:
            cmd += chr(x)
        # cmd+=chr(self.checksum(self.te))
        print(repr(cmd))
        self.ser.write(cmd)
        a = self.ser.readline()
        print(repr(a))
        l = []
        for x in a:
            l.append(ord(x))
        print(repr(l))

    def __del__(self):
        self.ser.close()
        del self.ser


if __name__ == "__main__":
    s = steprocker()
    s.stop()

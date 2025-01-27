# based on the example from http://www.solarpoweredhome.co.uk/

from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from time import sleep
from sys import argv
from db import db
from os import path
import struct

def locateDevicePath():
    for i in range(2):
        dev=f'/dev/ttyXRUSB{i}'
        if path.exists(dev):
            return dev
    return None
def getFloat(bits):
    s = struct.pack('>L',bits)
    return struct.unpack('>f', s)[0]

client = ModbusClient(method = 'rtu', port = locateDevicePath(), baudrate = 115200)
client.connect()
print(len(argv))
print(locateDevicePath())
if len(argv) > 1:
    devId = int(argv[1])
else:
    print(f"usage: {argv[0]} devId")
    quit()
if True:
    result = client.read_input_registers(0x3100,16,unit=devId)
    dat = {}
    dat['solarVoltage'] = float(result.registers[0] / 100.0)
    dat['solarCurrent'] = float(result.registers[1] / 100.0)
    dat['batteryVoltage'] = float(result.registers[4] / 100.0)
    dat['chargeCurrent'] = float(result.registers[5] / 100.0)
    dat['chargePower'] = float(((result.registers[7]<<16) + result.registers[6])/ 100.0)
    dat['loadVoltage'] = float(result.registers[12] / 100.0)
    dat['loadCurrent'] = float(result.registers[13] / 100.0)
    dat['loadPower'] = float(((result.registers[15]<<16) + result.registers[14])/ 100.0)
   # dat['remoteBatteryTemp'] = float(result.registers[27] / 100.0)
    
    result = client.read_input_registers(0x3300,31,unit=devId)
    dat['maxInputVoltageToday'] = float(result.registers[0] / 100.0)
    dat['minInputVoltageToday'] = float(result.registers[1] / 100.0)
    dat['maxBatteryVoltageToday'] = float(result.registers[2] / 100.0)
    dat['minBatteryVoltageToday'] = float(result.registers[3] / 100.0)
    dat['generatedEnergyToday'] = float((result.registers[13]*100 + result.registers[12]) / 100.0)
    dat['generatedEnergyThisMonth'] = float(((result.registers[15]<<16) + result.registers[14]) / 100.0)
    dat['generatedEnergyThisYear'] = float(((result.registers[17]<<16) + result.registers[16]) / 100.0)
    dat['generatedEnergyTotal'] = float(((result.registers[19]<<16) + result.registers[18]) / 100.0)
 
    # Do something with the data
    for (k,v) in dat.items():
        print(f'{k:} {v}')
    db.dbsave(f"pv_{devId}",dat)

#print("Load Power: " + str(loadPower))
    
    sleep(5)

client.close()

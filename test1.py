from dronekit import VehicleMode, connect
import threading
import time, logging
import sys

logging.basicConfig(filename="debug.log",level=logging.DEBUG,format='%(asctime)s,%(msecs)d %(name)s %(message)s')   #LOG FILE FOR DEBUGGING
logging.basicConfig(filename="error.log",level=logging.ERROR,format='%(asctime)s,%(msecs)d %(name)s %(message)s')   #LOG FILR FOR ERRORS

#Connect to vehicles
def connect_vehicle(vehicle_address,call_id):
    try:
        vehicle = connect(vehicle_address, wait_ready=True)
        print("CONNECTED TO VEHICLE " + call_id)
        logging.debug("CONNECTED TO VEHICLE " + call_id)
        return vehicle
    except:
        print("CONNECTION FAILED")
        logging.error("CONNECTION FAILED")
        return 0

def arm_and_takeoff(vehicle,height,call_id):
    print("CHECKING IF ARMABLE")
    logging.debug("CHECKING IF ARMABLE")

    timeout = time.time()+60*5
    while not vehicle.is_armable:
        print("WAITING FOR VEHICLE TO INITIALIZE")
        time.sleep(2)
        if(time.time()>timeout):
            print("TIMEOUT ERROR")
            logging.error("TIMEOUT ERROR")
            sys.exit()
    print("VEHICLE ARMABLE" + (call_id))
    logging.debug("VEHICLE ARMABLE" + (call_id))

vehicle = connect_vehicle("/dev/ttyUSB0")

while (vehicle.mode != VehicleMode("GUIDED")):
    vehicle.mode = VehicleMode("GUIDED")
    time.sleep(2)

if __name__ == "__main__":
    blinky = connect_vehicle('address','blinky')
    buggy = connect_vehicle('address','buggy')
from dronekit import VehicleMode, connect
import threading, time, logging, sys

logging.basicConfig(filename="debug.log",level=logging.DEBUG,format='%(asctime)s,%(msecs)d %(name)s %(message)s')   #LOG FILE FOR DEBUGGING
logging.basicConfig(filename="error.log",level=logging.ERROR,format='%(asctime)s,%(msecs)d %(name)s %(message)s')   #LOG FILR FOR ERRORS

def connect_vehicle(vehicle_address):
    try:
        vehicle = connect(vehicle_address, wait_ready=True)
        print("CONNECTED TO VEHICLE")
        logging.debug("CONNECTED TO VEHICLE")
        return vehicle
    except:
        print("Connection Failed")
        logging.error("CONNECTION FAILED")
        return 0

def arm_and_takeoff(height):
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
    print("VEHICLE ARMABLE")
    logging.debug("VEHICLE ARMABLE")

vehicle = connect_vehicle("/dev/ttyUSB0")


from flask import Flask
from dronekit import VehicleMode, connect,Vehicle
import time,sys,threading
import json,csv

#################
#Global Variables
#################
logging_flag = False
call_id = """
<pre>
#####################################################
__________.____    .___ _______   ____  __._____.___.
\______   \    |   |   |\      \ |    |/ _|\__  |   |
 |    |  _/    |   |   |/   |   \|      <   /   |   |
 |    |   \    |___|   /    |    \    |  \  \____   |
 |______  /_______ \___\____|__  /____|__ \ / ______|
        \/        \/           \/        \/ \/
#####################################################
</pre>
"""
call_id_2="""
<pre>
#####################################################
__________ ____ ___  ________  _____________.___.
\______   \    |   \/  _____/ /  _____/\__  |   |
 |    |  _/    |   /   \  ___/   \  ___ /   |   |
 |    |   \    |  /\    \_\  \    \_\  \\____   |
 |______  /______/  \______  /\______  // ______|
        \/                 \/        \/ \/      
#####################################################
</pre>
"""
log_file = open('logging_beast.csv',mode='w')
log_writer = csv.writer(log_file,delimiter=',')
log_writer.writerow(["GPS Alt","Baro Alt","IMU Alt"])

msg = ''
gps_loc = ''
##################
#Dronekit commands
##################

def connect_vehicle(vehicle_address):
    try:
        global quad
        global msg
        vehicle = connect(vehicle_address, wait_ready=True)
        msg = ("CONNECTED TO VEHICLE " + call_id)
        # logging.debug("CONNECTED TO VEHICLE " + call_id)
        quad = vehicle
        return vehicle
    except:
        msg="CONNECTION FAILED"
        # logging.error("CONNECTION FAILED")
        return False

path = '/dev/ttyACM0'

quad = connect_vehicle(path)

@quad.on_attribute('location.global_frame')
def listener(self, attr_name, value):
    global gps_loc
    gps_loc = value

def not_connected():
    if(quad==''):
        msg = "VEHICLE NOT CONNECTED"
        return True
    else:
        return False

def arm(vehicle):
    if(not_connected()):
        return
    print("CHECKING IF ARMABLE")
    # logging.debug("CHECKING IF ARMABLE")

    # timeout = time.time()+60*5
    # while not vehicle.is_armable:
    #     print("WAITING FOR VEHICLE TO INITIALIZE")
    #     time.sleep(2)
    #     if(time.time()>timeout):
    #         print("TIMEOUT ERROR")
    #         # logging.error("TIMEOUT ERROR")
    #         sys.exit()
    vehicle.mode = VehicleMode("GUIDED")
    while  not vehicle.mode == VehicleMode("GUIDED"):
        print("AWAITING VEHICLE")
        time.sleep(0.1)
    print("VEHICLE MODE SET TO GUIDED")
    print("ARMING")
    vehicle.armed = True
    while not vehicle.armed:
        print("AWAITING VEHICLE")
    global msg
    msg = ((call_id)+ "VEHICLE ARMED & READY FOR LIFTOFF")
    # logging.debug("VEHICLE ARMABLE" + (call_id))

def arm_and_takeoff(vehicle,height):
    if(not_connected()):
        return
    arm(vehicle)
    vehicle.simple_takeoff(height)
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= height * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

def logging(rate,stop_event):
    global logging_flag
    while not stop_event.is_set():
        try:
            if(logging_flag):
                global quad
                global log_writer
                global log_file
                global gps_loc
                log_writer.writerow([gps_loc,"Current Baro Alt","Gibberish"])
                time.sleep(0.1)
            else:
                time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            log_file.close()

def logging_flag_handler(option):
    global logging_flag
    if(option == 'start'):
        logging_flag=True
    elif(option == 'stop'):
        logging_flag=False

def disarm():
    global quad
    global msg
    quad.armed = False
    while not quad.armed == False:
        quad.armed = False
        time.sleep(0.1)
    msg = 'DISARMED'
##################
#Server Code
##################

app = Flask(__name__)
@app.route("/")
def index():
    return "Index!"

@app.route("/command/connect/")
def connect_handler ():
    global  msg
    connect_vehicle(path)
    return msg

@app.route("/command/id/")
def id_handler():
    return call_id

@app.route("/command/arm/")
def arm_handler():
    arm(quad)
    return msg

@app.route("/command/disarm/")
def disarm_handler():
    disarm()
    return msg

@app.route("/command/takeoff/<float:alt>")
def takeoff_handler(alt):
    arm_and_takeoff(quad,alt)
    return msg
# @app.route("/command/current_alt/")
# def cur_alt_handler():
#     global quad
#     return quad.global_frame.

@app.route("/logging/<string:option>/")
def logging_handler(option):
    logging_flag_handler(option)
    if(option == 'start'):
        return "LOGGING BEAST ACTIVE..."
    elif(option == 'stop'):
        return "LOGGING BEAST OFFLINE"
    else:
        return null
    

app.debug = True
rate = 0.2
stop_event = threading.Event()
log_thread = threading.Thread(target=logging,daemon=True,args=(rate, stop_event))
log_thread.start()
print("Running")
app.run()
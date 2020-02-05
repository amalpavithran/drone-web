from flask import Flask
from dronekit import VehicleMode, connect,Vehicle
import time,sys,threading
import json,csv

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
quad = ''
msg = ''
##################
#Dronekit commands
##################
path = '/dev/ttyACM0'
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

def arm(vehicle):
    print("CHECKING IF ARMABLE")
    # logging.debug("CHECKING IF ARMABLE")

    timeout = time.time()+60*5
    while not vehicle.is_armable:
        print("WAITING FOR VEHICLE TO INITIALIZE")
        time.sleep(2)
        if(time.time()>timeout):
            print("TIMEOUT ERROR")
            # logging.error("TIMEOUT ERROR")
            sys.exit()
    print("VEHICLE ARMABLE" + (call_id))
    # logging.debug("VEHICLE ARMABLE" + (call_id))

def arm_and_takeoff(vehicle,height):
    arm(vehicle)
    vehicle.is_armed = True

def logging(rate,stop_event):
    while not stop_event.is_set():
        try:
            time.sleep(rate)
            global log_writer
            global log_file
            log_writer.writerow(["Current GPS Alt","Current Baro Alt","Gibberish"])
        except (KeyboardInterrupt, SystemExit):
            log_file.close()
            
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
    vehicle = connect_vehicle(path)
    return msg

@app.route("/command/id/")
def id_handler():
    return call_id

@app.route("/logging/<string:option>/")
def logging_handler(option):
    if(option == 'start'):
        log_thread.start()
        return "LOGGING BEAST ACTIVE..."
    elif(option == 'stop'):
        stop_event.set()
        log_file.close()
        return "LOGGING BEAST OFFLINE"
    

app.debug = True
rate = 0.2
stop_event = threading.Event()
log_thread = threading.Thread(target=logging,daemon=True,args=(rate, stop_event))
print("Running")
app.run()
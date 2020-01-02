import websockets,asyncio,threading,logging
from dronekit import VehicleMode, connect
import time,sys
import json
logging.basicConfig(filename="debug.log",level=logging.DEBUG,format='%(asctime)s,%(msecs)d %(name)s %(message)s')   #LOG FILE FOR DEBUGGING
logging.basicConfig(filename="error.log",level=logging.ERROR,format='%(asctime)s,%(msecs)d %(name)s %(message)s')   #LOG FILR FOR ERRORS

call_id = """
#####################################################
__________.____    .___ _______   ____  __._____.___.
\______   \    |   |   |\      \ |    |/ _|\__  |   |
 |    |  _/    |   |   |/   |   \|      <   /   |   |
 |    |   \    |___|   /    |    \    |  \  \____   |
 |______  /_______ \___\____|__  /____|__ \ / ______|
        \/        \/           \/        \/ \/
#####################################################
    [1] Connect
    [2] Arm & TakeOff
    [3] Arm
"""
#Command to override rc channel inputs
#vehicle.channels.overrides = {'5':None, '6':None,'3':500}
path = '/dev/ttyUSB0'

def connect_vehicle(vehicle_address):
    try:
        vehicle = connect(vehicle_address, wait_ready=True)
        print("CONNECTED TO VEHICLE " + call_id)
        logging.debug("CONNECTED TO VEHICLE " + call_id)
        return vehicle
    except:
        print("CONNECTION FAILED")
        logging.error("CONNECTION FAILED")
        return False

def arm(vehicle):
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

def arm_and_takeoff(vehicle,height):
    arm(vehicle)
    vehicle.is_armed = True

async def command_get(websocket, path):
    command = await websocket.recv()
    print("Ready")
    await websocket.send(f'{command}')
    command = json.loads(f'{command}')['command']
    #Connect to Vehicle
    if f'{command}' == 'id':
        await websocket.send(f'< {call_id}')
    elif 'start' in f'{command}' or f'{command}'=='1':
        if(f'{command}'==1):
            path = '/dev/ttyUSB0'
        else:
            path = f'{command}'.split(' ')[1]
            print(path)
            logging.debug(f'PATH SET TO: {path}')
        vehicle = await connect_vehicle(f'{path}')
        if not vehicle:
            logging.error("CONNECTION FAILED")
            await websocket.send(f'CONNECTION FAILED')
        else:
            logging.debug("CONNECTED")
            print("<CONNECTED")
            await websocket.send(f'<CONNECTED')
            return vehicle
    elif f'{command}' == 'arm':
        await websocket.send('<ARMING')
    elif f'{command}' == 'exit':
        await websocket.send('<EXITING')
        asyncio.get_event_loop().stop()
    else:
        await websocket.send(f'<INVALID INPUT')
    # await websocket.send(greeting)
    # print(f"> {greeting}")

start_server = websockets.serve(command_get, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
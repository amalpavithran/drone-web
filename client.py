import websockets,asyncio,threading,logging
from dronekit import VehicleMode, connect
import time,sys
import json
hello = {"name":"Amal","command":"1"}

async def command_interface():
    uri = "ws://localhost:8765"
    while True:
        async with websockets.connect(uri) as websocket:
            command = input(">>")
            hello['command'] = command
            await websocket.send(json.dumps(hello))
            # print(f'>{command}')

            try:
                greeting = await websocket.recv()
                next = await websocket.recv()
            except:
                print("Exception Raised: ",sys.exc_info()[0])
            print(f"<{greeting}")
            print(f'<{next}')
            if(command=='exit'):
                asyncio.get_event_loop().stop
                sys.exit()
# async def main():
#     while(await command_interface()):
#         continue
# asyncio.run
asyncio.get_event_loop().run_until_complete(command_interface())
asyncio.get_event_loop().run_forever()
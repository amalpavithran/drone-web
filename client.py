import websockets,asyncio,threading,logging
from dronekit import VehicleMode, connect
import time,sys

async def command_interface():
    uri = "ws://localhost:8765"
    while True:
        async with websockets.connect(uri) as websocket:
            command = input(">>")
            await websocket.send(command)
            # print(f'>{command}')

            try:
                greeting = await websocket.recv()
            except:
                print('ERROR')
            print(f"<{greeting}")
            if(command=='exit'):
                asyncio.get_event_loop().stop
# async def main():
#     while(await command_interface()):
#         continue
# asyncio.run
asyncio.get_event_loop().run_until_complete(command_interface())
asyncio.get_event_loop().run_forever()
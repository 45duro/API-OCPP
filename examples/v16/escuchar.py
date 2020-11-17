#!/usr/bin/env python

import asyncio
import websockets
import json

async def hello(uri):
    
    async with websockets.connect(uri) as websocket:
        x = '[2, "12345", "BootNotification", {"chargePointVendor": "The Mobility House", "chargePointModel": "Optimus"}]'
        y = json.loads(x)
        #await websocket.send(x)
        #print("< ", x)

        texto = await websocket.recv()
        print (">", texto)

        
        if (texto):
            await websocket.send("recibido")
        

'''
asyncio.get_event_loop().run_until_complete(
    hello('ws://localhost:9000/cargador1'))
'''
try:
    asyncio.run(
        hello('ws://localhost:9000/cargador1')
    )

finally:
    pass
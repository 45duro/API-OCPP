import asyncio
import logging
from datetime import datetime
import json

try:
    import websockets
except ModuleNotFoundError:
    print("This example relies on the 'websockets' package.")
    print("Please install it by running: ")
    print()
    print(" $ pip install websockets")
    import sys
    sys.exit(1)

#from ocpp.routing import on, after
from ocpp.v16 import call, call_result
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import RegistrationStatus, ChargePointErrorCode, ChargePointStatus, Reason, Action, RemoteStartStopStatus
from ocpp.routing import on, after

logging.basicConfig(level=logging.INFO)


class ChargePoint(cp):
    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charge_point_model="Digital Spaces",
            charge_point_vendor="Mercacentro"
        )
        

        response = await self.call(request)

        if response.status == RegistrationStatus.accepted:
            print("Connected to central system.")
    
    async def send_authorize(self):
        request1 = call.AuthorizePayload(
            id_tag="miTagId9999" 
            )

        response2 = await self.call(request1)
        #print(response2)
    
    async def send_start_transaction(self):
        request2 = call.StartTransactionPayload(
            connector_id=12,
            id_tag="miTagId9999",
            meter_start=20,
            timestamp=str(datetime.utcnow().isoformat())
            )
        response2 = await self.call(request2)
        #print(response2)
    
    async def heartbeat(self):
        request2 = call.HeartbeatPayload (  
            )
        response2 = await self.call(request2)
    
    
    async def send_status_notification(self):
        request2 = call.StatusNotificationPayload (
            connector_id=12,
            error_code= ChargePointErrorCode.noError,
            status = ChargePointStatus.available,
            timestamp=str(datetime.utcnow().isoformat()),
            info= "Accepted",
            vendor_id = "JonathanVendor", 
            vendor_error_code = "noError"
            
            )
        response2 = await self.call(request2)
    
    async def send_stop_transaction(self):
        
        request = call.StopTransactionPayload(
            #transaction_id = 12,
            timestamp= str(datetime.utcnow().isoformat()),
            meter_stop = 90,
            transaction_id = 12
            #reason = Reason.emergencyStop
            

        )

        response2 = await self.call(request)

    @on(Action.RemoteStartTransaction)
    def on_remote_start_transaction(self, id_tag: str, connector_id: int, **kwargs):
        
        print ("recibiendo Start Remoto")
        return call_result.RemoteStartTransactionPayload(
            status = "Accepted"
        )

    @after(Action.RemoteStartTransaction)
    def printer(self, id_tag: str, connector_id: int, **kwargs):
        print ("recibiendo Start Remoto de: ", id_tag)



    @on(Action.RemoteStopTransaction)
    def on_remote_stop_transaction(self, transaction_id: str, **kwargs):
        
        print ("recibiendo Stop Remoto")
        return call_result.RemoteStopTransactionPayload(
            status = "Accepted"
        )

    @after(Action.RemoteStopTransaction)
    def printer2(self, transaction_id: str, **kwargs):
        print ("se ha parado la transaccion id: ", transaction_id)



async def main():
    async with websockets.connect(
        #'ws://149.56.47.168:8080/PCremote',
        'ws://localhost:9000/PCremote',
        subprotocols=['ocpp1.6']
    ) as ws:

        #x = '[3, "12345", {"currentTime": "2019-06-16T11:18:09.591716", "interval": 10, "status": "Accepted"}]'

        #await ws.send(x)

        #greeting = await ws.recv()
        #print(f"< {greeting}")

        cp = ChargePoint('PCremote', ws)

        await asyncio.gather(
            cp.start(), 
            cp.send_boot_notification(),
            cp.send_authorize(),
            #cp.send_start_transaction(),
            cp.heartbeat(),
            cp.send_status_notification()
            #cp.send_stop_transaction()
            #cp.remote_start_transaction()

            )
        
        
        



if __name__ == '__main__':
    try:
        # asyncio.run() is used when running this example with Python 3.7 and
        # higher.
        asyncio.run(main())
    except AttributeError:
        # For Python 3.6 a bit more code is required to run the main() task on
        # an event loop.
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.close()

import asyncio
import logging
from datetime import datetime

try:
    import websockets
except ModuleNotFoundError:
    print("This example relies on the 'websockets' package.")
    print("Please install it by running: ")
    print()
    print(" $ pip install websockets")
    import sys
    sys.exit(1)

from ocpp.routing import on, after
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import Action, RegistrationStatus, AuthorizationStatus
from ocpp.v16 import call_result

logging.basicConfig(level=logging.INFO)


class ChargePoint(cp):
    @on(Action.BootNotification)
    def on_boot_notitication(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status=RegistrationStatus.accepted
        )

    @after(Action.BootNotification)
    def after_boot_notification(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        print("JHoider tio...........")

    
    try:
        @on(Action.Authorize)
        def on_authorize_response(self, id_tag: str):
            print("He recibido: ", id_tag)
            
            return call_result.AuthorizePayload(
                id_tag_info={
                    "status" : AuthorizationStatus.accepted
                }
            )
            
    except: 
        print("No se puede hacer la transaccion")
    
    
    @on(Action.StartTransaction)
    def on_start_transaction(self, connector_id: int, id_tag: str, meter_start: int, timestamp: str, **kwargs):
        return call_result.StartTransactionPayload(
            transaction_id=connector_id,
            id_tag_info={
                "status" : AuthorizationStatus.accepted
            }
        )

    
    @after(Action.StartTransaction)
    def imprimirJoder(self, connector_id: int, id_tag: str, meter_start: int, timestamp: str, **kwargs):
        print("Joder tio")
    

async def on_connect(websocket, path):
    """ For every new charge point that connects, create a ChargePoint instance
    and start listening for messages.

    """
    charge_point_id = path.strip('/')
    cp = ChargePoint(charge_point_id, websocket)

    await cp.start()


async def main():
    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        9000,
        subprotocols=['ocpp1.6']
    )

    await server.wait_closed()


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

import asyncio
import websockets

# HOST = "irrigationsystem.onrender.com"
HOST = "localhost:8000"
IDENTIFIER = "A1L1D1U1"

async def listen(unique_identifier: str):
    uri = f"ws://{HOST}/ws/{unique_identifier}"
    try:
        async with websockets.connect(uri) as websocket:
            # waiting for auth
            auth_message = await websocket.recv()
            if auth_message != "Authorised":
                print(f"Неавторизований агент: {auth_message}")
                return
            print(f"Підключено до WebSocket як {unique_identifier}")

            # listen server
            while True:
                message = await websocket.recv()
                print(f"Отримано повідомлення: {message}")
    except websockets.exceptions.ConnectionClosed as e:
        print(f"З'єднання закрито: {e.code} - {e.reason}")
    except Exception as e:
        print(f"Виникла помилка: {e}")


asyncio.get_event_loop().run_until_complete(listen(IDENTIFIER))

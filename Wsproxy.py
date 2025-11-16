import asyncio
import websockets
import aiohttp

BACKEND_URL = "http://<YOUR_SERVER_IP>:8080"  # Replace with your backend IP/port
LISTEN_PORT = 8081

async def handle_ws(websocket, path):
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(BACKEND_URL.replace("http", "ws")) as backend:
            async def ws_to_backend():
                async for msg in websocket:
                    await backend.send_str(msg)

            async def backend_to_ws():
                async for msg in backend:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        await websocket.send(msg.data)

            await asyncio.gather(ws_to_backend(), backend_to_ws())

async def main():
    print(f"Railway WebSocket proxy running on 0.0.0.0:{LISTEN_PORT}")
    async with websockets.serve(handle_ws, "0.0.0.0", LISTEN_PORT):
        await asyncio.Future()

asyncio.run(main())

# import asyncio
# from time import sleep, time

# fake_users = [
#     {'id': 1, 'name': 'April Murphy', 'company': 'Bailey Inc', 'email': 'shawnlittle@example.org'},
#     {'id': 2, 'name': 'Emily Alexander', 'company': 'Martinez-Smith', 'email': 'turnerandrew@example.org'},
#     {'id': 3, 'name': 'Patrick Jones', 'company': 'Young, Pruitt and Miller', 'email': 'alancoleman@example.net'}
# ]


# def get_user_sync(uid: int) -> dict:
#     sleep(0.5)
#     user, = list(filter(lambda user: user["id"] == uid, fake_users))
#     return user

# async def get_user_async(uid: int) -> dict:
#     await asyncio.sleep(0.5)
#     user, = list(filter(lambda user: user["id"] == uid, fake_users))
#     return user


# async def main():
#     r = []
#     for i in range(1, 4):
#         r.append(get_user_async(i))
#     return await asyncio.gather(*r)

    
# if __name__ == '__main__':
#     print('------Synchronous Request-----')
#     start = time()
#     for i in range(1, 4):
#         print(get_user_sync(i))
#     print(time() - start)
#     print('------Asynchronous Request-----')
#     start = time()
#     result = asyncio.run(main())
#     for r in result:
#         print(r)
#     print(time() - start)


# import asyncio
# import concurrent.futures
# from time import time


# def blocks(n):
#     counter = n
#     start = time()
#     while counter > 0:
#         counter -= 1
#     return time() - start


# async def monitoring():
#     while True:
#         await asyncio.sleep(2)
#         print(f'Monitoring {time()}')


# async def run_blocking_tasks(executor, n):
#     loop = asyncio.get_event_loop()
#     print('waiting for executor tasks')
#     result = await loop.run_in_executor(executor, blocks, n)
#     return result


# async def main():
#     asyncio.create_task(monitoring())
#     with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
#         futures = [run_blocking_tasks(executor, n) for n in [50_000_000, 60_000_000, 70_000_000]]
#         results = await asyncio.gather(*futures)
#         return results


# if __name__ == '__main__':
#     result = asyncio.run(main())
#     for r in result:
#         print(r)


# import asyncio
# import requests
# from concurrent.futures import ThreadPoolExecutor
# from time import time

# urls = ['http://www.google.com', 'http://www.python.org', 'http://duckduckgo.com']


# def preview_fetch(url):
#     r = requests.get(url)
#     return url, r.text[:150]


# async def preview_fetch_async():
#     loop = asyncio.get_running_loop()

#     with ThreadPoolExecutor(3) as pool:
#         futures = [loop.run_in_executor(pool, preview_fetch, url) for url in urls]
#         result = await asyncio.gather(*futures)
#         return result


# import platform

# import aiohttp
# import asyncio


# async def main():

#     async with aiohttp.ClientSession() as session:
#         async with session.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5') as response:

#             print("Status:", response.status)
#             print("Content-type:", response.headers['content-type'])
#             print('Cookies: ', response.cookies)
#             print(response.ok)
#             result = await response.json()
#             return result


# if __name__ == "__main__":
#     if platform.system() == 'Windows':
#         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     r = asyncio.run(main())
#     print(r)


# import asyncio
# import requests
# from concurrent.futures import ThreadPoolExecutor
# from time import time

# urls = ['http://www.google.com', 'http://www.python.org', 'http://duckduckgo.com']


# def preview_fetch(url):
#     r = requests.get(url)
#     return url, r.text[:150]


# async def preview_fetch_async():
#     loop = asyncio.get_running_loop()

#     with ThreadPoolExecutor(3) as pool:
#         futures = [loop.run_in_executor(pool, preview_fetch, url) for url in urls]
#         result = await asyncio.gather(*futures)
#         return result


# if __name__ == '__main__':
#     start = time()
#     r = asyncio.run(preview_fetch_async())
#     print(r)
#     print(time() - start)


# import platform

# import aiohttp
# import asyncio


# async def main():

#     async with aiohttp.ClientSession() as session:
#         async with session.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5') as response:

#             print("Status:", response.status)
#             print("Content-type:", response.headers['content-type'])
#             print('Cookies: ', response.cookies)
#             print(response.ok)
#             result = await response.json()
#             return result


# if __name__ == "__main__":
#     if platform.system() == 'Windows':
#         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     r = asyncio.run(main())
#     print(r)

# import aiohttp
# import asyncio
# import platform

# urls = ['https://www.google.com', 'https://www.python.org/asdf', 'https://duckduckgo.com', 'http://test']


# async def main():
#     async with aiohttp.ClientSession() as session:
#         for url in urls:
#             print(f'Starting {url}')
#             try:
#                 async with session.get(url) as resp:
#                     if resp.status == 200:
#                         html = await resp.text()
#                         print(url, html[:150])
#                     else:
#                         print(f"Error status: {resp.status} for {url}")
#             except aiohttp.ClientConnectorError as err:
#                 print(f'Connection error: {url}', str(err))


# if __name__ == '__main__':
#     if platform.system() == 'Windows':
#         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     asyncio.run(main())

# import asyncio
# import websockets


# async def handler(websocket, path):
#     data = await websocket.recv()
#     reply = f"Data recieved as:  {data}!"
#     print(reply)
#     await websocket.send(reply)


# async def main():
#     async with websockets.serve(handler, "0.0.0.0", 81):
#         await asyncio.Future()  # run forever

# if __name__ == '__main__':
#     asyncio.run(main())

# import asyncio
# import logging
# import websockets

# logging.basicConfig(level=logging.INFO)

# async def consumer(hostname: str, port: int):
#     ws_resource_url = f"ws://{hostname}:{port}"
#     async with websockets.connect(ws_resource_url) as ws:
#         async for message in ws:
#             logging.info(f"Message: {message}")

# if __name__ == '__main__':
#     asyncio.run(consumer('localhost', 4000))


# import asyncio
# import logging
# import websockets
# from websockets import WebSocketServerProtocol
# import names
# from websockets.exceptions import ConnectionClosedOK

# logging.basicConfig(level=logging.INFO)

# class Server:
#     clients = set()

#     async def register(self, ws: WebSocketServerProtocol):
#         ws.name = names.get_full_name()
#         self.clients.add(ws)
#         logging.info(f'{ws.remote_address} connects')

#     async def unregister(self, ws: WebSocketServerProtocol):
#         self.clients.remove(ws)
#         logging.info(f'{ws.remote_address} disconnects')

#     async def send_to_clients(self, message: str):
#         if self.clients:
#             [await client.send(message) for client in self.clients]

#     async def ws_handler(self, ws: WebSocketServerProtocol):
#         await self.register(ws)
#         try:
#             await self.distrubute(ws)
#         except ConnectionClosedOK:
#             pass
#         finally:
#             await self.unregister(ws)

#     async def distrubute(self, ws: WebSocketServerProtocol):
#         async for message in ws:
#              await self.send_to_clients(f"{ws.name}: {message}")


# async def main():
#     server = Server()
#     async with websockets.serve(server.ws_handler, '0.0.0.0', 81):
#         await asyncio.Future()  # run forever

# if __name__ == '__main__':
#     asyncio.run(main())


import asyncio
import logging
import websockets
from websockets import WebSocketServerProtocol
import names
from websockets.exceptions import ConnectionClosedOK

logging.basicConfig(level=logging.INFO)



class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
             await self.send_to_clients(f"{ws.name}: {message}")


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, '0.0.0.0', 81):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())

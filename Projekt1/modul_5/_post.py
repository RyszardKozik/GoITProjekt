# from http.server import HTTPServer, BaseHTTPRequestHandler

# class HttpHandler(BaseHTTPRequestHandler):
#     def do_POST(self):
#         data = self.rfile.read(int(self.headers['Content-Length']))
#         print(data)
#         self.send_response(201)
#         self.end_headers()
#         self.wfile.write(b'Done request!' + data)

#     def do_GET(self):
#         self.send_response(200)
#         self.end_headers()
#         self.wfile.write(b'Hello, world!')

# def run(server_class=HTTPServer, handler_class=HttpHandler):
#     server_address = ('', 5000)
#     http = server_class(server_address, handler_class)
#     try:
#         http.serve_forever()
#     except KeyboardInterrupt:
#         http.server_close()

# if __name__ == '__main__':
#     run()


# import platform

# import aiohttp
# import asyncio
# from uuid import uuid4

# async def main():
#     async with aiohttp.ClientSession() as session:
#         async with session.post('http://localhost:5000', data={"message": "Hello world!"}, ssl=False) as response:

#             print("Status:", response.status)
#             html = await response.text()
#             return f"Body: {html}"

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

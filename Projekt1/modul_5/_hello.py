# import asyncio
# from aiopath import AsyncPath

# async def main():
#     apath = AsyncPath("hello.txt")
#     print(await apath.exists())
#     print(await apath.is_file())
#     print(await apath.is_dir())

# if __name__ == '__main__':
#     asyncio.run(main())


# import asyncio
# from aiofile import async_open

# async def main():
#     async with async_open("hello.txt", 'w+') as afp:
#         await afp.write("Hello ")
#         await afp.write("world\n")
#         await afp.write("Hello from - async world!")

# if __name__ == '__main__':
#     asyncio.run(main())

# import asyncio
# from aiofile import async_open

# async def main():
#     async with async_open("hello.txt", 'w+') as afp:
#         await afp.write("Hello ")
#         await afp.write("world\n")
#         await afp.write("Hello from - async world!")

# if __name__ == '__main__':
#     asyncio.run(main())

# import asyncio
# from aiofile import async_open

# async def main():
#     async with async_open("hello.txt", 'r') as afp:
#         print(await afp.read())

# if __name__ == '__main__':
#     asyncio.run(main())


# import asyncio
# from aiofile import AIOFile, LineReader

# async def main():
#     async with AIOFile("hello.txt", 'r') as afp:
#         async for line in LineReader(afp):
#             print(line)

# if __name__ == '__main__':
#     asyncio.run(main())

# import asyncio
# from aiopath import AsyncPath

# async def main():
#     apath = AsyncPath("hello.txt")
#     print(await apath.exists())
#     print(await apath.is_file())
#     print(await apath.is_dir())

# if __name__ == '__main__':
#     asyncio.run(main())


# import asyncio
# from aiopath import AsyncPath
# from aioshutil import copyfile

# async def main():
#     apath = AsyncPath("hello.txt")
#     if await apath.exists():
#         new_path = AsyncPath('logs')
#         await new_path.mkdir(exist_ok=True, parents=True)
#         await copyfile(apath, new_path / apath)

# if __name__ == '__main__':
#     asyncio.run(main())

# import platform

# import aiohttp
# import asyncio

# async def main():

#     session = aiohttp.ClientSession()
#     response = await session.get('https://python.org')

#     print("Status:", response.status)
#     print("Content-type:", response.headers['content-type'])

#     html = await response.text()
#     response.close()

#     await session.close()
#     return f"Body: {html[:15]}..."

# if __name__ == "__main__":
#     if platform.system() == 'Windows':
#         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     r = asyncio.run(main())
#     print(r)

# import platform

# import aiohttp
# import asyncio

# async def index(session):
#     url = 'https://python.org'
#     async with session.get(url) as response:
#         print("Status:", response.status)
#         print("Content-type:", response.headers['content-type'])

#         html = await response.text()
#         return f"Body: {html[:15]}..."

# async def doc(session):
#     url = "https://www.python.org/doc/"
#     async with session.get(url) as response:
#         print("Status:", response.status)
#         print("Content-type:", response.headers['content-type'])

#         html = await response.text()
#         return f"Body: {html[:15]}..."

# async def main():
#     async with aiohttp.ClientSession() as session:
#         result = await asyncio.gather(index(session), doc(session))
#         return result

# if __name__ == "__main__":
#     if platform.system() == 'Windows':
#         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     r = asyncio.run(main())
#     print(r)

import platform

import aiohttp
import asyncio
from uuid import uuid4

async def main():
    timeout = aiohttp.ClientTimeout(total=1)
    async with aiohttp.ClientSession(
        headers={"Request-Id": str(uuid4())},
        timeout=timeout,
    ) as session:
        async with session.get('https://python.org') as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.text()
            return f"Body: {html[:15]}..."

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
    print(r)

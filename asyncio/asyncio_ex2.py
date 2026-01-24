import asyncio

async def brew(name):
    print(f"Brewing {name}...")
    await asyncio.sleep(2)
    print(f"{name} is ready")

async def main():
    await asyncio.gather(
        brew('chai'),
        brew('coffee'),
        brew('Ginger tea'),
    )

asyncio.run(main())



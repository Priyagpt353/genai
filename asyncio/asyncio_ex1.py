import asyncio  # Step 1: Import the asyncio module

async def brew_chai():  # Step 2: Define an asynchronous function
  print("Brewing chai...")
  await asyncio.sleep(2)
  print("Chai is ready") # this line will be print after 2 seconds delay

asyncio.run(brew_chai()) # Step 3: Run the asynchronous function using asyncio.run()




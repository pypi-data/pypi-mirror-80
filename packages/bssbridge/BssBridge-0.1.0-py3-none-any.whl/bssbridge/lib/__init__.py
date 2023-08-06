def periodic(period):
  def scheduler(fcn):
    async def wrapper(*args, **kwargs):
      import asyncio
      while True:
        asyncio.create_task(fcn(*args, **kwargs))
        await asyncio.sleep(period)

    return wrapper

  return scheduler

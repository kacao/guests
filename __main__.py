import asyncio
from server import main

try:
    asyncio.run(main())
except KeyboardInterrupt as e:
    pass

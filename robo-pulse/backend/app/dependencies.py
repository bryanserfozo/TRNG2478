"""
Day 4 - shared FastAPI Dependencies

In our application (or many other apps) one piece of code might be dependent on the functions of another piece
In our case, we are dependent on having an AsyncSessionLocal object to perform any of our DB operations
We need a way to provide this dependency in a reliable way to each FastAPI function

Enter Dependency Injection.
Design pattern where a piece of code declares what it is dependent on and the framework holds the responsibility for
creating and managing that dependency
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

"""
What is yield and why are we using it? Yield basically can be considered like a try-with-resources statement from Java

When a method requires this, it will call get_db which will return the session, then the operations get executed and then after the other function is 
finished, it returns here and completes this method, which just means it closes the session
"""
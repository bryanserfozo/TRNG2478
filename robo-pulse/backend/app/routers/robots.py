"""
Day 4 - Robot Endpoints

At this point we have everything we need to expose our application to the internet, we just need to define how the endpoints are
created.

We'll need to give the endpoints a URL (everything here should be under /robots) and then define any additional
parameters as needed
"""

from fastapi import APIRouter, Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.models.enums import RobotStatus
from app.models.robot import Robot
from app.schemas.robot import RobotRead


# Every request comes under /robots and has to do with robots
router = APIRouter(prefix="/robots", tags=["robots"])

# This decorator says this goes to "/robots" with nothing else and returns a list of RobotRead objects
@router.get("", response_model = list[RobotRead])
async def list_robots(db: AsyncSession = Depends(get_db)):
    # We need to be able to interact with the DB, so we need our session object to execute those statement
    # We are DEPENDENT on the session object

    # Create our statement for the DB
    statement = select(Robot).where(Robot.status != RobotStatus.OFFLINE)

    result = await db.execute(statement)

    return list(result.scalars().all())
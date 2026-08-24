"""
Day 4 - Robot Endpoints

At this point we have everything we need to expose our application to the internet, we just need to define how the endpoints are
created.

We'll need to give the endpoints a URL (everything here should be under /robots) and then define any additional
parameters as needed

Common pattern for REST endpoints:
GET /robots -> Gets all robots
GET /robots/1 -> Get robot with id = 1
POST /robots -> Creates a robot resources
PUT /robots/2 -> Updates robot with id = 2
DELETE /robots/3 -> delete the robot with id = 3

Query parameter (THIS IS GETTING REPLACED WITH THE NEW HTTP METHOD):
GET /robots?max_battery=20 -> Get all robots WHERE max batter is 20
"""

from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.models.enums import RobotStatus
from app.models.robot import Robot
from app.schemas.robot import RobotCreate, RobotRead


# Every request comes under /robots and has to do with robots
router = APIRouter(prefix="/robots", tags=["robots"])

# This decorator says this goes to "/robots" with nothing else and returns a list of RobotRead objects
@router.get("", response_model = list[RobotRead])
async def list_robots(
    max_battery: Decimal | None = Query(
        # This is a query param, used for filtering all of our results
        default = None, # This makes it optional
        ge=0,
        le=100,
        description="Only return robots strictly below this battery percentage"
    ),
    db: AsyncSession = Depends(get_db)):
    # We need to be able to interact with the DB, so we need our session object to execute those statement
    # We are DEPENDENT on the session object
    # TODO add in optional query parameter for filtering based on power level (Business Question #1)

    # Create our statement for the DB
    statement = select(Robot).where(Robot.status != RobotStatus.OFFLINE)

    # Check for max_battery query param
    if max_battery is not None:
        statement = statement.where(Robot.battery_level < max_battery)
    statement = statement.order_by(Robot.id)

    result = await db.execute(statement)

    return list(result.scalars().all())


# Get a specific robot by its id
# GET /robots/{robot_id} -> robot_id is known as a PATH PARAMETER
@router.get("/{robot_id}", response_model=RobotRead)
async def get_robot(robot_id: int, db: AsyncSession = Depends(get_db)):
    robot = await db.get(Robot, robot_id)

    # TODO Code defensively
    if robot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Robot {robot_id} not found"
        )

    return robot

# Let's create a Robot
# POST requests are used for creating new resources or altering state
@router.post("", response_model=RobotRead, status_code=status.HTTP_201_CREATED)
async def create_robot(payload: RobotCreate, db: AsyncSession = Depends(get_db)):
    # We receive the payload as a RobotCreate object
    # We need it as a Robot object to save with the ORM
    robot = Robot(**payload.model_dump())
    # Dumps the model into the Robot constructor
    db.add(robot)
    await db.commit()
    await db.refresh(robot)
    return robot
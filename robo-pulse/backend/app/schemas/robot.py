"""
Day 4 - Pydantic v2 Schema for the robot resource

What is Pydantic? A validation framework used widely in python projects and other framework for validating
the "shape" of data, especially in transit

Why is this separate from the models? The Models leverage ORM level definitions to define how they interact with
a database, we don't need to have all of that, this is going to be just defining the shape that gets passed in and out
of the application
"""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import RobotStatus


class RobotBase(BaseModel):
    # String fields withg specific lengths
    serial_number: str = Field(min_length=1, max_length=50)
    model: str = Field(min_length=1, max_length=100)
    # Decimal values with bounds
    battery_level: Decimal = Field(ge=0, le=100)
    facility_id: int
    # Robot Status field that defaults to IDLE
    status: RobotStatus = RobotStatus.IDLE


# Two additional classes that build upon this starter class
class RobotCreate(RobotBase):
    """Shape of the Request Body for POST /robots"""

class RobotRead(RobotBase):
    """Shape of a Robot in any API Response"""

    id: int

    model_config = ConfigDict(from_attributes=True)
"""
Day 4 Challenge, creating DiscrepancyRead Class for input/output validation
"""

from pydantic import BaseModel, ConfigDict


class DiscrepancyRead(BaseModel):
    mission_id: int
    title: str
    robot_facility_id: int
    operator_facility_id: int

    # Since we expect this coming back from our ORM
    model_config = ConfigDict(from_attributes=True)
    # Allows us to create a DiscrepancyRead Object from an object with the exact same attributes


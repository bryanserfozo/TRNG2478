"""
Day 4 Challenge - Creating discrepancy router
"""

from fastapi import APIRouter, Depends, Query

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.mission import DiscrepancyRead
from app.dependencies import get_db
from app.models.mission import Mission
from app.models.operator import Operator
from app.models.robot import Robot
from app.models.enums import MissionPriority


router = APIRouter(prefix = "/missions", tags = ["missions"])

# Construct our method for Business Question #2
# Recall we need to inject our DB dependency

@router.get("/discrepancies", response_model=list[DiscrepancyRead])
async def list_colocation_discrepancies(
    priority: MissionPriority | None = Query(
        default=None,
        description="Only return discrepancies for missions of this priority"
    ),
    db: AsyncSession = Depends(get_db)
):
    """Returns the answer to business question #2, showing location discrepancies between robots and operators"""
    statement = (
            select(
                Mission.id.label("mission_id"),
                Mission.title,
                Robot.facility_id.label("robot_facility_id"),
                Operator.facility_id.label("operator_facility_id")
            )
            .join(Robot, Robot.id == Mission.robot_id)
            .join(Operator, Operator.id == Mission.operator_id)
            .where(Robot.facility_id != Operator.facility_id)
        )

    # Use the query parameter
    if priority is not None:
        statement = statement.where(Mission.priority == priority)

    statement = statement.order_by(Mission.id)

    result = await db.execute(statement)
    return [dict(row) for row in result.mappings().all()]
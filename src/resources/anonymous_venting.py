from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from src.db.functions.anonymous_venting import add_vent, get_vents

anonymous_venting_router = APIRouter()


class Vent(BaseModel):
    id: str
    text: str


@anonymous_venting_router.post("/add")
def add_venting(vent: Vent):
    v_id = add_vent(vent.id, vent.text)

    return {"data": "vent added successfully",
            "vent_id": v_id}


@anonymous_venting_router.get("/")
def get_veting():
    return {"data": get_vents()}

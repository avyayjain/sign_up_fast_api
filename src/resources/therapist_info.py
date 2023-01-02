from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.db.functions.therapist_info import get_therapist_info, therapist_info

therepist_info_router = APIRouter()


class Therapist(BaseModel):
    t_name: str
    t_city: str
    t_phone: int
    t_address: str
    t_dis: str
    t_services: str
    t_picture: str
    t_spec: str


@therepist_info_router.get("/")
def therapist_data():
    return {"data": get_therapist_info()}


@therepist_info_router.post("/add")
def therapist_data_post(the: Therapist):
    v_id = therapist_info(the.t_name, the.t_city, the.t_phone, the.t_address, the.t_dis, the.t_services,
                          the.t_picture, the.t_spec)

    return {"data": "vent added successfully",
            "vent_id": v_id}

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from src.db.functions.therapist_info import get_therapist_info

therepist_info_router = APIRouter()


@therepist_info_router.get("/")
def therapist_data():
    return {"data": get_therapist_info()}

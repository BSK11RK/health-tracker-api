# APIの入力定義
from pydantic import BaseModel, field_validator


class HealthCreate(BaseModel):
    height: float
    weight: float


    @field_validator("height")
    def height_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("身長は0より大きい値にしてください")
        if v > 300:
            raise ValueError("身長が不正です")
        return v


    @field_validator("weight")
    def weight_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("体重は0より大きい値にしてください")
        if v > 500:
            raise ValueError("体重が不正です")
        return v
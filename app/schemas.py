# APIの入力定義
from pydantic import BaseModel, field_validator


class UserCreate(BaseModel):
    username: str
    password: str
    
    @field_validator("password")
    def password_length(cls, v):
        if len(v) < 6:
            raise ValueError("パスワードは6文字以上にしてください")
        if len(v) > 72:
            raise ValueError("パスワードは72文字以内にしてください")
        return v


class UserLogin(BaseModel):
    username: str
    password: str
    
    @field_validator("password")
    def password_length(cls, v):
        if len(v) > 72:
            raise ValueError("パスワードは72文字以内にしてください")
        return v
    

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
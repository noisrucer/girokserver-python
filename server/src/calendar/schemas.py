from typing import Union, List, Dict
from pydantic import BaseModel
    

class CategoryOut(BaseModel):
    resp: Dict[str, dict]
    
    
class CategoryCreateIn(BaseModel):
    color: str
    names: List[str]
    

class CategoryCreateOut(BaseModel):
    task_category_id: int
    class Config:
        orm_mode = True
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
        
        
class CategoryDeleteIn(BaseModel):
    cats: List[str]
    

class CategoryRenameIn(BaseModel):
    cats: List[str]
    new_name: str
    
class CategoryMoveIn(BaseModel):
    cats: List[str]
    new_parent_cats: List[str]
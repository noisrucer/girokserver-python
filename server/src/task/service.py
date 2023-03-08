from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.orm import Session

import server.src.task.models as models

def create_task(db: Session, task_data):
    new_task = models.Task(**task_data)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task



from sqlalchemy.orm import Session


class EventRepository:
    def __init__(self, session: Session):
        self.session = session

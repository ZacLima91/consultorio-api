from sqlalchemy import select
from sqlalchemy.orm import Session
from src.schemas.schemas import UserBase
from src.infra.sqlalchemy.models import models


class RepositoryUser():

    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user: UserBase):
        db_user = models.User(username=user.username, email=user.email,
                              cpf=user.cpf, password=user.password, laudos=user.laudos)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user
    
    def get_all_user(self):
        return self.session.query(models.User).all()
    
    def delete_user(self, id: int):
        self.session.query(models.User).filter(models.User.id == id).delete()
        self.session.commit()

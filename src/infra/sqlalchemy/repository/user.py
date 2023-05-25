from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.schemas.schemas import UserBase, UserList
from src.infra.sqlalchemy.models import models


class RepositoryUser():

    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user: UserBase):
        try:
            db_user = models.User(username=user.username, email=user.email,
                                  cpf=user.cpf, password=user.password, laudos=user.laudos, role=user.role)
            self.session.add(db_user)
            self.session.commit()
            self.session.refresh(db_user)
            return db_user
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def get_all_user(self):
        try:
            db_user = self.session.query(models.User).all()
            return db_user
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def get_by_cpf(self, cpf):
        try:
            query = select(models.User).where(models.User.cpf == cpf)
            return self.session.execute(query).scalars().first()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def delete_user(self, id: int):
        try:
            self.session.query(models.User).filter(
                models.User.id == id).delete()
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

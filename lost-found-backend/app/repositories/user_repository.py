from sqlalchemy.orm import Session

from models.user import User


class UserRepository:

    @staticmethod
    def create_user(
        db: Session,
        user_data: dict
    ):
        user = User(**user_data)

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def get_user_by_id(
        db: Session,
        user_id: int
    ):
        return db.query(User).filter(
            User.user_id == user_id
        ).first()

    @staticmethod
    def get_user_by_email(
        db: Session,
        email: str
    ):
        return db.query(User).filter(
            User.email == email
        ).first()

    @staticmethod
    def get_user_for_login(
        db: Session,
        email: str
    ):
        return db.query(User).filter(
            User.email == email
        ).first()

    @staticmethod
    def get_user_by_username(
        db: Session,
        username: str
    ):
        return db.query(User).filter(
            User.username == username
        ).first()

    @staticmethod
    def get_all_users(db: Session):
        return db.query(User).all()

    @staticmethod
    def update_user(
        db: Session,
        user: User,
        user_data: dict
    ):
        for key, value in user_data.items():
            if value is not None:
                setattr(user, key, value)

        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def delete_user(
        db: Session,
        user: User
    ):
        db.delete(user)
        db.commit()

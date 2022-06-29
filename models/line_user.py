import logging
from typing import List

import sqlalchemy.exc
from sqlalchemy import Column
from sqlalchemy import Integer, String

from models.database import Base, create_session

logger = logging.getLogger(__name__)


class LineUser(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    line_user_id = Column(String(100), unique=True)
    line_notify_access_token = Column(String(100))

    def __str__(self):
        return f"<LineUser (id={self.id}, " \
               f"line_user_id={self.line_user_id}," \
               f"line_notify_access_token={self.line_notify_access_token})>"

    # def __repr__(self):
    #     return f"<LineUser (id={self.id}, " \
    #            f"line_user_id={self.line_user_id}," \
    #            f"line_notify_access_token={self.line_notify_access_token})>"


def get_notify_tokens_by_line_ids(id_list: List[str]) -> List[str]:
    session = create_session()
    users: List[LineUser] = session.query(LineUser)\
        .filter(LineUser.line_user_id.in_(id_list))\
        .all()

    # users2 = [local_session.query(LineUser).filter(LineUser.line_user_id == user_id).first()
    #           for user_id in id_list]

    return [user.line_notify_access_token for user in users]


def get_user_by_id(line_id: str) -> LineUser:
    session = create_session()
    user: LineUser = session.query(LineUser)\
        .filter(LineUser.line_user_id == line_id)\
        .first()

    return user


def check_notify_connect(line_id: str) -> bool:
    user = get_user_by_id(line_id)
    if user is None:
        return False
    elif user.line_notify_access_token is None:
        return False
    return True


def insert_line_user(line_id: str, access_token: str):
    session = create_session()
    user = LineUser(line_user_id=line_id,
                    line_notify_access_token=access_token)
    session.add(user)
    try:
        session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        # TODO: handle update line_notify_access_token
        # session.query(LineUser) \
        #     .filter(LineUser.line_user_id == line_id) \
        #     .update({"line_notify_access_token": access_token})
        # session.commit()

        # TODO: fix logger
        print(f"User already exits. {e}")
        pass

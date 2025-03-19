from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from config import DATABASE_URL

# Baseクラスの作成 (マッピング定義で使用)
Base = declarative_base()

# サンプル用のテーブル定義 (Model)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)

# Engine と Session のセットアップ
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """テーブル作成(まだ存在しなければ)"""
    Base.metadata.create_all(bind=engine)

def create_user(session: Session, name: str, email: str):
    """ユーザデータを作成 (CREATE)"""
    new_user = User(name=name, email=email)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

def get_user_by_name(session: Session, name: str):
    """ユーザを名前で検索 (READ)"""
    return session.query(User).filter(User.name == name).first()

def update_user_email(session: Session, user_id: int, new_email: str):
    """ユーザのメールアドレスを更新 (UPDATE)"""
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.email = new_email
        session.commit()
        session.refresh(user)
    return user

def delete_user(session: Session, user_id: int):
    """ユーザを削除 (DELETE)"""
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        session.delete(user)
        session.commit()
    return user

if __name__ == "__main__":
    # DB初期化 (テーブルが無ければ作成)
    init_db()

    # Session 作成
    db_session = SessionLocal()

    try:
        # --- CREATE ---
        created_user = create_user(db_session, name="Taro", email="taro@example.com")
        print("Created user:", created_user.name, created_user.email)

        # --- READ ---
        fetched_user = get_user_by_name(db_session, "Taro")
        if fetched_user:
            print("Fetched user:", fetched_user.id, fetched_user.name, fetched_user.email)
        else:
            print("User not found.")

        # --- UPDATE ---
        updated_user = update_user_email(db_session, fetched_user.id, "taro_new@example.com")
        print("Updated user email:", updated_user.email)

        # --- DELETE ---
        deleted_user = delete_user(db_session, fetched_user.id)
        if deleted_user:
            print("Deleted user:", deleted_user.name)
        else:
            print("No user found to delete.")

    finally:
        db_session.close()

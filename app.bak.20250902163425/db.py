from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///travel.db"
engine = create_engine(DATABASE_URL, echo=False)

def create_db_and_tables() -> None:
    # 根據 models 定義先建表
    SQLModel.metadata.create_all(engine)

    # 簡易遷移：補上缺的欄位（SQLite）
    with engine.begin() as conn:
        # Trip.user_id
        cols_trip = [row[1] for row in conn.exec_driver_sql("PRAGMA table_info(trip)")]
        if "user_id" not in cols_trip:
            conn.exec_driver_sql("ALTER TABLE trip ADD COLUMN user_id INTEGER")
        # ItineraryItem.order_index
        cols_item = [row[1] for row in conn.exec_driver_sql("PRAGMA table_info(itineraryitem)")]
        if "order_index" not in cols_item:
            conn.exec_driver_sql("ALTER TABLE itineraryitem ADD COLUMN order_index INTEGER")
        # Trip.order_index
        if "order_index" not in cols_trip:
            conn.exec_driver_sql("ALTER TABLE trip ADD COLUMN order_index INTEGER")

def get_session():
    with Session(engine) as session:
        yield session

import aiosqlite
from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class User:
    id: int
    stock_value: float
    trend: float
    effective_trend: float
    balance: float

    @staticmethod
    def default(user_id: int):
        return User(id=user_id, stock_value=1000, trend=0, effective_trend=0, balance=1000)
    
class Database:
    def __init__(self):
        self.db_path = "./data.db"

    async def create_tables(self):
        async with aiosqlite.connect(self.db_path) as conn:
            await conn.execute(
                """
            CREATE TABLE IF NOT EXISTS users (
            id BIGINT PRIMARY KEY,
            stock_value FLOAT NOT NULL,
            trend FLOAT NOT NULL,
            effective_trend FLOAT NOT NULL,
            balance FLOAT NOT NULL
            );
            """
            )

            await conn.execute(
                """
            CREATE TABLE IF NOT EXISTS stocks (
            user_id BIGINT NOT NULL,
            stock_id BIGINT NOT NULL,
            amount BIGINT NOT NULL)"""
            )
            await conn.commit()
            
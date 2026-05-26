import sqlite3
import os

# 데이터베이스 파일 경로
DB_FILE = "users.db"

def init_db():
    """
    데이터베이스와 테이블을 초기화하고 샘플 데이터를 추가합니다.
    """
    # 애플리케이션 시작 시 이전 DB 파일이 있다면 삭제
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 사용자 테이블 생성
    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        credit_card_number TEXT NOT NULL
    )
    """)
    
    # 샘플 데이터 삽입
    cursor.execute("INSERT INTO users (username, email, credit_card_number) VALUES (?, ?, ?)",
                   ('hong_gildong', 'hong.gildong@example.com', '0000-0000-0000-0000'))
    cursor.execute("INSERT INTO users (username, email, credit_card_number) VALUES (?, ?, ?)",
                   ('lee_sunsin', 'lee.sunsin@example.com', '9999-9999-9999-9999'))
    
    conn.commit()
    conn.close()
    print(f"데이터베이스 '{DB_FILE}'가 초기화되었습니다.")

def get_user_by_username_vulnerable(username: str):
    """
    SQL 인젝션에 취약한 사용자 검색 함수.
    사용자 입력을 그대로 쿼리 문자열에 삽입합니다.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 경고: SQL 인젝션 취약점!
    # f-string을 사용하여 쿼리를 동적으로 생성하므로 공격에 노출됩니다.
    query = f"SELECT username, email, credit_card_number FROM users WHERE username = '{username}'"
    print(f"실행되는 쿼리: {query}")
    
    cursor.execute(query)
    user_data = cursor.fetchone()
    
    conn.close()
    
    if user_data:
        return {"username": user_data[0], "email": user_data[1], "credit_card_number": user_data[2]}
    return None

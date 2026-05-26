from fastapi import FastAPI, HTTPException
from pydantic_settings import BaseSettings, SettingsConfigDict
import hashlib

from database import init_db, get_user_by_username_vulnerable

# --- 설정 관리 ---
# .env 파일로부터 환경 변수를 로드하는 설정 클래스
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    user_name: str = "demo_user"
    rrn_plaintext: str = "TEST-RRN-DO-NOT-USE"  # env: RRN_PLAINTEXT
    credit_card_number: str = "0000-0000-0000-0000"
    user_email: str = "demo@example.com"

settings = Settings()
app = FastAPI()

# --- 애플리케이션 시작 시 데이터베이스 초기화 ---
@app.on_event("startup")
def on_startup():
    """
    애플리케이션이 시작될 때 데이터베이스를 설정합니다.
    """
    init_db()

# --- API 엔드포인트 ---

@app.get("/user/profile/from-env")
def get_user_profile_from_env():
    """
    환경 변수에서 사용자 프로필을 안전하게 로드합니다.
    하드코딩을 방지한 예시입니다.
    """
    ssn_protected = hashlib.sha256(settings.rrn_plaintext.encode("utf-8")).hexdigest()
    return {
        "username": settings.user_name,
        "ssn_protected": ssn_protected,
        "credit_card_number": settings.credit_card_number,
        "email": settings.user_email,
        "protection_note": "ssn_protected는 SHA-256 해시(보호됨), credit_card_number는 평문(취약 예시)"
    }

@app.get("/users/{username}")
def get_user_vulnerable(username: str):
    """
    SQL 인젝션에 취약한 사용자 검색 엔드포인트.
    """
    user = get_user_by_username_vulnerable(username)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/")
def read_root():
    return {"message": "하드코딩은 방어했지만 SQL 인젝션에 취약한 애플리케이션입니다."}

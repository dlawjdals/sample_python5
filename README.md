# Samplepython5

FastAPI 데모 프로젝트입니다.

## 의도된 보안 상태

- 하드코딩 방어: 리포에는 `.env`를 포함하지 않습니다. (대신 `.env.example` 제공)
- 개인정보 일부 보호: `RRN_PLAINTEXT`는 응답에서 SHA-256 해시로만 노출됩니다.
- 취약점 데모: `/users/{username}`는 문자열 결합 쿼리로 SQL Injection에 취약합니다.

## 실행(Windows)

```powershell
py -3.11 -m pip install -r requirements.txt
py -3.11 -m uvicorn main:app --port 8000
```

## 환경변수

- 로컬에서 필요하면 `.env.example`을 `.env`로 복사해서 값을 바꿀 수 있습니다.
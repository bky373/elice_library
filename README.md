# 📚 도서관 책 대여 서비스

## 프로젝트 소개

도서관의 핵심적인 기능들( 회원가입, 도서 대여, 반납, 검색, 조회 등 )을 제공하는 서비스입니다.

집에서도 [도서관을 이용해보세요](http://elice-kdt-ai-track-vm-racer-37.koreacentral.cloudapp.azure.com/books/) !

## 주요 사용 기술

- **Flask**
- SQLAlchemy + Migrate
- PyMySQL + MySQL
- Marshmallow
- Flask-RESTX
- HTML + Flask Jinja2 + Bootstrap
- JQuery 

## 프로젝트 실행

### 프로젝트 설치

```bash
git clone https://kdt-gitlab.elice.io/001_part2_project-library/team1/elice-library.git
```

 ### 환경 구축

```bash
python -m venv venv // 가상 환경 폴더 생성

source venv/[Scripts|bin]/activate // 가상 환경 접속

pip install -r requirements.txt // 필요한 패키지 설치
```

### 데이버베이스 설정

```python
# elice_library/utils/config.py
# 아래와 같이 설정
# 혹은 .env 파일 이용

SECRET_KEY = [사용자 고유 비밀키 지정]
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{pw}@{host}:{port}/{db}?	
                            charset=utf8'.format(
                                user = [사용자 MySQL 계정],
                                pw = [사용자 MySQL 비밀번호],
                                host = [사용자 host],
                                port = [사용자 port],
                                db = [사용자 db 이름] 
                            )

SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### 데이터 베이스 초기화

```bash
flask db init
flask db migrate
flask db update
```

### 초기 데이터 세팅

```python
python load_data.py
```

### 서버 실행

```python
python run.py
```

## 기능 구현

### 회원가입

- `아이디(이메일), 비밀번호, 이름`은 필수 입력 사항입니다.
- 아이디는 `이메일 형식`이어야 합니다.
- 이름은 `한글, 영문`으로만 입력해야 합니다.
- 비밀번호와 비밀번호 확인의 `값이 일치`해야 합니다.
- 비밀번호는 `영문, 숫자, 특수문자 3종류` 이상을 조합하여 `최소 8자리 이상`의 길이로 구성해야 합니다.

### 로그인

- `아이디(이메일)와 비밀번호`는 필수 입력 사항입니다.
- 아이디는 `이메일 형식`이어야 합니다.
- 로그인한 유저는 session으로 관리합니다.

### 로그아웃

- 현재 로그인한 사용자를 로그아웃합니다.
- 로그아웃한 유저를 현재 session에서 제거합니다.

### 메인

- 현재 DB 상에 존재하는 모든 책 정보를 가져옵니다.
- 현재 DB 상에 존재하는 남은 책의 수를 표기합니다.
- 책 이름을 클릭 시 책 소개 페이지로 이동합니다.
- 책의 평점은 현재 DB 상에 담겨있는 모든 평점의 평균으로 표시합니다.
  (숫자 한자리수로 반올림하여 표기합니다.)

- 페이지네이션 기능을 추가합니다. (한 페이지 당 8권의 책만을 표기합니다.)

### 책 소개

- 메인 페이지의 책 이름을 클릭하여 접근합니다.
- 책에 대한 소개를 출력합니다.
- 가장 최신의 댓글이 보이도록 sorting하여 보여줍니다.
- 댓글을 작성함으로써 책에 대한 평가 점수를 기입합니다.
- 댓글 내용과 평가 점수는 모두 “필수 입력” 사항입니다.

### 대여하기

- 메인 페이지의 대여하기 버튼을 클릭하여 실행합니다.
- 현재 DB 상에 책이 존재하지 않는 경우, 대여되지 않습니다.
- 현재 DB 상에 책에 존재하는 경우, 책을 대여하고 책의 권수를 -1 합니다.
- 현재 DB 상에 책이 존재하지 않는 경우, 사용자에게 대여가 불가능하다는 메세지를 반환합니다.
- 유저가 이미 이 책을 대여했을 경우, 이에 대한 안내 메세지를 반환합니다.

### 반환하기

- 로그인한 유저가 대여한 책을 모두 보여줍니다.
- 반납하기 버튼을 통해 책을 반납합니다.
- 이때, 책을 반납한 후 DB 상에 책의 권수를 +1 합니다.

### 대여 기록

- 로그인한 유저가 대여 후 반납했던 책에 대한 모든 사항을 출력합니다.

​    

## 전체 프로젝트 진행 일정

### 1주차 (2/23 ~ 2/27)

- 필수 및 선택 기능 구현 (앞 페이지의 주요 서비스들 중 ”노란색”으로 표시된 기능)
- 간단한 UI/UX 작업



### 2주차 (3/2 ~ 3/8)

- 모듈화 / 관심사 분리 리팩토링

- 부가 기능 구현 (뒷 페이지 참고)

- UI/UX 수정 및 보완


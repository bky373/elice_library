# 📚 도서관 책 대여 서비스

### 프로젝트 소개

도서관의 핵심적인 기능들을 제공하는 서비스입니다.  

>  `회원가입, 도서 대여, 반납, 검색, 조회 기능` 등 제공) <br>
> 우측 페이지에 접속하여 [도서관](http://elice-kdt-ai-track-vm-racer-37.koreacentral.cloudapp.azure.com/books/)을 이용할 수 있습니다 😙

## 주요 사용 기술

- **Flask**
- SQLAlchemy + Migrate
- PyMySQL + MySQL
- Marshmallow
- Flask-RESTX
- HTML + Flask Jinja2 + Bootstrap
- JQuery 
- Azure VM (OS: Ubuntu LTS 18.04)
- Black

<a name="directory-structure"></a>

## 프로젝트 디렉토리 구조

기능 대신 계층 위주로 구조를 나누었습니다.

![image](https://user-images.githubusercontent.com/49539592/110431708-80203480-80f1-11eb-8594-4412df905eee.png)

### 세부 구조

```
// 각 패키지별 __init__.py는 생략

elice_library
 ├─ static : css, js 파일들
 ├─ templates : html 파일들
 ├─ database  
 │    └─ config.py : db 인스턴스	
 ├─ domain
 │    ├─ models
 │    │    ├─ user.py : User 모델 정의
 │	  │    ├─ book.py : Book 모델 정의	  
 │    │    └─ ... : [그 외 model].py
 │    └─ schemas : 모델과 관련된 스키마들
 │         ├─ user_schema.py : User 스키마 정의	  
 │         └─ ... : [그 외 schema].py
 ├─ services
 │	  ├─ user_service.py : User 모델과 관련된 로직 수행
 │	  ├─ book_service.py : Book 모델과 관련된 로직 수행
 │	  └─ ... : [그 외 service].py
 ├─ controllers
 │	  ├─ user_controller.py : User과 관련된 HTTP request 핸들링
 │	  ├─ book_controller.py : Book과 관련된 HTTP request 핸들링
 │	  └─ ... : [그 외 controller].py
 ├─ utils
 │	  ├─ config : Flask 앱 config
 │	  └─ errors.py : Book 모델과 관련된 로직 수행
 ├─ __init__.py : create_app 함수 정의
 └─ routes.py : 각 namespace의 api routes 연결
```

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
// elice_library/utils/config.py
// 아래와 같이 설정
// 혹은 .env 파일 이용

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
flask db init  // migrations 디렉토리 생성
flask db migrate  // 데이터베이스 모델 테이블 생성 및 변경
flask db update  //  데이터베이스 갱신
```

### 초기 데이터 세팅

```python
python load_data.py
```

### 서버 실행

```python
python run.py
```

## 전체 프로젝트 진행 일정

### 1주차 (2/23 ~ 2/27)

- 핵심 기능 구현 (아래 <a href="https://kdt-gitlab.elice.io/001_part2_project-library/team1/elice-library#features">기능 소개</a> 참고)

  > 회원가입
  >
  > 로그인 / 로그아웃
  >
  > 대여하기
  >
  > 반납하기
  >
  > 대여 기록 
  >
  > 반납 기록
  >
  > 책 목록 페이지
  >
  > 책 소개 페이지
  >
  > 댓글 작성

- 간단한 UI/UX 작업 

### 2주차 (3/2 ~ 3/8)

- **모듈화** / **관심사 분리** 리팩토링 (위의 <a href="https://kdt-gitlab.elice.io/001_part2_project-library/team1/elice-library#directory-structure">프로젝트 디렉토리 구조</a> 참고)

- 부가 기능 구현 

  > 댓글 수정 및 삭제
  >
  > 도서 검색
  >
  > 도서 평점 차트
  >
  > 출간일, 평점, 대여횟수, 댓글 개수 순으로 정렬된 책 목록 확인    
  >
  > 책 추천하기 및 찜하기
  >
  > 개인 맞춤 정보 확인 (내가 찜한 도서, 추천한 도서, 댓글 남긴 도서 목록 확인)
  >
  > 비밀번호 변경
  >
  > 회원 탈퇴

- UI/UX 수정 및 보완

<a name="features"></a>

## 기능 소개

### 회원가입

- `아이디(이메일), 비밀번호, 이름`은 필수 입력 사항입니다.
- 아이디는 `이메일 형식`이어야 합니다.
- 이름은 `한글, 영문`으로만 입력해야 합니다.
- 비밀번호와 비밀번호 확인의 `값이 일치`해야 합니다.
- 비밀번호는 `영문, 숫자, 특수문자 3종류` 이상을 조합하여 `최소 8자리 이상`의 길이로 구성해야 합니다.

### 로그인

- `아이디(이메일)와 비밀번호`는 필수 입력 사항입니다.
- 아이디는 `이메일 형식`이어야 합니다.
- 로그인한 유저는 `session`으로 관리합니다.

### 로그아웃

- 현재 로그인한 사용자를 로그아웃합니다.
- 로그아웃한 유저를 현재 session에서 제거합니다.

### 메인

- 현재 DB 상에 존재하는 `모든 책 정보`를 가져옵니다.
- 현재 DB 상에 존재하는 `남은 책의 수`를 표기합니다.
- 책 이름을 클릭 시 `책 소개 페이지`로 이동합니다.
- `책의 평점`은 현재 DB 상에 담겨있는 모든 평점의 평균으로 표시합니다.
  (숫자 한자리수로 반올림하여 표기합니다.)
- `페이지네이션` 기능을 넣어 한 페이지 당 8권의 책만을 표기합니다.

### 책 소개 / 댓글 남기기

- 메인 페이지의 `책 이름`을 클릭하여 접근합니다.
- `책에 대한 소개`를 출력합니다.
- 가장 `최신의 댓글`이 보이도록 `sorting`하여 보여줍니다.
- 댓글을 작성함으로써 책에 대한 `평가 점수`를 기입합니다.
- `댓글 내용`과 `평가 점수`는 모두 “필수 입력” 사항입니다.
- 동일한 사용자는 동일 책에 한 번만 평점을 매길 수 있습니다.  
- 책 소개 페이지에서도 `대여하기, 찜하기, 추천하기` 기능을 사용할 수 있습니다.

### 대여하기

- 메인 페이지의 `대여하기 버튼`을 클릭하여 실행합니다.
- 현재 DB 상에 책이 존재하지 않는 경우, `대여되지 않습니다`.
- 현재 DB 상에 책에 존재하는 경우, 책을 대여하고 `책의 권수를 -1 합니다`.
- 현재 DB 상에 책이 존재하지 않는 경우, 사용자에게 대여가 `불가능하다는 메세지를 반환`합니다.
- 유저가 이미 이 책을 대여했을 경우, 이에 대한 `안내 메세지를 반환`합니다.

### 반납하기

- `반납하기 버튼`을 통해 책을 반납합니다.
- 책을 반납한 후 DB 상에 `책의 권수를 +1 합니다.`

### 대여 / 반납 기록

- 로그인한 유저가 `대여한 책을 모두` 보여줍니다.
- 로그인한 유저가 대여 후 `반납했던 책에 대한 모든 기록`을 보여줍니다.

### 회원정보

- 비밀번호를 변경합니다. 현재 비밀번호와 다른 새로운 비밀번호를 입력해야 합니다.
- 유효성 검사는 회원가입시의 검사와 동일합니다.
- 비밀번호를 입력 후 회원탈퇴를 합니다. (책이 모두 반납되어 있어야 합니다.)

### 도서 검색

- 검색어를 입력했을 때 검색어에 해당하는 이름을 가진 책 목록을 불러옵니다.


# 📚 도서관 책 대여 서비스

### Contents

> 1. [프로젝트 소개](#프로젝트-소개)
> 2. [주요 사용 기술](#주요-사용-기술)
> 3. [프로젝트 디렉토리 구조](#프로젝트-디렉토리-구조)
> 4. [프로젝트 실행](#프로젝트-실행)
> 5. [전체 프로젝트 일정](#전체-프로젝트-일정)
> 6. [기능 상세 소개](#기능-상세-소개)
> 7. [어려웠던 점과 해결 방법](#어려웠던-점과-해결-방법)
> 8. [느낀 점](#느낀-점)

## 프로젝트 소개

도서관의 핵심적인 기능과 부가적인 기능을 제공하는 웹 서비스입니다.  

>  `회원가입, 도서 대여, 반납, 검색, 조회, 댓글 작성 기능` 등 제공 <br>
>  우측 링크에 접속하여 [도서관](http://elice-kdt-ai-track-vm-racer-37.koreacentral.cloudapp.azure.com/books/)을 이용할 수 있습니다 😙

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

기능 대신 **계층 위주**로 구조를 나누었습니다.

![image](https://user-images.githubusercontent.com/49539592/110431708-80203480-80f1-11eb-8594-4412df905eee.png)

### 세부 구조

```
// 각 패키지별 __init__.py는 생략

elice_library
 ├─ static: css, js, images 파일 관리
 ├─ templates: html 파일 관리
 ├─ database  
 │    └─ config.py: db 인스턴스
 ├─ domain
 │    ├─ models
 │    │    ├─ user.py: User 모델 정의
 │    │    ├─ book.py: Book 모델 정의
 │    │    └─ [...].py: 그 외 모델 정의
 │    └─ schemas
 │         ├─ user_schema.py: User 스키마 정의	  
 │         └─ [...].py: 그 외 스키마 정의
 ├─ services
 │	  ├─ user_service.py: User 모델과 관련된 로직 수행
 │	  ├─ book_service.py: Book 모델과 관련된 로직 수행
 │	  └─ [...].py: 그 외 service
 ├─ controllers
 │	  ├─ user_controller.py : User과 관련된 HTTP request 핸들링
 │	  ├─ book_controller.py : Book과 관련된 HTTP request 핸들링
 │	  └─ [...].py: 그 외 controller
 ├─ utils
 │	  ├─ config : 앱 config
 │	  └─ errors.py : error 클래스 정의
 ├─ __init__.py : create_app 함수 정의
 └─ routes.py : Namespace별 api routes 연결
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

### 데이터베이스 초기화

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

## 전체 프로젝트 일정

### 1주차 (2/23 ~ 2/27)

- **핵심 기능 구현** (아래 [기능 상세 소개](https://github.com/bky373/elice_library#기능-상세-소개) 참고)

  > 회원가입 <br>
  > 로그인 / 로그아웃 <br>
  > 대여하기 <br>
  > 반납하기 <br>
  > 대여 기록 <br>
  > 반납 기록 <br>
  > 책 목록 페이지 <br>
  > 책 소개 페이지 <br>
  > 댓글 작성

- 간단한 UI/UX 작업 

### 2주차 (3/2 ~ 3/8)

- **모듈화** / **관심사 분리 리팩토링** (위의 [프로젝트 디렉토리 구조](https://github.com/bky373/elice_library#프로젝트-디렉토리-구조) 참고)

- **부가 기능 구현** 

  > 댓글 수정 및 삭제 <br>
  > 도서 검색 <br>
  > 도서 평점 차트 <br>
  > 출간일, 평점, 대여횟수, 댓글 개수 순으로 정렬된 책 목록 확인 <br>
  > 책 추천하기 및 찜하기 <br>
  > 개인 맞춤 정보 확인 (내가 찜한 도서, 추천한 도서, 댓글 남긴 도서 목록 확인) <br>
  > 비밀번호 변경 <br>
  > 회원 탈퇴 <br>

- UI/UX 수정 및 보완

<a name="features"></a>

## 기능 상세 소개

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

---

## 어려웠던 점과 해결 방법  

### 1. 회원가입 / 로그인 validation

- 이름이 `한글 또는 영어`로만 구성됐는지, 비밀번호가 `영문, 숫자, 특수문자 3종류 이상을 조합하여 최소 8자리 이상의 길이`로 구성됐는지 확인하는 유효성 검사가 조금 어려웠습니다

`>` 처음에 **정규표현식**을 사용해야겠다고 생각했지만, 막상 쓰려니 잘 써지지 않았습니다. <br>그래서 [엘리스 학습 자료](https://github.com/bky373/elice-1st-racer/blob/master/week_02_Linux_%26_Git/Linux_02.md)를 다시 보고, 구글링을 하면서 정규표현식을 복습했습니다. <br>이후 `re` 패키지의 메소드(`match`, `search` 등)을 공부하였고, 이 두 가지를 조합해 기능을 완성했습니다. 



### 2. 리눅스 VM 접속 / 환경 구축 

- 리눅스를 배우긴 했지만 잘 사용해보지 않았기 때문에 명령어들이 조금 낯설었습니다. <br>`>` [엘리스 2주차 때 배운 내용](https://github.com/bky373/elice-1st-racer/blob/master/week_02_Linux_%26_Git/Linux_01.md)을 계속 따라해보는 방법으로, 점차 익숙해졌습니다. 

- `ssh(secure shell)`에 대해 잘 알지 못했습니다. <br>`> ` 외부 컴퓨터에 접근하도록 도와주는 프로토콜 중 하나라는 걸 알게 됐습니다.

- DB 관련해서도 궁금하거나 어려운 부분이 있었습니다. 

  > - 로컬 db를 그대로 azure에 옮길 수 있는지
  > - migrations 파일을 git repo에 올려야하는지 올리지 말아야하는지 
  > - 올린다면 azure에서 git pull만 하면 끝나는 건지 등,,

  `>` 아래 코치님의 설명을 듣고 궁금증을 풀 수 있었습니다. 

  > ssh로 azure 접속 -> mysql server 설치 -> flask app 설정 -> migrations 진행 등



### 3. 평점 차트 구현

프로젝트를 진행하던 중, **배달의 민족 가게 리뷰**를 보다가 아래 **평점 차트**가 눈에 띄었습니다.

<img src="https://user-images.githubusercontent.com/49539592/111057761-41152900-84cd-11eb-95a4-74e7e74956be.png" width="320px" height="310px">

도서관의 책도 가게처럼 여러 명의 **별점**을 갖고 있으니, 위와 같이 표현할 수 있겠다고 생각했습니다.<br>차트를 만들어본 경험은 없어서 구글링을 바로 시작했습니다.

참고로 기존 형식을 먼저 살펴보면, 아래 사진처럼 댓글 목록에서 여러 명의 별점을 확인할 수 있습니다. <br>하지만 댓글이 많아졌을 때 별점 분포가 어떻게 되는지 한눈에 파악하기는 어렵습니다.

<img src="https://user-images.githubusercontent.com/49539592/111057910-30b17e00-84ce-11eb-8274-0e00442f8669.png" width="300px" height="360px">



`>` 차트를 그리기 위해선 틀이 필요했고, 저는 `Goole Charts`의 `Bar Charts`를 사용했습니다.<br>그리고 아래 방법대로 책의 별점 데이터를 가져와 그래프의 데이터로 활용했습니다.

> 1. 먼저는 book의 모든 comments를 가져온 후, 반복문으로 각 comment의 rating(1~5점)을 얻습니다.
> 2. 그리고 미리 만든 rating list에 rating을 각각 점수별로 1개씩 더해주어 전체 분포 데이터를 얻습니다.
> 3. 마지막으로 이렇게 얻은 rating list를 그래프의 데이터로 넣어, 최종적인 그래프를 완성합니다. 
>
> - 아래 그래프는 위의 댓글 사진과 연동된 차트입니다. 
>
> - 개인적으로 코드와 디자인을 더 개선해보고 싶습니다.

<img src="https://user-images.githubusercontent.com/49539592/111058133-bb46ad00-84cf-11eb-90ba-07ce9a26f01e.png" width="350px" height="350px">

## 느낀 점

### 1. 라이브러리에 겁 먹지 말자!

이번 프로젝트를 진행하면서 가장 좋았던 경험 중 하나는, <br>필요한 **라이브러리를 직접 찾아보고, 이를 스스로 적용해보았다는 것**입니다.<br>(이번 프로젝트에서는 `유효성 검사 또는 직렬화`를 위해 [**Marshmallow**](https://marshmallow.readthedocs.io/en/stable/) 라이브러리를,<br>`빠른 REST API 빌딩`을 위해 [**Flask-RESTX**](https://flask-restx.readthedocs.io/en/latest/) 라이브러리를 사용했습니다.)

누군가 잘 정리한 코드를 기계적으로 따라가는 방식이 아니라<br>공식 문서에서 시작해, 필요한 기능들을 직접 가져와 사용해보았는데<br>아래와 같은 이점을 얻을 수 있었습니다.

- 우선 **라이브러리의 등장 배경**을 명확히 알 수 있었습니다. <br>2차 가공된 문서보다, 공식 문서를 통해 라이브러리의 **사용 목적**을 분명히 알 수 있었습니다.

- **간단한 기본 예제(Quickstart)** 를 통해 라이브러리의 **전반적인 맥락**을 이해할 수 있었습니다.

- 특정 기능의 **기본 동작**이 무엇인지, **커스텀 가능한 동작**은 무엇인지, <br>**어디서, 어떻게** 사용될 수 있는지 글의 흐름에 따라 쉽게 이해할 수 있었습니다.<br>

- **최신 버전**이 무엇인지, **`deprecated`되는 기능**이 무엇인지 알 수 있었습니다.

  > 예를 들어 `Flask-RESTX`의 경우, [Request Parsing](https://flask-restx.readthedocs.io/en/latest/parsing.html) 기능이 곧 제거될 예정이며, 다른 방식(`marshmallow`)으로 대체될 것이라는 정보가 나와 있습니다.

오버 엔지니어링은 독이 되겠지만, <br>필요한 경우에는 라이브러리를 사용하며, 앞으로도 공식 문서를 적극 활용할 생각입니다! 

### 2. 리팩토링은 재밌다!

작년 8월, [Effective Kotlin 1기](https://github.com/bky373/kotlin-blackjack#Contents) 과정에 참여하여 처음 리팩토링에 대해 알게 되었고,<br>그 매력에 금방 빠지게 되었습니다. 거기서 배운 내용들을 떠올리며 이번 코드에 적용시켜 보았습니다. 

[프로젝트 디렉토리 구조](https://github.com/bky373/elice_library#프로젝트-디렉토리-구조)에서도 알 수 있듯, **관심사 분리**가 주된 목표였습니다.<br>혼자 많은 로직을 감당하던 `views`를 `services`와 `controllers` 로 나누었습니다. <br>그 외에도 필요한 부분들을 나누었고, 동시에 클린 코드를 진행했습니다.

비록 UI/UX에서 달라지는 부분은 없었지만<br>코드의 가독성이 좋아질 때마다 뿌듯했습니다. 

그리고 책임을 분리했을 때 그에 따라 관리가 더 쉬워진다는 걸 몸소 느꼈습니다.<br>이전에는 DB에 새로운 `User`를 추가하는 로직이, `User` 모델과 `views.py`에 걸쳐 있었지만, <br>리팩토링 이후에는 `user_service`에서만 관리하면 되었습니다.<br>앞으로 디자인 패턴 등을 공부해서 새로운 리팩토링 방법들을 알아가는 것도 재밌을 것 같습니다! 

### 3. 에러는 친구와 원수 그 중간 어딘가...

이전까지 에러 메시지는 늘 스트레스였습니다. <br>하지만 이번에 수많은 에러 메시지들을 만나면서 어느새 저도 모르게 친밀감이 생겼습니다. <br>

물론 아직까지는 친구보단 원수에 더 가깝습니다.<br>하지만 메시지조차 던져주지 않는 css에 비하면 <br>무심하게 메시지라도 던져주는 에러에게 그저 감사한 마음이 듭니다.  

친구와 만나고 헤어지듯이, <br>에러와 만나면 아래 [정리해둔 내용](https://kdt-gitlab.elice.io/001_part2_project-library/team1/elice-library/-/issues/8#%EB%AC%B8%EC%A0%9C-%ED%95%B4%EA%B2%B0) 또는 구글링을 통해 헤어졌습니다. 

<img src="https://user-images.githubusercontent.com/49539592/111060398-e6d19380-84df-11eb-99d0-c71f533cb34d.png" width="700px" height="440px">



위처럼 에러를 해결하는 것도 매우 소중한 경험이었습니다. <br>가지각색의 에러에 대처하면서, 여러 가지 기술과 경험을 터득할 수 있어 기뻤습니다. <br>이제는 어떤 에러 메시지를 만나도 이전보다 의연하게 대처할 수 있을 것 같습니다.
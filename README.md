# CLAID

## 배포 사이트
[Play Your Music](https://claid.kr)

## 📚 stacks 
<img src="https://img.shields.io/badge/python 3.10.6 -3776AB?style=for-the-badge&logo=python&logoColor=white"><img src="https://img.shields.io/badge/django 4.2.3-092E20?style=for-the-badge&logo=django&logoColor=white"><img src="https://img.shields.io/badge/restframework 3.14.0-092E20?style=for-the-badge&logo=django&logoColor=white"><img src="https://img.shields.io/badge/Pyenv%203.1.1-4EC9B0?style=for-the-badge&logo=python&logoColor=white"><img src="https://img.shields.io/badge/celery 5.1.1-378A43?style=for-the-badge&logo=celery&logoColor=white"><img src="https://img.shields.io/badge/rabbitmq 3.7.14-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white"><img src="https://img.shields.io/badge/Spleeter 2.3.2-FF0000?style=for-the-badge&logoColor=white"><br><img src="https://img.shields.io/badge/Kakao_Login-FFCD00?style=for-the-badge&logo=kakao&logoColor=black"><img src="https://img.shields.io/badge/Google_Login-4285F4?style=for-the-badge&logo=google&logoColor=white"><img src="https://img.shields.io/badge/simplejwt 5.2.2-092E20?style=for-the-badge&logo=django&logoColor=white"><br><img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white"><img src="https://img.shields.io/badge/postgresql-316192?style=for-the-badge&logo=postgresql&logoColor=white"><br><img src="https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white"><img src="https://img.shields.io/badge/amazonec2-FF9900?style=for-the-badge&logo=amazonec2&logoColor=white"><img src="https://img.shields.io/badge/amazonrds-527FFF?style=for-the-badge&logo=amazonrds&logoColor=white"><img src="https://img.shields.io/badge/Route_53-FF9000?style=for-the-badge&logo=amazon-aws&logoColor=white"><img src="https://img.shields.io/badge/S3-569A31?style=for-the-badge&logo=amazon-s3&logoColor=white"><img src="https://img.shields.io/badge/CloudFront-00C7F2?style=for-the-badge&logo=amazon-aws&logoColor=white"><img src="https://img.shields.io/badge/Elastic_Load_Balancer-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white"><br><img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white"><img src="https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white"><img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"><img src="https://img.shields.io/badge/jQuery%203.7.0-0769AD?style=for-the-badge&logo=jquery&logoColor=white"><br><img src="https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"><img src="https://img.shields.io/badge/gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white"><img src="https://img.shields.io/badge/Nginx%201.32.2-009639?style=for-the-badge&logo=nginx&logoColor=white">

## 🖼️ Front-End
> [Front-End Link](https://github.com/madonghwi/CLAID_front)

## 🤔 최종 프로젝트 : 보컬 합성 음악 커뮤니티 + 음원 분리
------
> 2023.06.05 ~ 2023.07.09
보컬 합성한 음악을 공유하고 보컬 합성하는 방법들을 서로 공유하는 커뮤니티 + 딥러닝 모델을 사용하여 음원 분리

## 🤔 기능
------
### 회원기능 : Jwt Token, Oauth 2.0 사용

1. 회원가입 `POST`
    - 일반 회원가입
    - SNS 회원가입
        - SNS 사이트에 이동하여 사용자 인증 후 앱 연결 동의 후 로그인으로 연결
            - KAKAO
            - GOOGLE
2. 이메일 인증 `POST`
    - uid64를 base64로 디코딩하여 사용자 식별 값을 생성 후 이메일 인증
3. 로그인 `POST`
    - 일반 로그인
    - SNS 로그인
        - SNS 사이트에 이동하여 사용자 인증 후 JWT Token 발급
            - KAKAO
            - GOOGLE
4. 로그아웃
    - 사용자의 웹 브라우저에서 JWT Token 삭제
5. 프로필 `GET`
    - 프로필 이미지, 닉네임

### 포인트
- 회원 가입 시 1000p 지급
- 게시글 작성 시 1000p 지급
- 댓글 작성시 500p 지급
- 게시글 작성 후 24시간이내 삭제 시 1000p 차감

### 음원 분리 (separator)
1. 음악 업로드 `POST`
    - 사용자가 음악을 업로드하면 머신러닝 Spleeter가 분석
    - 보컬과 악기로 나누어줌.
2. 보컬 / 악기 `GET`
    - 목록
        - 음원 분리한 목록들을 PageNumberPagination을 Custom해서 5개씩 나열해줌.
        - 음원들을 wave로 표현
    - 상세페이지
        - 음원들을 wave로 표현
        - 보컬과 악기 오디오를 함께 들으며 테스트
        - 다운로드
        - 볼륨 조절

### 자랑 (article)
1. 게시글 CREATE `POST`
    - 사용자가 제목, 내용, 이미지, 음원파일을 입력하고 작성완료 버튼 클릭 시 게시글 리스트에 생성되어 공유.
2. 게시글 READ `GET`
    - 목록
        - 홈, index.html 게시글 목록
        - 사진과 오디오로 목록화, 누르면 해당 게시글 상세 페이지
    - 상세 페이지
        - 해당 게시글의 작성시간, 작성자 등을 포함한 상세 페이지
        - 댓글 작성 가능
        - 해당 게시글에 달린 댓글 확인 가능

3. 게시글 UPDATE `PATCH`
    - 현재 로그인 되어있는 사용자와 해당 글 작성자가 동일할 경우에만 수정 버튼 생성되며 수정 가능

4. 게시글 DELETE `DELETE`
    - 현재 로그인 되어있는 사용자와 해당 글 작성자가 동일할 경우에만 삭제 버튼 생성되며 삭제 가능
    
5. 댓글 목록 `GET`
    - 댓글을 단 사람의 프로필이미지와 이름을 보여줌
    - 유저네임, 프로필이미지, 좋아요, 댓글내용을 가져옴
    
6. 댓글 작성 `POST`
    - 로그인 한 상태로 내용을 입력해서 댓글을 작성가능 
    - 내용이 없는 댓글 작성불가

7. 댓글 수정 `PATCH`
    - 댓글 작성자만 수정이 가능함
    - 댓글 수정중 취소할 수 있음

8. 댓글 삭제 `DELETE`
    - 댓글 작성자만 가능

9. 좋아요 `POST`
    - 로그인한 사용자만 가능
    - 다시 한번 누르면 좋아요를 취소 할 수 있음

10. 조회수 `GET`
    - IP당 하루에 한 번 오르게 설정
    
### FAQ (VocalNotice)
  - VocalNotice -> 질문 / 공지
1. 게시글 CREATE `POST`
    - 사용자가 제목과 내용을 입력하고 작성완료 버튼 클릭 시 게시글 리스트에 생성되어 공유.
    
2. 게시글 READ `GET`
    - 목록
        - 홈, 게시글 목록을 누르면 해당 게시글 상세 페이지 로드
        - 페이지네이션을 통해 게시글이 많아졌을 때 한번에 10개의 게시글만 보이도록 목록 분리
        -
    - 상세 페이지
        - 해당 게시글의 작성시간, 작성자 등을 포함한 상세 페이지
        - 게시글 좋아요
        - 해당 게시글에 달린 댓글 확인 가능
        - 댓글 작성 가능

3. 게시글 UPDATE `PATCH`
    - 해당 글 작성자만 수정 가능

4. 게시글 DELETE `DELETE`
    - 해당 글 작성자만 삭제 가능

5. 댓글 목록 `GET`
    - 댓글을 단 사람의 프로필이미지와 이름을 보여줌
    - 유저네임, 프로필이미지, 좋아요, 댓글내용을 가져옴

6. 댓글 작성 `POST`
    - 로그인 한 상태로 내용을 입력해서 댓글을 작성가능 
    - 내용이 없는 댓글 작성불가

7. 댓글 수정 `PATCH`
    - 댓글 작성자만 수정이 가능함
    - 댓글 수정중 취소할 수 있음

8. 댓글 삭제 `DELETE`
    - 댓글 작성자만 가능

9. 좋아요 `POST`
    - 로그인한 사용자만 가능
    - 다시 한번 누르면 좋아요를 취소 할 수 있음

10. 조회수 `GET`
    - IP당 하루에 한 번 오르게 설정

### 검색 (Search)
1. artice, vocalnotice 검색 `POST`
    - 각 모델에서 정보를 필터링하여 가져옴

2. 검색결과 `GET`
    - 가져온 결과를 보여줌 내용(contents)에는 제한을 두어 일정 글자수 이상은 ...으로 표기됨 
***
💜 ERD
------
![image](https://file.notion.so/f/s/33d7e11e-7177-4254-841b-7e672436818a/b7-claid-erd.png?id=d9b3e460-23a1-4212-ac53-ebd6401a81f4&table=block&spaceId=881fbe82-e5ca-47db-9089-ae93ae8f7525&expirationTimestamp=1689069600000&signature=ZvAYfMtp6Xi0_Uyi8g_HWdGCqqMO9O8dmLnOYZW32G4&downloadName=b7-claid-erd.png)

💚 API 명세
------
[API 명세](https://juicy-bow-33d.notion.site/4f68e45033084ac8be3d7a4ba7e76ac9?v=62276268370f48a9be9dd75b7880ae87&pvs=4)

🧡 와이어 프레임
------
[와이어 프레임](https://www.figma.com/file/OH25J6tB2MTR1oRDNXh4yv/CLAID-Wireframe?type=design&node-id=0-1&mode=design&t=5BSwjFAS6I6H2tke-0)

💛 역할분담 + 전체 S.A.
------
[역할분담 + SA](https://juicy-bow-33d.notion.site/S-A-4e0242adf881433d9273057cca09496a?pvs=4)

🤎 프로젝트 타임라인
------
[프로젝트 타임라인](https://juicy-bow-33d.notion.site/04d66670f2424788843bb1c5170dc8c8?v=f865c6b085ad49b28e3fa0b408aab2de&pvs=4)


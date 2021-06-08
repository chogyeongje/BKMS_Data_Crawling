# 사용법

### Set Up

아래 코드를 실행하여 필요한 라이브러리 다운로드

```
pip3 install -r requirements.txt
```



### 옵션 설명

> url : 검색을 시작할 Google Scholar 프로필 URL (Google Scholar 검색 -> 왼쪽 메뉴 -> 프로필 선택 해서 나오는 페이지)
>
> interval : 크롤링한 데이터를 저장할 간격 (ex-10 일경우 10개의 데이터마다 csv 로 저장)
>
> max_count : 크롤링할 최대 문서 수
>
> max_author_count : 논문 데이터 크롤링 시 참고할 최대 저자 수
>
> author_link : 저자 링크를 크롤링하고 싶은 경우
>
> author : 저자 데이터를 크롤링 하고 싶은 경우 (저자 링크 크롤링 후 사용)
>
> scholar : 논문 데이터를 크롤링 하고 싶은 경우 (논문 링크 크롤링 후 사용)



### 사용방법

1. 저자 링크 데이터 크롤링

```
python3 run.py --author_link --interval=1000 --max_count=10000
```

2. 저자 데이터 크롤링

```
python3 run.py --author --interval=1000 --max_count=100000
```

3. 논문 데이터 크롤링

```
python3 run.py --scholar --interval=1000 --max_count=100000
```



### 결과

> author_links : 저자 링크 데이터가 저장
>
> authors : 저자 데이터 저장
>
> scholars : 논문 데이터 저장



## 주의사항

1. 간혹 ChromeDriveManager 가 동작하지 않는 경우, `install_driver.py` 파일에서 driveManager 변수에 직접 설치한 ChromeDrivier 경로 입력
2. 논문 데이터는 크롤링 도중 매크로 방지에 의해 동작하지 않을 수 있음;

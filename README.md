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
> max_scholar : 크롤링한 논문 개수가 해당 값 보다 커지면 종료
>
> max_author : 크롤링한 저자 개수가 해당 값 보다 커지면 종료
>
> author : 저자 데이터를 크롤링 하고 싶은 경우
>
> scholar : 논문 데이터를 크롤링 하고 싶은 경우



### 사용 예시

```
python3 run.py --interval=100 --max_scholar=10000 --max_author=100 --author
```



### 결과

> authors_with_page_1 : 저자 데이터가 저장
>
> scholars_with_page_1 : 논문 데이터가 저장


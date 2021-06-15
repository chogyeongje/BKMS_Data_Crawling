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
> start : 시작할 논문 번호 (ex- 101 이라 입력하면 101번째 논문부터 저장)
>
> file_path : 논문 crawling 시 사용할 csv 파일 이름
>
> author_link : 저자 링크를 크롤링하고 싶은 경우
>
> author : 저자 데이터를 크롤링 하고 싶은 경우 (저자 링크 크롤링 후 사용)
>
> scholar : 논문 데이터를 크롤링 하고 싶은 경우 (논문 링크 크롤링 후 사용)



### 사용방법

1. 저자 링크 데이터 크롤링

```
python3 run.py --author_link --interval=1000 --max_count=10000 --url="https://~"
```

2. 저자 데이터 크롤링

```
python3 run.py --author --interval=1000 --max_count=100000
```

3. 논문 데이터 크롤링

file_path : csv 를 명시할 경우 해당 파일에 있는 저자 논문만 크롤링, 명시하지 않은 경우 author_links 에 있는 모든 저자 논문 크롤링

```
python3 run.py --scholar --start=1 --interval=1000 --max_author_count=10000
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





# 서버 세팅

jupyter hub 을 사용할 경우 서버를 시작할 때마다 아래 과정을 실행하여야 한다.

### google-chrome 설치

```
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
```

```
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
```

```
sudo apt-get update
```

```
sudo apt-get install google-chrome-stable
```

```
google-chrome --version 
```

### chromedriver 설치

```
!wget -N https://chromedriver.storage.googleapis.com/91.0.4472.19/chromedriver_linux64.zip
```

```
!unzip chromedriver_linux64.zip
```

```
!mv chromedriver BKMS_Data_Crawling/
```



# Colab 세팅

colab 을 사용하는 경우 아래와 같은 코드를 실행하여야 한다.

```
!sudo apt-get update
```

```
!apt install chromium-chromedriver
```

```
!cp /usr/lib/chromium-browser/chromedriver /usr/bin
```

이후 install_driver.py 의 `driveManager` 변수값을 `chromedriver` 로 수정


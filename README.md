# About
- 현재 세상은 정보가 매우매우 중요하다.. 하루하루 빠르게 바뀌는 세상에서 놓치고 있는 정보들을 얼마나 될까?
  네이버 뉴스를 크롤링해서 Spark를 통해 가공해본 후, AWS S3, RedShift에 저장하여 꼭 읽어야 하는 뉴스를 DB Query를 통해 추출해보자.

# Structure
- 기본 구조는 데이터 엔지니어링에서 사용하는 ETL 구조를 채택. 모든 작업은 Airflow Orchestration 아래에서 자동화됨.
  - Extract : NewsCrawler를 통해 데이터를 추출하여 실행되는 Ubuntu 서버를 DataLake로 사용.
  - Transform : Pyspark를 통해 DataLake에서 읽은 데이터를 Process
  - Load : S3에 저장 후, RedShift까지 적재. ( 실무에서는 이렇게 안쓰이는 것 같은데, 토이프로젝트니깐 그냥 Pass. )
  ![image](https://user-images.githubusercontent.com/18378009/153808666-55eb7a7d-7962-4ff0-b57e-86a054e2dde0.png)

# Directory
1. newscrawler : News를 크롤링해서 csv 파일로 뽑아주는 python 프로그램. Selenium, BeatifulSoup4 사용.
2. newsstatistics : 뽑아낸 csv 파일을 pyspark를 통해 가공하고 parquet 파일의 형태로 s3 에 저장. 이후 s3 에서 aws redshift로 db화
3. dags : Structure에 있는 단계를 Orchstrate 할수 있는 Airflow DAGs. 
  - SparkSubmitOperator, S3ToRedshiftOperator, BashOperator 등을 사용해서 DAGs를 구성해봄.
  ![image](https://user-images.githubusercontent.com/18378009/153809799-f4452887-200e-4f45-86a8-277ac06ee8bd.png)

# Result
위의 task 자동화 dag이 정상 수행 된 이후 Redshift에 정상 적재됨을 확인.
![image](https://user-images.githubusercontent.com/18378009/153551895-364e34e2-545c-4402-8537-84250e9995e0.png)

# Problem history
- 존재하지 않는 element를 찾을때 너무 느림.
  - stackoverflow : https://stackoverflow.com/questions/16075997/iselementpresent-is-very-slow-in-case-if-element-does-not-exist
  - wait command 설명 : https://www.browserstack.com/guide/wait-commands-in-selenium-webdriver

- linux 환경에서 chrome driver를 찾지 못하는 문제
  - https://league-cat.tistory.com/278
  - https://league-cat.tistory.com/356

- AWS S3 Redshift - psycopg2 연결이 안되던 문제
  - https://stackoverflow.com/questions/36881846/configure-security-groups-to-connect-to-postgres-rds-via-client-psycopg2

# Version 
- v1.0 : Initial Commit
- v1.1 ( Branch_Multi-Thread ) : newscralwer MultiProcessing 처리.

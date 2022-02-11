# NewsCrawler
- 현재 세상은 정보가 매우매우 중요하다.. 하루하루 빠르게 바뀌는 세상에서 놓치고 있는 정보들을 얼마나 될까?
  네이버 뉴스를 크롤링해서 꼭 읽어야 하는 정보를 Extract 해보자!

# Structure


1. newscrawler
2. newsstatistics
3. dags


# Result
RedShift에서 크롤링한 데이터를 확인할 수 있음.
![image](https://user-images.githubusercontent.com/18378009/153551814-e7a6a2f1-d7b3-4624-8137-add8f319c595.png)
![image](https://user-images.githubusercontent.com/18378009/153551895-364e34e2-545c-4402-8537-84250e9995e0.png)



# Problem history
- 존재하지 않는 element를 찾을때 너무 느림.
  - stackoverflow : https://stackoverflow.com/questions/16075997/iselementpresent-is-very-slow-in-case-if-element-does-not-exist
  - wait command 설명 : https://www.browserstack.com/guide/wait-commands-in-selenium-webdriver

- linux 환경에서 chrome driver를 찾지 못하는 문제
  - https://league-cat.tistory.com/278
  - https://league-cat.tistory.com/356

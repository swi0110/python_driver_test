### 지원 환경 : Linux OS
### 필요 패키지 : Python3
</br>

#### Test 실행 방법
1. CBURID python driver 설치
 - https://www.cubrid.com/downloads
2. Test.py의 'tc_path'에 Test scenario path 설정
 - 개발 검증시 사용한 Test scenario : https://github.com/CUBRID/cubrid-testcases/tree/develop/sql (중 일부)
3. Python3 Test.py
</br>

#### python test의 문제
1. 테스트하는 파일이 150~200개 이상이면 python driver에서 core가 발생함
2. null 값을 None으로 출력함
3. collection type을 select하면 data에 []를 씌움

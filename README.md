# Dataset
2011-2021 서울 오피스텔 전월세 데이터
(https://www.data.go.kr/data/3050988/fileData.do)

Int64Index: 284785 entries, 0 to 10465
Data columns (total 16 columns):
 #   Column       Non-Null Count   Dtype  
---  ------       --------------   -----  
 0   시군구          284785 non-null  object 
 1   번지           283949 non-null  object 
 2   본번           284785 non-null  int64  
 3   부번           284785 non-null  int64  
 4   단지명          282876 non-null  object 
 5   전월세구분        284785 non-null  object 
 6   전용면적(㎡)      282876 non-null  float64
 7   계약년월         284785 non-null  object 
 8   계약일          284785 non-null  float64
 9   보증금(만원)      284785 non-null  object 
 10  월세(만원)       284785 non-null  int64  
 11  층            284785 non-null  int64  
 12  건축년도         276309 non-null  float64
 13  도로명          284785 non-null  object 
 14  Unnamed: 14  1909 non-null    float64
 15  Unnamed: 15  1909 non-null    object 

# What the project is about
2011년부터 2020년까지 10년 기간의 데이터를 분석 및 시각화하고 이를 토대로 2021년 1월부터 6월까지의 서울 오피스텔 전월세 가격/보증금을 예측함

# Sections
1. EDA 및 결과 시각화
2. 기본 예측 모델로 regression 사용
3. 제출기간까지 남는 시간이 있으면 ML, DL, time series 모델도 추가로 적용하여 가격을 예측해봄   

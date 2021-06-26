# EDA, Regression Modeling and More with Seoul Officetel Rentals Data (2011-2021)

## Introduction
## Preprocessing
### Set Hangeul Font, 한글 폰트 설정
#### - For plotting purposes
#### - matplotlib.rc("font",family=font_name)

import matplotlib as mpl
import matplotlib.font_manager as fm 

# Nanum Gothic Coding
# font_path= r"C:\tmp\NanumGothicCoding-Bold.ttf"

# D2Coding
font_path= r"C:\tmp\D2CodingBold-Ver1.3.2-20180524.ttf".replace("\\","/")

font_name= fm.FontProperties(fname=font_path).get_name() # D2Coding

mpl.rc("font",family=font_name)

# =======================================================
import pandas as pd 

path= "./data/"
#csv_2021= "seoul_rental_2021.csv"
csv_2020= "seoul_rental_2020.csv"
csv_2019= "seoul_rental_2019.csv"
csv_2018= "seoul_rental_2018.csv"
csv_2017= "seoul_rental_2017.csv"
csv_2016= "seoul_rental_2016.txt"
csv_2015= "seoul_rental_2015.txt"
#csv_2014= "seoul_rental_2014.txt"
csv_2014_clean= "seoul_rental_2014_clean.txt"
csv_2013= "seoul_rental_2013.txt"
csv_2012= "seoul_rental_2012.txt"
csv_2011= "seoul_rental_2011.txt"

# df_2021= pd.read_csv(path+csv_2021,encoding="cp949")
# df_2021.shape
df_2020= pd.read_csv(path+csv_2020,encoding="cp949")
df_2019= pd.read_csv(path+csv_2019,encoding="cp949")
df_2018= pd.read_csv(path+csv_2018,encoding="cp949")
df_2017= pd.read_csv(path+csv_2017,encoding="cp949")
df_2016= pd.read_csv(path+csv_2016,encoding="utf-8")
df_2015= pd.read_csv(path+csv_2015,encoding="utf-8")
#df_2014= pd.read_csv(path+csv_2014,encoding="utf-8")
df_2013= pd.read_csv(path+csv_2013,encoding="utf-8")
df_2012= pd.read_csv(path+csv_2012,encoding="utf-8")
df_2011= pd.read_csv(path+csv_2011,encoding="utf-8")
# =======================================================
### Merge 10-year records into one dataframe
#### - Check the shape of all the dataframes

# df_list= [df_2020,df_2019,df_2018,df_2017,df_2016,df_2015,df_2014,df_2013,df_2012,df_2011]
# for i,df in enumerate(df_list):
#     year=2020-i
#     print(year,":",df.shape)
    
# =======================================================
#### - The two unnamed columns are from the year 2014.
#### - tabulation of 1909 rows incorrect; has to be manually adjusted

# df_2014.isna().sum()

df_2014_clean= pd.read_csv(path+csv_2014_clean,encoding="utf-8")
df_2014_clean.shape

df_list= [df_2020,df_2019,df_2018,df_2017,df_2016,df_2015,df_2014_clean,df_2013,df_2012,df_2011]
df_backup= pd.concat(df_list,ignore_index=True)
df= df_backup.copy()
# df.info()

# df.head(1)

# =======================================================
### Columns to be merged/dropped
#### - 번지 (lot number)
#### - 본번 (primary lot number)
#### - 부번 (secondary lot number)
#### - 단지명 (building/estate name)
#### - 도로명 (street address)
#### The street address is the only address that is legally valid in South Korea since the Road Name Address Act came fully into effect on January 1, 2014. The estate name has additional information and will be merged with the street name. The empty cells of the street address column will be filled the lot number and/or the estate name. The lot number is made up of a primary number hyphenated with a secondary number, e.g., 1237-3.
#### 🇰🇷
#### > 도로명주소법이 전면적으로 시행되면서 2014년 1월 1일부터는 토지대장을 제외한 모든 곳에 도로명주소만을 쓸 수 있다. 따라서 도로명 주소와 단지명을 합쳐 각 건물의 전체 주소를 표시하되 도로명 주소 또는 단지명 컬럼이 비어 있으면 번지를 사용한다.

### Rename data columns
#### - 시군구 → district1
#### - 번지 → lot_num
#### - 본번 → lot_num_primary
#### - 부번 → lot_num_secondary
#### - 단지명 → estate_name
#### - 전월세구분 → rent_type (lump-sum or monthly)
#### - 전용면적(㎡) → unit_size (m²)
#### - 계약년월 → sign_yymm
#### - 계약일 → sign_dd
#### - 보증금(만원) → deposit (in 10,000 won)
#### - 월세(만원) → rent_price (in 10,000 won)
#### - 층 → floor
#### - 건축년도 → yr_built
#### - 도로명 → str_addr

cols= ["district1","lot_num","lot_num_primary","lot_num_secondary","estate_name","rent_type","unit_size","sign_yymm","sign_dd","deposit","rent_price","floor","yr_built","str_addr"]

df.columns= cols
# df.head(1)
# df.isna().sum()

import numpy as np 
nan_index= np.where(df.str_addr.isna())
# nan_index
# nan_index[0]

# =======================================================
### Merge str_addr and estate_name
#### - into new column street_addr, and
#### - drop the two columns

import numpy as np
df["estate_name"]= df["estate_name"].astype(str)
df["str_addr"]= df.str_addr.astype(str)
str_addr_series= [row["str_addr"].replace("nan","")+row["estate_name"] if row["str_addr"]=="nan" else row["str_addr"]+", "+row["estate_name"] for i,row in df.iterrows()]
df.insert(0,"street_addr",str_addr_series)

# df.isna().sum()

# =======================================================
### Drop unused columns
#### - lot_num
#### - lot_num_primary
#### - lot_num_secondary
#### - estate_name
#### - str_addr

df.drop(["lot_num","lot_num_primary","lot_num_secondary","estate_name","str_addr"],axis=1,inplace=True)
# df.head(1)

# =======================================================
### New column district
#### - 전체 데이터가 서울 지역에 한정되어 있으므로 "서울특별시", 동 이름 제거

df.insert(0,"district",[val.split()[1] for i,val in df.district1.iteritems() ])
# df.head(2)

df.insert(2,"district_sub",[f"{val.split()[2]}" for i,val in df.district1.iteritems()])
# df.head(1)

# =======================================================
### Drop columns
#### - district1

df.drop("district1",axis=1,inplace=True)
df.head(1)

# =======================================================
### Data imputation: yr_built
#### - Fill empty cells of yr_built with the median value
#### 🇰🇷 - 건축년도가 비어 있는 경우 median value로 채움

#### find the median value for a given column
def find_median(col,df):
    return df[df[col].notna()][col].median()

df.loc[df.yr_built.isna(),"yr_built"]= find_median("yr_built", df) # median: 2013
df["yr_built"]= df.yr_built.astype(int)

df.head(1)
df.isna().sum()
df.yr_built.nunique()
df.yr_built.unique()

# =======================================================
### Create new column sign_date
#### - create `sign_date` from sign_yymm and sign_dd
#### 🇰🇷
#### > 계약년월(예: 202004)과 계약일(11)을 합쳐 sign_date (예: 2020-04-11) 생성

df.sign_dd.value_counts()

#### sign_dd ratio 
(df.sign_dd.value_counts()/df.shape[0])

sign_date= pd.to_datetime((df.sign_yymm.astype(str)+df.sign_dd.astype(str)),format="%Y%m%d")
df.insert(5,"sign_date",sign_date)
df.head(1)

# =======================================================
### rent_type ratio
#### ratio of monthly and lump-sum 
df.rent_type.value_counts()

#### 전세 계약 건물의 건축년도 분포
df[df.rent_type=="전세"]["yr_built"].value_counts()

# df.info()

# ======================================================
### Change dtype of `deposit` to int
#### - First, remove the thousand-separator
#### - and convert to int
df.deposit.astype(str).str.contains(",").sum()
# df["deposit"]= df_backup["보증금(만원)"]
df["deposit"]= df[df.deposit.astype(str).str.contains(",")].deposit.str.replace(",","").astype(int)

# ======================================================
### Impute the monthly rent_price for the lump-sum lease

#### - Zero-value cells will be filled with deposit.mode value of the monthly rent_type
#### 🇰🇷 >  2021년 5월 서울 오피스텔 전월세 전환율은 4.69%이며 전월세 전환식은 아래와 같다.
#### ((lump_sum - new_deposit) * 4.69%) / 12 = monthly_rent
#### 오피스텔 가격동향조사 link: https://www.r-one.co.kr/
deposit_median= df[df.rent_type=="월세"].deposit.median()[0]
df["rent_price_adj"]= ((df.deposit - deposit_median)*.0469)/12
### 월세 계약 건은 원래의 값으로 대체한다
df.loc[df.rent_price_adj==0,"rent_price_adj"]= df.loc[df.rent_type=="월세","rent_price"]

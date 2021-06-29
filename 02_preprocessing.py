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

df_2014_clean= pd.read_csv(path+csv_2014_clean,encoding="utf-8")
df_2014_clean.shape

df_list= [df_2020,df_2019,df_2018,df_2017,df_2016,df_2015,df_2014_clean,df_2013,df_2012,df_2011]
for i,df in enumerate(df_list):
    year=2020-i
    print(year,":",df.info())
    
# =======================================================
#### - The two unnamed columns are from the year 2014.
#### - tabulation of 1909 rows incorrect; has to be manually adjusted
#### - 2014년 단지명에 도로명도 포함된 부분 직접 수정
#### - 2015: 2931 rows 
#### - 2016: 3054 rows
#### - 2017: 7163 rows
#### - 2018: 6276 rows
#### - 2019: 6811
#### - 2020: 6183 rows
# pd.set_option("display.max_rows",106) # 106 rows with whitespace
# na_idx= df_2014_clean[df_2014_clean["도로명"]==" "].index
# df_2014_clean.iloc[na_idx]

# df_2014.isna().sum()

df_list= [df_2020,df_2019,df_2018,df_2017,df_2016,df_2015,df_2014_clean,df_2013,df_2012,df_2011]
df_backup= pd.concat(df_list,ignore_index=True)
df= df_backup.copy()
df.info()
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
#### > 도로명주소법이 전면적으로 시행되면서 2014년 1월 1일부터는 토지대장을 제외한 모든 곳에 도로명주소만을 쓸 수 있다. 따라서 번지는 제외하고 도로명 주소와 단지명을 활용한다.

### Rename data columns
#### - 시군구 → district1
#### - 번지 → lot_num
#### - 본번 → lot_num_1
#### - 부번 → lot_num_2
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

cols= ["district1","lot_num","lotnum_1","lotnum_2","estate_name","rent_type","unit_size","sign_yymm","sign_dd","deposit","rent_price","floor","yr_built","str_addr"]

df.columns= cols
# df.head(1)
# df.isna().sum()

# import numpy as np 
# nan_index= np.where(df.str_addr.isna())
# nan_index
# nan_index[0]

# =======================================================
### Merge str_addr and estate_name
#### - into new column street_addr, and
#### - drop the two columns
import numpy as np
df["estate_name"]= df["estate_name"].astype(str)
df["str_addr"]= df.str_addr.astype(str)

# str_addr_series= [row["str_addr"].replace("nan","")+row["estate_name"] if row["str_addr"]=="nan" else row["str_addr"]+", "+row["estate_name"] for i,row in df.iterrows()]
# df.insert(0,"street_addr",str_addr_series)
#### 🇰🇷
#### > 탐색 결과 도로명 컬럼에 whitespace만 있는 row가 파일마다 수천개 발견됨. 빈 cell은 단지명으로 채움
### Fill in empty or whitespaced cells with estate_name
idx_empty_addr= df[df.str_addr==" "].index
idx_empty_addr.shape

# 도로명이 비어있는 레코드 중 다른 연도 파일에 도로명이 기록되어 있으면 복사하여 채운다
df["estate_name"]= df.estate_name.str.strip().astype(str)
df["str_addr"]= df.str_addr.str.strip().astype(str)

empty_strt_estate= list(df.iloc[idx_empty_addr].estate_name.unique()) # 261 properties
estate_street_name= df[df.str_addr!=""][["estate_name","str_addr"]].drop_duplicates()
ESTATE_STR_ADDR= {} # KEY estate_name: VALUE street_addr
for i,row in estate_street_name.iterrows():
    # list of estate without street addr
    for es in empty_strt_estate:
        if es in row["estate_name"]:
            ESTATE_STR_ADDR[es]= row.str_addr
            continue

# =======================================================
# 도로 주소가 없는 셀에 단지명을 채워넣음.
# 32418 rows 
from timeit import default_timer as timer
start_t= timer()
for i in idx_empty_addr:
    estate_name= df.loc[i,"estate_name"]
    str_addr= ESTATE_STR_ADDR.get(estate_name)
    df.loc[i,"str_addr"]= str_addr if str_addr is not None else estate_name
elapsed_t= timer()-start_t
print(elapsed_t,"seconds")

#### function equivalent to the above
def replace_none(estate_name,str_addr):
    if str_addr is None:
        return estate_name
    else:
        return str_addr
df.loc[idx_empty_addr,"str_addr"]=df.iloc[idx_empty_addr][["estate_name","str_addr"]].apply(lambda x: replace_none(*x),axis=1)#.drop_duplicates()

# =======================================================

# df.isna().sum()

# =======================================================
### Drop unused columns
#### - lot_num
#### - lot_num_2
#### - estate_name
#### - str_addr

df.drop(["lot_num","lotnum_2","estate_name"],axis=1,inplace=True)
# df.head(1)

# =======================================================
### New column district
#### - 전체 데이터가 서울 지역에 한정되어 있으므로 "서울특별시", 동 이름 제거

df.insert(0,"district",[val.split()[1] for i,val in df.district1.iteritems() ])
df.head(1)

df.insert(1,"old_div",[f"{val.split()[2]}" for i,val in df.district1.iteritems()])
df.head(1)

# =======================================================
### Drop columns
#### - district1

df.drop("district1",axis=1,inplace=True)
# df.head(1)

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
# df.isna().sum()
# df.yr_built.nunique()
# df.yr_built.unique()

# =======================================================
### Create new column sign_date
#### - create `sign_date` from sign_yymm and sign_dd
#### 🇰🇷
#### > 계약년월(예: 202004)과 계약일(11)을 합쳐 sign_date (예: 2020-04-11) 생성

# df.sign_dd.value_counts()

#### sign_dd ratio 
(df.sign_dd.value_counts()/df.shape[0])

sign_date= pd.to_datetime((df.sign_yymm.astype(str)+df.sign_dd.astype(str)),format="%Y%m%d")
df.insert(7,"sign_date",sign_date)
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
df["deposit"]= df.astype(str).deposit.str.replace(",","").astype(int)

# df= df.convert_dtypes()
# df.dtypes

# =====================================================
### Impute the monthly rent_price for the lump-sum lease

#### - Zero-value cells will be filled with deposit.mode value of the monthly rent_type
#### 🇰🇷 >  2021년 5월 서울 오피스텔 전월세 전환율은 4.69%이며 전월세 전환식은 아래와 같다.
#### ((lump_sum - new_deposit) * 4.69%) / 12 = monthly_rent
#### 오피스텔 가격동향조사 link: https://www.r-one.co.kr/
# deposit_median= df[df.rent_type=="월세"].deposit.median()#[0]
# df["rent_price_adj"]= ((df.deposit - deposit_median)*.0469)/12
### replace zero cells with the original rent_price for monthly rent type 월세 계약 건은 원래의 값으로 대체한다
# df.loc[df.rent_price_adj<=0,"rent_price_adj"]= df.loc[df.rent_type=="월세","rent_price"]
# =====================================================

### GPS coordinates for the 25 districts
### - ['강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구', '노원구',       '도봉구', '동대문구', '동작구', '마포구', '서대문구', '서초구', '성동구', '성북구', '송파구',       '양천구', '영등포구', '용산구', '은평구', '종로구', '중구', '중랑구']

coords= [
    (37.5172, 127.0473), #gangnam
    (37.5301, 127.1238), #gangdong
    (37.6396, 127.0257), #gangbuk-gu
    (37.5510, 126.8495),# gangseo-gu
    (37.4784, 126.9516),# gwanak-gu
    (37.5385, 127.0823), #gwangjin-gu 
    (37.4954, 126.8874), #guro-gu
    (37.4519, 126.9020), #geumcheon-gu
    (37.6542, 127.0568), #nowon-gu
    (37.6688, 127.0471), #dobong-gu
(37.5744, 127.0400), #dongdaemun-gu
(37.5124, 126.9393), #dongjak-gu
(37.5638, 126.9084), #mapo-gu
(37.5791, 126.9368), #seodaemun-gu
(37.4837, 127.0324), #seocho-gu
(37.5633, 127.0371), #seongdong-gu
(37.5891, 127.0182), #seongbuk-gu
(37.5145, 127.1066), #songpa-gu
(37.5169, 126.8664), #yangcheon-gu
(37.5264, 126.8962), #yeongdeungpo-gu
    (37.5384, 126.9654), #yongsan-gu
    (37.6027, 126.9291), #eunpyeong-gu
    (37.5730, 126.9794), #jongno-gu
    (37.5641, 126.9979), #jung-gu
    (37.6066, 127.0927), #jungnang-gu
]

DISTRICT_LAT= {}
DISTRICT_LON= {}
for idx,name in enumerate((list(df.district.unique()))):
    DISTRICT_LAT[name]= coords[idx][0]
    DISTRICT_LON[name]= coords[idx][1]

### Add latitude and longitude columns
lat= [DISTRICT_LAT.get(name) for i,name in df["district"].iteritems()]
lon= [DISTRICT_LON.get(name) for i,name in df["district"].iteritems()]

df.insert(1,"latitude",lat)
df.insert(2,"longitude",lon)
df.head(1)
# =====================================================
df.insert(3,"street_addr",df.str_addr)
del df["str_addr"]
df.head(1)

# =====================================================
### separate street names using regular expression
#
# https://stackoverflow.com/questions/43237338/python-regular-expression-split-string-into-numbers-and-text-symbols
import re
re.sub("\(|\)","","(1237-3)") # gives 1237-3

import re
def find_pattern(pat,str_seq):
    # \d+     matches one or more digits
    # \d*\D+  matches zero or more digits followed by one or more non-digits
    # \d+|\D+ matches one or more digits OR one or more non-digits
    return re.search(pat,str_seq).group()

#### split by whitespace \s or
####  one or more digits \d+ 
#마곡중앙로 161-11, 힐스테이트에코 마곡나루역 라마다앙코르 서울마곡
import re
ser_street= [re.split("\d+|\(",val)[0] for val in df.street_addr.values]
#### longest street name
# max(ser_street,key=len) # 목동중앙북로

### Add new `street` column
df.insert(3,"street",ser_street)
df.head(1)

#
df[df.street.str.contains("청룡")].street_addr.unique() #청룡_길
df[df.street.str.contains("진관")].street_addr.unique() #진관_로
df[df.street.str.contains("마곡중앙")].street_addr.unique() # 마곡중앙로
df[df.street.str.contains("승방")].street_addr.unique() # 승방길

### ==========================================
### Numeric encoding
#### - `district`: 4 groups
#### - `old_div`: 272 categories -> 4*4 groups
#### - `floor`: <=10, >10, >20 -> 3 groups
#### - `yr_built`: 70s,80s,90s,00s,10s -> 5 groups 
#### 🇰🇷
#### > categorical 유형의 컬럼은 숫자형으로 encode함

df["district"]= df.district.astype("category")
df["old_div"]= df.district.astype("category")
df["floor"]= df.district.astype("category")
df["yr_built"]= df.district.astype("category")
df.dtypes

import category_encoders as ce
from timeit import default_timer as timer

### ==========================================
### encode `district`
start_t= timer()

# ce_hash.hashing_trick(df[["old_div"]], N=10, cols=['old_div'])
encoder= ce.hashing.HashingEncoder(cols=["district"],return_df=True)
df_enc= encoder.hashing_trick(df[["district","latitude","longitude"]],N=4)
# df_enc.insert(0,"district",df.district)

print("elapsed:",timer()-start_t,"seconds")
df_enc.head(1)

### ==========================================
### encode `old_div`
start_t= timer()
encoder= ce.hashing.HashingEncoder(cols=["old_div"],return_df=True)
df_enc= encoder.hashing_trick(df[["old_div","latitude","longitude"]],N=16)
print("elapsed:",timer()-start_t,"seconds")
df_enc.head(1)

### ==========================================
### encode `floor`
start_t= timer()
encoder= ce.hashing.HashingEncoder(cols=["floor"],return_df=True)
df_enc= encoder.hashing_trick(df[["floor","yr_built"]],N=3)
print("elapsed:",timer()-start_t,"seconds")
df_enc.head(1)

### ==========================================
### encode `yr_built`
start_t= timer()
encoder= ce.hashing.HashingEncoder(cols=["yr_built"],return_df=True)
df_enc= encoder.hashing_trick(df[["yr_built","latitude","longitude"]],N=5)
print("elapsed:",timer()-start_t,"seconds")
df_enc.head(1)

### ==========================================
### Divide the dataset by `rent_type`
#### - Lump-sum: `deposit` is chosen as the target variable.
#### - Monthly: `rent_price` as the target variable.   
#### 🇰🇷
#### > 임대 유형에 따라 target_variable이 달라지므로 데이터세트를 분리함

df_lumpsum= df[df.rent_type=="전세"].drop("rent_type",axis=1)
df_monthly= df[df.rent_type=="월세"].drop("rent_type",axis=1)
# 전세 데이터세트 중 월세가 0보다 큰 3건은 고려 안 함
# drop rent_price column from df_lumpsum
df_lumpsum.drop("rent_price",axis=1) 
df_lumpsum.shape, df_monthly.shape

df.head(1)

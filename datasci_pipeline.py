# EDA, Regression Modeling and More with Seoul Officetel Rentals Data (2011-2021)

## Introduction
## Preprocessing

from matplotlib import font_manager,rc
import matplotlib

# D2Coding
# font_path= r"C:\Users\Jieun\AppData\Local\Microsoft\Windows\Fonts\D2CodingBold-Ver1.3.2-20180524.ttf".replace("\\","/")

# Medium
font_path= r"C:\Windows\Fonts\SourceCodePro-Semibold.ttf".replace("\\","/")

font_name= font_manager.FontProperties(fname=font_path).get_name() # D2Coding

matplotlib.rc("font",family=font_name)

# =========================================
import pandas as pd 
path= "./data/"
# csv_2021= "seoul_rental_2021.txt"
csv_2020= "seoul_rental_2020.csv"
csv_2019= "seoul_rental_2019.csv"
csv_2018= "seoul_rental_2018.csv"
csv_2017= "seoul_rental_2017.csv"
csv_2016= "seoul_rental_2016.txt"
csv_2015= "seoul_rental_2015.txt"
csv_2014= "seoul_rental_2014.txt"
csv_2014_clean= "seoul_rental_2014_clean.txt"
csv_2013= "seoul_rental_2013.txt"
csv_2012= "seoul_rental_2012.txt"
csv_2011= "seoul_rental_2011.txt"

# df_2021= pd.read_csv(path+csv_2021,encoding="utf-8")
# df_2021.shape
df_2020= pd.read_csv(path+csv_2020,encoding="cp949")
df_2019= pd.read_csv(path+csv_2019,encoding="cp949")
df_2018= pd.read_csv(path+csv_2018,encoding="cp949")
df_2017= pd.read_csv(path+csv_2017,encoding="cp949")
df_2016= pd.read_csv(path+csv_2016,encoding="utf-8")
df_2015= pd.read_csv(path+csv_2015,encoding="utf-8")
# df_2014= pd.read_csv(path+csv_2014,encoding="utf-8")
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
# print("="*35)

df_2014_clean= pd.read_csv(path+csv_2014_clean,encoding="utf-8")
# df_2014_clean.shape

df_list= [df_2020,df_2019,df_2018,df_2017,df_2016,df_2015,df_2014_clean,df_2013,df_2012,df_2011]
for i,df in enumerate(df_list):
    year=2020-i
    print(year,":",df.shape)
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
#### - 월세(만원) → pay_monthly (in 10,000 won)
#### - 층 → floor
#### - 건축년도 → yr_built
#### - 도로명 → str_addr

cols= ["district1","lot_num","lotnum_1","lotnum_2","estate_name","rent_type","unit_size","sign_yymm","sign_dd","deposit","pay_monthly","floor","yr_built","str_addr"]

df.columns= cols
# df.head(1)
# df.isna().sum()

# import numpy as np 
# nan_index= np.where(df.str_addr.isna())
# nan_index

# =======================================================
### Fill in empty or whitespaced cells with estate_name
#### 🇰🇷
#### > 탐색 결과 도로명 컬럼에 whitespace만 있는 row가 파일마다 수천개 발견됨. 빈 cell은 단지명으로 채움

# Of 32419 cells of length 1,
# - 32418 cells has one whitespace,
# 🇰🇷 도로 주소가 없는 " " 셀에 단지명을 채워넣음.
# 32418 rows 
# df["estate_name"]= df_backup["단지명"]
df["estate_name"]= df.estate_name.astype(str)
df["str_addr"]= df.str_addr.astype(str)
idx= df[(df.str_addr.str.len()==1)&(df.str_addr==" ")].index # idx.shape
df.loc[idx,"str_addr"]= df.iloc[idx].estate_name
df.iloc[idx].str_addr

#### and the remaining one cell has the value of "5"; will be filled manually with its street address 
# index 166852, current str_addr: "5"
# manually change it to "선유로11길 5"
idx_one= df[(df.str_addr.str.len()==1)&(df.str_addr!=" ")].index # idx.shape
df.loc[idx_one,"str_addr"]= "선유로11길 "+df.iloc[idx_one].str_addr.str[0]
### ==================================================

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
# df.head(1)

df.insert(1,"old_div",[f"{val.split()[2]}" for i,val in df.district1.iteritems()])
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

# df.loc[df.yr_built.isna(),"yr_built"]= find_median("yr_built", df) # median: 2013
df.yr_built.fillna(df.yr_built.median(),inplace=True)
df["yr_built"]= df.yr_built.astype(int)

# df.head(1)
# df.isna().values.any()
# df.isna().sum()

# =======================================================
### Create new column sign_date
#### - create `sign_date` from sign_yymm and sign_dd
#### 🇰🇷
#### > 계약년월(예: 202004)과 계약일(11)을 합쳐 sign_date (예: 2020-04-11) 생성
sign_date= pd.to_datetime((df.sign_yymm.astype(str)+df.sign_dd.astype(str)),format="%Y%m%d")
df.insert(7,"sign_date",sign_date)
df.head(1)

# df.sign_dd.value_counts()

#### sign_dd ratio 
# (df.sign_dd.value_counts()/df.shape[0])

# =================================================
### rent_type ratio
#### ratio of monthly and lump-sum 
# df.rent_type.value_counts()

#### 전세 계약 건물의 건축년도 분포
# df[df.rent_type=="전세"]["yr_built"].value_counts()

# ======================================================
### Change dtype of `deposit` to int
#### - First, remove the thousand-separator
#### - and convert to int
#### 🇰🇷 
#### > 보증금 컬럼의 구분자(,)를 제거하고 dtype을 int로 변환
df.deposit.astype(str).str.contains(",").sum()
# df["deposit"]= df_backup["보증금(만원)"]
df["deposit"]= df.deposit.astype(str).str.replace(",","").astype(int) # 2125 => 1806 unique values

### =====================================================
### Change dtype of `lotnum_1`,`sign_yymm`,`sign_dd`,`rent_price`,`floor` to int32
#### 🇰🇷 
#### > dtype을 int32/float32로 변환하며 memory usage ↓
import numpy as np
df.lotnum_1= df.lotnum_1.astype(int)
df.sign_yymm= df.sign_yymm.astype(int)
df.sign_dd= df.sign_dd.astype(int)
df.unit_size= df.unit_size.astype(np.float32)
df.pay_monthly= df.pay_monthly.astype(int)
df.floor= df.floor.astype(int)

# df= df.convert_dtypes()
# df.dtypes
df.info()

### dataset shape: (284785 rows, 13 columns)
## 0   district    284785 non-null  object        
#  1   old_div     284785 non-null  object        
#  2   lotnum_1    284785 non-null  int32         
#  3   rent_type   284785 non-null  object        
#  4   unit_size   284785 non-null  float32       
#  5   sign_yymm   284785 non-null  int32         
#  6   sign_dd     284785 non-null  int32         
#  7   sign_date   284785 non-null  datetime64[ns]
#  8   deposit     284785 non-null  int32         
#  9   rent_price  284785 non-null  int32         
#  10  floor       284785 non-null  int32         
#  11  yr_built    284785 non-null  int32         
#  12  str_addr    284785 non-null  object        
# dtypes: datetime64[ns](1), float32(1), int32(7), object(4)
# memory usage: 19.6+ MB 

print(df.shape) #(284785 rows, 13 columns)

print(df.isna().sum())
# =============================================
### Number of missing values
# district      0
# old_div       0
# lotnum_1      0
# rent_type     0
# unit_size     0
# sign_yymm     0
# sign_dd       0
# sign_date     0
# deposit       0
# rent_price    0
# floor         0
# yr_built      0
# str_addr      0


# =====================================================
## FEATURE ENGINEERING
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

# str_addr
# separate street names using regular expression
#
# https://stackoverflow.com/questions/43237338/python-regular-expression-split-string-into-numbers-and-text-symbols

# import re
# re.sub("\(|\)","","(1237-3)") # gives 1237-3
# def find_pattern(pat,str_seq):
#     # \d+     matches one or more digits
#     # \d*\D+  matches zero or more digits followed by one or more non-digits
#     # \d+|\D+ matches one or more digits OR one or more non-digits
#     return re.search(pat,str_seq).group()

#### split by whitespace \s or
####  one or more digits \d+ 
#마곡중앙로 161-11, 힐스테이트에코 마곡나루역 라마다앙코르 서울마곡
import re
# ser_street= [re.split("\d+|\(",val)[0] for val in df.str_addr.values]
# str_addr= str_addr.apply(lambda x: re.sub("\(|\)|\s","",x))

# 77 rows has lot_number in their street address
# df["str_addr"]= df_backup["도로명"]
# str_addr= df[df.street.str.len()<3]["str_addr"]
# str_addr= df[df.street.str.len()==2]["str_addr"]

#
# =================================
# Add new `street` column
# separator: whitespace

dict_lot_num_street= {}
dict_lot_num_street["669-3"]= "방학로 173"
dict_lot_num_street["121-5"]= "동소문로24길 13-9"
dict_lot_num_street["441-11"]= "고덕로 45"
dict_lot_num_street["204-5"]= "자곡로 127"
dict_lot_num_street["9-13"]= "양천로57길 9-13"
dict_lot_num_street["115-1"]= "마곡서1로 115-1"
dict_lot_num_street["10-16"]= "중앙로 10-16"
dict_lot_num_street["16"]= "선릉로89길 16"
dict_lot_num_street["355"]= "아차산로 355"
dict_lot_num_street["164"]= "사당로 164"
dict_lot_num_street["212"]= "올림픽로 212"

dict_lot_num_street["한흥 삼성오피스텔"]= "봉은사로 430"
dict_lot_num_street["한흥삼성오피스텔"]= "봉은사로 430"
dict_lot_num_street["강남 드림하이 오피스텔"]= "헌릉로569길 21-30"
dict_lot_num_street["강남드림하이오피스텔"]= "헌릉로569길 21-30"
dict_lot_num_street["역삼 푸르지오 시티"]= "논현로85길 52"
dict_lot_num_street["역삼푸르지오시티"]= "논현로85길 52"
dict_lot_num_street["강일 포디움"]= "아리수로91길 24-9"
dict_lot_num_street["강일포디움"]= "아리수로91길 24-9"
dict_lot_num_street["에코 타워빌"]= "성안로27길 51-14"
dict_lot_num_street["에코타워빌"]= "성안로27길 51-14"
dict_lot_num_street["GM Valley"]= "곰달래로 116"
dict_lot_num_street["GMValley"]= "곰달래로 116"
dict_lot_num_street["금천 롯데캐슬 골드파크 2차"]= "벚꽃로 30"
dict_lot_num_street["금천롯데캐슬골드파크2차"]= "벚꽃로 30"
dict_lot_num_street["도봉 엠블렘"]= "도봉로180길 38"
dict_lot_num_street["도봉엠블렘"]= "도봉로180길 38"
dict_lot_num_street["도봉 투웨니퍼스트 1단지"]= "도봉로180길 20"
dict_lot_num_street["도봉투웨니퍼스트1단지"]= "도봉로180길 20"
dict_lot_num_street["도봉 투웨니퍼스트 2단지"]= "도봉로180길 28"
dict_lot_num_street["도봉투웨니퍼스트2단지"]= "도봉로180길 28"
dict_lot_num_street["창동 투웨니퍼스트"]= "도봉로110라길 70-14"
dict_lot_num_street["창동투웨니퍼스트"]= "도봉로110라길 70-14"

df["str_addr2"]= df.str_addr.apply(lambda x: dict_lot_num_street.get(x,x)) # get value of x, if none keep it

import re
str_addr= df.str_addr.apply(lambda x: x.strip())
str_addr= str_addr.apply(lambda x: x if dict_lot_num_street.get(x)==None else dict_lot_num_street.get(x)) # get value of x, if none keep it

# import numpy as np
# np.argmin(str_addr.str.len())

ser_street= [re.split("\s",val)[0] for val in str_addr.values]
#### longest street name
# max(ser_street,key=len) # 목동중앙북로

### Add new `street` column
del df["street"]
df.insert(3,"street",ser_street)
df.head(1)

# 

### ===============================================
### ============== basic statistics ==============
### ===============================================
columns= ["latitude","longitude",'yr_built', 'unit_size', 'floor','deposit', 'pay_monthly' ]
col_desc= ["Year Built","Unit Size","Floor","Deposit","Monthly Rent"]
datetime= "sign_date"

df[columns].describe()

# histograms
import matplotlib.pyplot as plt 
plt.style.use("fivethirtyeight")
plt.style.use("ggplot")
df[columns].hist(bins=50,figsize=(11,10))
plt.savefig("df[columns].hist(bins_50).png")
plt.show()

# ========================================
# FOLIUM
import folium

# seoul_map = folium.Map(location=[37.55,126.98],zoom_start=12) # city center 37.56421, 127,00169

data_map= folium.Map(location=[37.56421, 127.00169],zoom_start=10)

df_songpa= df[df.district=="송파구"]

for district,lat,lon in zip(df_songpa.district,df_songpa.latitude,df_songpa.longitude):
    folium.Marker(location=[lat,lon],tootip=district,).add_to(data_map)
data_map


# =======================================
# GEOPANDAS
# https://thlee33.medium.com/geopandas-%EA%B8%B0%EC%B4%88-fe1feecd2ab4
import geopandas as gpd

from IPython.display import display
from IPython.display import HTML

geom_district= gpd.points_from_xy(df.longitude, df.latitude)
geom_district[:3]

# add location info
columns= ["district","street","old_div"]
gdf_district= gpd.GeoDataFrame(df[columns],geometry=geom_district,crs="epsg:4326") # google earth
gdf_district.head(1)

# convert coord. system to epsg:3857 (google/bing/yahoo,osm maps)
gdf_3857= gdf_district.to_crs(epsg=3857)

# plot
gdf_3857.drop_duplicates().plot(color="gray")

# ================
# SAVE AS GEOJSON
gdf_3857.drop_duplicates().to_file(path+"district.geojson",driver="GeoJSON")

# plot gangnam-gu
gdf_3857[gdf_3857.district=="강남구"].drop_duplicates().plot()

# =======================
# LOAD SEOUL DISTRICT MAP
#
# SIG_202101/TL_SCCO_SIG.shp
# path_geo= "./data/seoul_streets/"
# filename= "Z_KAIS_TL_SPRD_MANAGE_11000.shp"
map_seoul= gpd.read_file(path_geo+filename,encoding="cp949")
map_seoul

path_geo= "./data/seoul_districts/"
filename= "LARD_ADM_SECT_SGG_11.shp"
map_seoul= gpd.read_file(path_geo+filename,encoding="cp949")
map_seoul.crs

# convert coord. system to epsg:3857 (google/bing/yahoo,osm maps)
map_seoul_3857= map_seoul.to_crs(epsg=3857)
map_seoul_3857.crs

# untidy cells of SGG_NM: 
# 서울시노원구,서울시성북구,서울시도봉구
map_seoul_3857.SGG_NM= map_seoul_3857.SGG_NM.astype(str).apply(lambda x: re.sub("서울시","",x))

# ADM_SECT_C: district code
map_seoul_3857["ADM_SECT_C"]= map_seoul_3857["ADM_SECT_C"].astype(str)
map_seoul_3857.plot(color="gray")

# =================================
# MERGE GDF_DISTRICT WITH MAP_SEOUL
drop_cols= ["lotnum_1","str_addr","latitude","longitude"]
gdf_map= pd.merge(map_seoul_3857[['ADM_SECT_C', 'SGG_NM', 'geometry']],df.drop(drop_cols,axis=1),how="left",left_on="SGG_NM",right_on="district")

# For plotting
import matplotlib as mpl 
import matplotlib.pyplot as plt 
import seaborn as sns 
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Choropleth map

# ,label=['강서구', '영등포구', '마포구', '구로구', '송파구', '관악구', '강남구', '은평구', '동대문구', '강동구','서초구', '금천구', '양천구', '성동구', '광진구', '중구', '용산구', '서대문구', '도봉구', '종로구','중랑구', '노원구', '동작구', '성북구', '강북구']
district_ratio= gdf_map.district.value_counts()/gdf_map.shape[0]*100

fig,ax= plt.subplots(1,1,figsize=(20,8))
divider= make_axes_locatable(ax)
cax= divider.append_axes("right", size="5%",pad=.1)

gdf_map.drop_duplicates("district").plot((district_ratio/gdf_map.shape[0]*100).values,ax=ax,legend=True,cax=cax,edgecolor="black",cmap="cubehelix_r")
ax.set_title("Rentals (%) by District")
ax.set_axis_off()
plt.show()

# ================================
# GEOPLOT
# coord system: 4326, google earth
district_ratio= gdf_map.district.value_counts()
df_district_ratio= pd.DataFrame({"rental_vol":district_ratio,"rental_ratio":(district_ratio/gdf_map.shape[0]*100)},index=district_ratio.index)

gdf_map_ge= gdf_map.drop_duplicates("district").to_crs(epsg=4326)
gdf_map_ge= pd.merge(gdf_map_ge,df_district_ratio,how="left",left_on="district",right_on=df_district_ratio.index)

gdf_map_centroid= gdf_map_ge.copy()
gdf_map_centroid["geometry"]= gdf_map_centroid["geometry"].centroid

# ===========================================
# Rental Volumes in five groups

gdf_map_centroid[["district","rental_vol"]].sort_values("rental_vol",ascending=False)
# district	rental_vol
# 9	강서구	    43464
# 6	영등포구	34144
# 11 마포구	    21643
# 8	구로구	    21501
# 1	송파구	    20544
# 4	관악구	    18090
# 2	강남구	    17221
# 13 은평구	    13144
# 19 동대문구	10346

import matplotlib.pyplot as plt
import geoplot as gplt 
import geoplot.crs as gcrs
import mapclassify as mc
import pyproj
plt.style.use("fivethirtyeight")
plt.style.use("seaborn-notebook")

scheme= mc.Quantiles(gdf_map_centroid["rental_vol"],k=7) # Rental Volumes in five groups

proj= gcrs.WebMercator()

ax= gplt.polyplot(gdf_map_ge,zorder=-1,linewidth=1,projection=proj,facecolor="lightgray",edgecolor="white",figsize=(15,8))

gplt.pointplot(gdf_map_centroid,projection=gcrs.WebMercator(),scale="rental_vol",limits=(10,50),hue="rental_vol",scheme=scheme,cmap="viridis_r",legend=True,legend_var="hue",ax=ax)

plt.title("Rental Volumes in 7 Groups",fontsize=16)

# ========================
# ADD BACKGROUND MAP
import contextily as ctx

scheme= mc.Quantiles(gdf_map_centroid["rental_ratio"],k=7) # Rental Volumes in five groups
extent= gdf_map_ge.total_bounds

# plt.figure(figsize=(15,8))
ax= gplt.pointplot(gdf_map_centroid,projection=proj,alpha=.8,scale="rental_ratio",limits=(30,100),hue="rental_ratio",scheme=scheme,cmap="summer_r",legend=True,legend_var="hue",figsize=(25,25))
gplt.webmap(gdf_map_ge,ax=ax,extent=extent,provider=ctx.providers.Stamen.TonerLite)

plt.setp(ax.get_legend().get_texts(), fontsize='22') # for legend text
# plt.setp(plt.legend.set_title('Rental Volume'),prop={'size':'large'})
plt.show()




# =============================================
### column `district`
import matplotlib
import matplotlib.pyplot as plt 
import seaborn as sns

# boxplot: district 송파구
plt.style.use("fivethirtyeight")
figsize=(10,5)  #(16,6) 
fix,ax= plt.subplots(ncols=2,nrows=1, figsize=figsize)

sns.boxplot(ax=ax[0],x="district",y="pay_monthly",data=df[df.district=="송파구"],linewidth=1) #orient="h"
sns.violinplot(ax=ax[1],x="district",y="pay_monthly",data=df[df.district=="송파구"],color=".25") #orient="h"
plt.show()

# sns.set_theme(style="ticks",color_codes=True) # does not work for Korean
plt.style.use("seaborn-paper")
figsize=(16,6)  #(16,6) 
fix,ax= plt.subplots(figsize=figsize)
sns.boxplot(ax=ax,x="district",y="pay_monthly",data=df,linewidth=1) #orient="h"


print("The district names:\n",df.district.unique())
print("="*50)
print("The number of the districts:",df.district.nunique())
print("="*50)
print(f"The occurrence ratio (%) of the districts:\n{('=')*45}\n{np.round(df.district.value_counts()/df.shape[0]*100,2)}")

# =============================================
### column `old_div`
print("The old_div (동) names:\n",df.old_div.unique())
print("="*50)
print("The number of 동 :",df.old_div.nunique()) # 272 
print("="*50)
print(f"The occurrence of 동:\n{('=')*45}\n{df.old_div.value_counts()}")

# =============================================
### Column `rent_type`
# Rent type:
# =============================================
# 월세    153970
# 전세    130815
print(f"Rent type:\n{('=')*15}\n{df.rent_type.value_counts()}")


# pay_monthly: min,max: (0,2123)
# deposit    : min,max: (20,554100)
import matplotlib.pyplot as plt
plt.style.use("fivethirtyeight")
plt.style.use("seaborn-notebook")
plt.figure(figsize=(8,5))
h=plt.hist2d(df.yr_built, df.pay_monthly,bins=(10,10),vmax=2200)
cbar=plt.colorbar(h[3],label="monthly rent")
cbar.solids.set_edgecolor("face")
plt.xlabel("Year Built")
plt.ylabel("Monthly Rent (in 10K won)")
plt.show()

### =============================================
### Column `sign_date`
### - year of contract
### - month of contract
# ======================
# Year of Contract:
# ======================
# 2020    50310
# 2019    48053
# 2018    39927
# 2017    34668
# 2016    27497
# 2015    24528
# 2014    20699
# 2013    16151
# 2012    12482
# 2011    10454
# 2010       16
print(f"Year of Contract:\n{('=')*22}\n{df.sign_date.dt.isocalendar().year.value_counts()}")

# ======================
# Month of Contract:
# ======================
# 1     28815
# 2     28021
# 12    25430
# 8     24348
# 7     24317
# 3     24055
# 6     22397
# 10    22342
# 5     21672
# 11    21588
# 4     21132
# 9     20668
print(f"Month of Contract:\n{('=')*22}\n{df.sign_date.dt.month.value_counts()}")

# =============================================
### Column `deposit`
# deposit (in 10,000 won)
# =======================
# count    284785.000000
# mean       9862.980750
# std       10813.885617
# min          20.000000
# 25%        1500.000000
# 50%        6500.000000
# 75%       15000.000000
# max      554100.000000
print(df.deposit.describe())


# =============================================
### Column `pay_monthly`
### - Lump-sum lease is not considered
### - pay_monthly (in 10,000 won)
# count    153970.000000
# mean         53.417523
# std          29.123966
# min           1.000000
# 25%          40.000000
# 50%          50.000000
# 75%          60.000000
# max        2123.000000
print(df[df.rent_type=="월세"].pay_monthly.describe())

# =============================================
### Column `unit_size`
# Unit size (m²):
# count    284785.000000
# mean         30.842197
# std          18.669453
# min           3.400000
# 25%          19.930000
# 50%          24.910000
# 75%          32.150002
# max         445.119995
df.unit_size.describe()

# =============================================
### Column `floor`
# count    284785.000000
# mean          7.913798
# std           4.922598
# min           1.000000
# 25%           4.000000
# 50%           7.000000
# 75%          11.000000
# max          65.000000
df.floor.describe()

# =============================================
### Prior to data imputation on 8,476 empty cells
### Column 건축년도
# count    276309.000000
# mean       2010.333116
# std           6.434324
# min        1972.000000
# 25%        2004.000000
# 50%        2013.000000
# 75%        2016.000000
# max        2021.000000
df_backup[df_backup.건축년도.notna()].건축년도.describe()

### Column `yr_built` (after data imputation)
# count    284785.000000
# mean       2010.412490
# std           6.354031
# min        1972.000000
# 25%        2004.000000
# 50%        2013.000000
# 75%        2016.000000
# max        2021.000000
df.yr_built.describe()

## =================================================
## ====================== EDA ======================
### Set Hangeul Font, 한글 폰트 설정
#### - For plotting purposes
#### - matplotlib.rc("font",family=font_name)
import matplotlib as mpl
import matplotlib.font_manager as fm 
import matplotlib.pyplot as plt 
import seaborn as sns 

# sys_font=fm.findSystemFonts()
# custom_font= "NotoSansKR"
# fonts = [f for f in sys_font if font in f]
# print(f"Number of fonts: {len(fonts)}")
# for fnt in fonts:
#   print(fnt)

# ======== D2Coding ========
font_path= r"C:\Users\Jieun\AppData\Local\Microsoft\Windows\Fonts\D2CodingBold-Ver1.3.2-20180524.ttf".replace("\\","/")

#Noto Sans KR
# font_path_noto= r"C:\Users\Jieun\AppData\Local\Microsoft\Windows\Fonts\NotoSansKR-Medium.otf".replace("\\","/") 

font_name= fm.FontProperties(fname=font_path).get_name() # D2Coding

mpl.rc("font",family=font_name)
print(plt.rcParams['font.family'])

# ==================== Plot 1 ====================
### - seaborn.jointplot() for numerical vars
### - unit_size, deposit, rent_type
plt.style.use("bmh")
grid= sns.jointplot(data=df,x="unit_size",y="deposit",hue="rent_type")
# grid.fig.subtitle(f"Deposit w.r.t. Unit_Size\n전용면적(m²) 대비 보증금(만원)")#,kind="scatter",height=9)
# plt.title(f"Deposit w.r.t. Unit_Size\n전용면적(m²) 대비 보증금(만원)")
plt.tight_layout()
plt.savefig("./img/3.1_jointplot.png")
plt.show()

# ==================== Plot 2 ====================
### Distribution of Districts along with sign_year
### - seaborn.displot
# add column: contract year
plt.style.use("bmh")
df["sign_year"]= df.sign_date.dt.year.astype(int)
# fig,ax= plt.subplots(figsize=(22,5))
sns.displot(data=df,x="district",hue="sign_year",multiple="stack",shrink=.8, aspect=18/6) # "shrinking" the bars is helpful to emphasize the categorical nature of the axis # stat="density": when the subsets have unequal numbers of observations, comparing their distributions in terms of counts may not be ideal. One solution is to normalize the counts using the stat parameter
plt.ylabel("number of contracts | 계약 건수")
plt.title(f"Distribution of Districts | 행정구별 계약 건수")
plt.margins()
plt.savefig("./img/3.2_Distribution of Districts_with_sign_year.png")
plt.show()

# ==================== Plot 3 ====================
### - seaborn.boxplot()
### ===================
# print(plt.style.available)
# fivethirtyeight, ggplot, tableau-colorblind10, Solarize_Light2, seaborn-poster, bmh, grayscale, seaborn-talk, seaborn-darkgrid
plt.style.use("grayscale")
plt.figure(figsize=(10,5))
top_districts= (df[df.rent_type=="월세"].district.value_counts().head(8).index.values)
sns.boxplot(x="pay_monthly",y="district",data=\
            df[(df.rent_type=="월세")&(df.district.isin(top_districts))],orient="h")
plt.xlabel("Monthly Rent (in ₩10,000)")
plt.ylabel("District")
plt.tight_layout()
plt.title(f"Rent Distribution in 8 Districts with Most Leases\n임차계약이 가장 빈번한 행정구 8곳의 월세 분포") # 🇰🇷
plt.margins()
plt.grid()
plt.savefig("./img/3.3_boxplot_district_rent.png")
plt.show()


# ======== D2Coding ========
font_path_2= r"C:\Users\Jieun\AppData\Local\Microsoft\Windows\Fonts\D2CodingBold-Ver1.3.2-20180524.ttf".replace("\\","/")
#D2CodingBold-Ver1.3.2-20180524.ttf

font_name= fm.FontProperties(fname=font_path).get_name() # D2Coding

mpl.rc("font",family=font_name)
print(mpl.pyplot.rcParams['font.family'])

# ==================== Plot 4 ====================
### - seaborn.boxplot() for numerical variables
### - unit_size per rent_type
import matplotlib.pyplot as plt 
import seaborn as sns 
plt.style.use('seaborn-bright')
# print(plt.style.available)
# ['Solarize_Light2', 'bmh', 'dark_background', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn-bright', 'seaborn-colorblind', 'seaborn-poster', 'seaborn-ticks', 'tableau-colorblind10']
plt.figure(figsize=(10,5))
sns.boxplot(x="unit_size",y="rent_type",data=df)
plt.xlabel("unit size (m²) | 전용면적(m²)")
plt.ylabel("rent type | 전월세구분")
plt.savefig("./img/3.4_boxplot_unit_size_rent_type.png")
plt.show()

# ==================== Plot 5 ====================
### - seaborn.boxplot() for numerical variables
### - deposit per rent_type, rent_price
import matplotlib.pyplot as plt 
import seaborn as sns 
plt.style.use('bmh')
# print(plt.style.available)
# ['Solarize_Light2', 'bmh', 'dark_background', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn-bright', 'seaborn-colorblind', 'seaborn-poster', 'seaborn-ticks', 'tableau-colorblind10']
plt.figure(figsize=(15,6))
sns.boxplot(x="deposit",y="rent_type",data=df)
plt.xlabel("deposit (in ₩10,000) | 보증금(만원)")
plt.ylabel("rent type | 전월세구분")
plt.savefig("./img/3.5_boxplot_deposit_rent_type_bmh.png")
plt.show()

# ==================== Plot 6 ====================
### - seaborn.boxplot() for numerical variables
### - yr_built per rent_type
import matplotlib.pyplot as plt 
import seaborn as sns 
plt.style.use('tableau-colorblind10')
# print(plt.style.available)
# ['Solarize_Light2', 'bmh', 'dark_background', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn-bright', 'seaborn-colorblind', 'seaborn-poster', 'seaborn-ticks', 'tableau-colorblind10']
plt.figure(figsize=(11,5))
sns.boxplot(x="yr_built",y="rent_type",data=df)
plt.xlabel("yr_built | 건축년도")
plt.ylabel("rent type | 전월세구분")
plt.savefig("./img/3.6_boxplot_yr_built_rent_type.png")
plt.show()

# ==================== Plot 7 ====================
### - seaborn.boxplot() 
### - yr_built across districts
plt.style.use("bmh")
# fig,ax= plt.subplots(figsize=(22,5))
plt.figure(figsize=(13,9))
sns.boxplot(x="yr_built",y="district",data=df)
plt.xlabel("yr_built | 건축년도")
plt.ylabel("district | 행정구")
plt.title(f"Construction Year Across Districts  | 행정구별 건축년도 분포")
plt.margins()
# plt.savefig("./img/3.7_displot_yr_built_district.png")
plt.show()

# ==================== Plot 8 ====================

# ==================== Plot 9 ====================

# ==================== Plot 10 ====================

## =================================================
## ================ Post-processing ================
### Find and remove outliers
# https://towardsdatascience.com/ways-to-detect-and-remove-the-outliers-404d16608dba
# 
# 
#  





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
## FEATURE ENGINEERING
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
#### - `district`: 2*4 groups
#### - `old_div`: 272 categories -> 4*4 groups
#### - `floor`: <=10, >10, >20 -> 3 groups
#### - `yr_built`: 70s,80s,90s,00s,10s -> 5 groups 
#### 🇰🇷
#### > categorical 유형의 컬럼은 숫자형으로 encode함

df["district"]= df.district.astype("category")
df["old_div"]= df.old_div.astype("category")
df["floor"]= df.floor.astype("category")
df["yr_built"]= df.yr_built.astype("category")
df.dtypes

import category_encoders as ce
from timeit import default_timer as timer

### ==========================================
### encode `district`
start_t= timer()

# ce_hash.hashing_trick(df[["old_div"]], N=10, cols=['old_div'])
encoder= ce.hashing.HashingEncoder(cols=["district"],return_df=True)
df_enc= encoder.hashing_trick(df[["district","latitude","longitude"]],N=8)


print("elapsed:",timer()-start_t,"seconds")
df_enc.head(1)

df_copy= pd.concat([df_enc,df],axis=1)
df_copy.head(1)
### ==========================================
### encode `old_div` (272 subdivisions)
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
### encode `yr_built` ()
start_t= timer()
encoder= ce.hashing.HashingEncoder(cols=["yr_built"],return_df=True)
df_enc= encoder.hashing_trick(df[["yr_built","latitude","longitude"]],N=5)
print("elapsed:",timer()-start_t,"seconds")
df_enc.head(1)


### ==========================================
### add hash-encoded columns to df
df_copy= pd.concat(df_enc,df,axis=1)

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
df_lumpsum.drop("pay_monthly",axis=1) 
df_lumpsum.shape, df_monthly.shape

df.head(1)

## ================= Model =================
### - add contract year column
### - build models
### - train and test them
df_copy["sign_yr"]= df_copy.sign_date.dt.year.astype(int)

cols= ['col_0', 'col_1', 'col_2', 'col_3', 'col_4', 'col_5', 'col_6', 'col_7','latitude', 'longitude', 'unit_size', 'sign_yr','deposit', 'floor', 'yr_built'] # target: pay_monthly
X= df_copy[cols]
y= df_copy.pay_monthly

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test= train_test_split(X,y,test_size=.3)

from sklearn.linear_model import LinearRegression,LogisticRegression
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
"""
ConvergenceWarning: lbfgs failed to converge (status=1):
STOP: TOTAL NO. of ITERATIONS REACHED LIMIT.

Increase the number of iterations (max_iter) or scale the data as shown in:
    https://scikit-learn.org/stable/modules/preprocessing.html
Please also refer to the documentation for alternative solver options:
    https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression
  n_iter_i = _check_optimize_result(
"""
models= [LinearRegression(),LogisticRegression(),KNeighborsRegressor(n_neighbors=5),SVR(kernel="linear"),RandomForestRegressor(n_estimators=100,max_features="sqrt")]

model_results_df= pd.DataFrame()
res_dict= {}

from sklearn.metrics import r2_score
from timeit import default_timer as timer
start_t= timer()
for model in models:
    res_dict["Model"]= str(model).split("(")[0]
    model.fit(X_train,y_train)
    res_dict["R_squared (pay_monthly)"]= r2_score(y_test, model.predict(X_test))
    model_results_df= model_results_df.append(res_dict,ignore_index=True)
model_results_df.set_index("Model",inplace=True)
print("Elapsed:",timer()-start_t,"seconds")
plt.style.use("fivethirtyeight")
fig,ax= plt.subplots(ncols=1,figsize=(10,4))
model_results_df["R_squared (pay_monthly)"].plot(ax=ax,kind="bar",title="R² for pay_monthly")
plt.show()
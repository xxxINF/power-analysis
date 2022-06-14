import sys
import pandas as pd

path = sys.argv[1]
data = pd.read_excel(path)

 #数据清洗 逢空值剔除整行
data["缴费金额（元）"].dropna(axis=0)

#统计值计算
payment_amount_mean = data["缴费金额（元）"].mean()
payment_time_mean = data["用户编号"].value_counts().mean()

resoult_data = pd.DataFrame({'平均缴费金额（元）' : [payment_amount_mean], '平均缴费次数' :[payment_time_mean]})

resoult_data.to_csv('居民客户的用电缴费习惯分析 1.csv')

 
 
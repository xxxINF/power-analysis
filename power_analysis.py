import sys
import pandas as pd

path = sys.argv[1]
data = pd.read_excel(path)

 #数据清洗 逢空值剔除整行
data["缴费金额（元）"].dropna(axis=0)

#Statistical Analyzer
class StatisticalAnalyzer:
    def __init__(self,data):
        self.sdt = data
        self.get_statistics()


    def get_statistics(self):
        #adt每个用户的平均缴费金额
        self.adt = self.sdt.groupby(["用户编号"]).mean()
        #tdt每个用户的缴费次数
        self.tdt = self.sdt.drop(["缴费日期", "缴费金额（元）"], axis = 1).groupby("用户编号").value_counts(sort=False).to_frame(name="times")
        #合并adt&tdt
        self.rdt = pd.concat([self.adt, self.tdt], join="inner", axis = 1)
        #payment_amount_mean & payment_time_mean
        self.payment_amount_mean = self.adt["缴费金额（元）"].mean()
        self.payment_time_mean = self.tdt["times"].mean()

        
    def user_payment_habits(self):
        resoult_data = pd.DataFrame({'平均缴费金额（元）' : [self.payment_amount_mean], '平均缴费次数' :[self.payment_time_mean]})
        resoult_data.to_csv('./output/电力客户的用电缴费习惯分析 1.csv')


    def user_classification(self):
        def classify(x):
            #A: heigh value B: pertential C: public D: low value  
            if x["缴费金额（元）"] > self.payment_amount_mean:
                if x["times"] > self.payment_time_mean:
                    return "A"
                else:
                    return "B"
            else:
                if x["times"] > self.payment_time_mean:
                    return "C"
                else:
                    return "D"

            return 0
        self.rdt["type"] = self.rdt[["缴费金额（元）", "times"]].apply(lambda x: classify(x), axis=1)
        self.edt = self.rdt
        self.edt.drop(["缴费金额（元）", "times"], axis=1).to_csv('./output/电力客户的用电缴费习惯分析 2.csv')

    
    def user_value_predict(self):
        self.edt = self.edt.drop(self.edt.index[(self.edt["type"]!='A')], inplace=False).sort_values("缴费金额（元）",ascending=False)
        self.edt[0:5].to_csv('./output/电力客户的用电缴费习惯分析 3.csv')


user = StatisticalAnalyzer(data)
#job1
user.user_payment_habits()  
#job2
user.user_classification()
#job3
user.user_value_predict()






 
 
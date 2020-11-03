import pandas as pd
import numpy as np
import tushare as ts
import datetime
import time
import os
import csv
import warnings
warnings.filterwarnings("ignore")

class Shares(object):
    def Analysis(self, path=None, code=None):
        if (path is None) and (code is None):
            raise ValueError("请确认参数!您传入的参数不正确，path与code参数必须传入其一!")
        elif path is not None:
            code = os.path.basename(path).split(".")[0]
            DetailINFO = pd.read_csv(path)
            DetailINFO.index = DetailINFO.iloc[:, 0]
            DetailINFO = DetailINFO.iloc[:,1:6].sort_index()
        else:
            DetailINFO = ts.get_hist_data(code, '2019-01-01', '2020-12-31')
        DetailINFO.index = pd.to_datetime(DetailINFO.index, format='%Y-%m-%d')
        df1 = DetailINFO
        ndate = len(df1)
        periodHigh = pd.Series(np.zeros(ndate - 8), index = df1.index[8:])
        periodLow = pd.Series(np.zeros(ndate - 8), index=df1.index[8:])
        RSV = pd.Series(np.zeros(ndate - 8), index=df1.index[8:])
        close = df1.close
        high = df1.high
        low = df1.low
        date = close.index.to_series()
        date[date.index.duplicated()]
        for j in range(3, ndate):
            period = date[j-3:j+1]
            i = date[j]
            periodHigh[i] = high[period].max()
            periodLow[i] = low[period].min()
            RSV[i] = 100*(close[i] - periodLow[i]) / (periodHigh[i] - periodLow[i])
            periodHigh.name = 'periodHigh'
            periodLow.name = 'periodLow'
            RSV.name = 'RSV'
        RSV1 = pd.Series([50, 50], index = date[1:3]).append(RSV)
        RSV1.name = 'RSV'
        KValue = pd.Series(0.0, index = RSV1.index)
        KValue[0] = 50
        for i in range(1, len(RSV1)):
            KValue[i] = 2/3*KValue[i-1] + RSV1[i]/3
        KValue.name = 'KValue'
        DValue = pd.Series(0.0, index = RSV1.index)
        DValue[0] = 50
        for i in range(1, len(RSV1)):
            DValue[i] = 2/3*DValue[i-1] + KValue[i]/3
        KValue = KValue[1:]
        DValue.name = 'DValue'
        DValue = DValue[1:]
        date[date.index.duplicated()]
        closedf = close.to_frame()
        KValuedf = KValue.to_frame()
        DValuedf = DValue.to_frame()
        data = pd.DataFrame()
        data['close'] = closedf['close']
        data['k'] = KValuedf['KValue']
        data['d'] = DValuedf['DValue']
        buy_sell = self.buy_sell(data)
        data['Buy'] = buy_sell[0]
        data['Sell'] = buy_sell[1]
        dfresult = data[(pd.notna(data.Buy) | pd.notna(data.Sell))]
        dfresult['newcol'] = dfresult.Sell.shift(-1)
        dfresult = dfresult[(pd.isna(dfresult.Sell))]
        dfresult['pct'] = (dfresult.newcol - dfresult.Buy) / dfresult.Buy
        plus = 0
        minus = 0
        start = 100000
        for i in dfresult['pct'].to_list()[:-1]:
          if i < 0:
            start = start * (1 + i)
            minus += 1
          else :
            start = start * (1 + i)
            plus += 1
          i = 0
        var2 = ((start-100000)/100000)*100
        return (code, start, var2, plus, minus)


    def buy_sell(self, data):
        sigPriceBuy = []
        sigPriceSell = []
        flag = -1
        param = 0
        param2 = 1.15
        for i in range(len(data)):
            if data['k'][i] * param2 > data['d'][i]:
                if flag != 1:
                    sigPriceBuy.append(data['close'][i - param])
                    sigPriceSell.append(np.nan)
                    flag = 1
                else :
                    sigPriceBuy.append(np.nan)
                    sigPriceSell.append(np.nan)
            elif data['k'][i] * param2 < data['d'][i]:
                if flag != 0:
                    sigPriceBuy.append(np.nan)
                    sigPriceSell.append(data['close'][i - param])
                    flag = 0
                else :
                    sigPriceBuy.append(np.nan)
                    sigPriceSell.append(np.nan)
            else :
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        return (sigPriceBuy, sigPriceSell)

    def get_file_list(self, file_path):
        dir_list = os.listdir(file_path)
        if not dir_list:
            return
        else:
            # 注意，这里使用lambda表达式，将文件按照最后修改时间顺序升序排列
            # os.path.getmtime() 函数是获取文件最后修改时间
            # os.path.getctime() 函数是获取文件最后创建时间
            size_list = sorted(dir_list,key=lambda x: os.path.getsize(os.path.join(file_path, x)), reverse = True)
            # print(size_list)
            return size_list

if __name__ == "__main__":
    # 1. 创建文件对象
    f = open('E:\\Project\\Quantitative\\data\\result.csv', 'w', encoding='utf-8',newline='')
    # 2. 基于文件对象构建 csv写入对象
    csv_writer = csv.writer(f)
    # 3. 构建列表头
    csv_writer.writerow(["股票代号", "策略后本金", "收益率", "胜场", "负场"])
    # 设置计算的数量，是按照数据量大小排序过后的
    num = 4100
    # 设置数据文件夹
    path = "E:\\Project\\Quantitative\\data\\Detail\\"

    size_list = Shares().get_file_list(path)
    size_list = size_list[:num]
    start_time = datetime.datetime.now()
    for file_name in size_list:
        try:
            res = Shares().Analysis(path + file_name)
            csv_writer.writerow([res[0], res[1], res[2], res[3], res[4]])
            print(res)
        except:
            print ("解析失败" + file_name)
    end_time = datetime.datetime.now()
    take_up_time = (end_time - start_time).seconds
    # 5. 关闭文件
    f.close()
    print ("任务完成，共耗时:" + str(take_up_time) + "秒!")

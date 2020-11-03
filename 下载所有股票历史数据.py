import tushare as ts

start_date = '2019-01-01'
end_date = '2020-12-31'
class Shares(object):
    def get_all_info(self):
        all_info = ts.get_stock_basics()
        # all_info.to_csv("E:\\Project\\Quantitative\\data\\all_info.csv")
        # print (all_info)
        index_list = all_info.index.to_list()
        return index_list

    def down_load(self, index_list=None):
        if index_list == None:
            index_list = self.get_all_info()
        num = 0
        for index in index_list:
            print ("开始下载第" + str(num)  + "支股票的历史信息，正在下载的股票代码是" + str(index) + "，剩余待下载数量为" + str(4074 - num))
            DetailINFO = ts.get_hist_data(index, start_date, end_date)
            try:
                DetailINFO.to_csv("E:\\Project\\Quantitative\\data\\Detail\\" + index + ".csv")
            except:
                print ("下载异常!")
            num += 1

if __name__ == "__main__":
    index_list = ['002594', '002241', '000858']
    Shares().down_load()
    print ('任务完成!')
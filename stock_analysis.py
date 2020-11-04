# -*- coding: utf-8 -*-
# FROM __future__ import division
import pandas as pd
import numpy as np
import tushare as ts
import datetime
import time
import os
import csv
import pymysql
import warnings
import random
warnings.filterwarnings("ignore")

class Stock_Analysis():
	def get_today_all_info(self):
		all_info = ts.get_today_all()
		time_stamp = int(time.time())
		stock_file = "/project/script/stock/data/stock/" + str(time_stamp) + ".csv"
		# all_info.to_csv("F:\\Project\\Demo\\data\\all_info.csv")
		all_info.to_csv(stock_file)
		for stock in all_info.itertuples():
			code = stock[1]
			name = stock[2]
			changepercent = stock[3]
			trade = stock[4]
			open = stock[5]
			high = stock[6]
			low = stock[7]
			settlement = stock[8]
			volume = stock[9]
			sql = "SELECT count(1) FROM zhijia.stock_today_detail WHERE code = \'" + str(code) + "\' ;"
			cursor.execute(sql)
			results = cursor.fetchone()
			isexist = results[0]
			if isexist == 0:
				sql = "INSERT INTO zhijia.stock_today_detail values(null, " + str(code) + ", \'" + str(name) + "\', " + str(changepercent) + ", " + str(trade) + ", " + str(open) + ", " + str(high) + ", " + str(low) + ", " + str(settlement) + ", " + str(volume) + ", 1, 0, NOW()) ;"
				# print (sql)
				cursor.execute(sql)
			else:
				sql = "UPDATE zhijia.stock_today_detail set changepercent = " + str(changepercent) + ", trade = " + str(trade) + ", open = " + str(open) + ", high = " + str(high) + ", low = " + str(low) + ", settlement = " + str(settlement) + ", volume = " + str(volume) + ", activate = 1, validdate = NOW() WHERE code = \'" + str(code) + "\' ;"
				# print (sql)
				cursor.execute(sql)
		db.commit()
		# sql = "SELECT code FROM zhijia.stock_today_detail order by changepercent desc limit 10 ;"
		sql = "SELECT code FROM zhijia.stock_today_detail where activate = '1' and flag = '1' ;"
		cursor.execute(sql)
		results = cursor.fetchall()
		code_list = []
		for row in results:
			code = row[0]
			code_list.append(code)
		# print ("第一步查询并入《stock_today_detail》表完成！")
		return code_list

	def queryDetail(self, code, start_date=None, end_date=None):
		DetailINFO = ts.get_hist_data(code, start_date, end_date)
		sqlData = DetailINFO.head(1)
		self.insert_history(code, sqlData)
		DetailINFO = DetailINFO.iloc[:,:5].sort_index()
		DetailINFO.index = pd.to_datetime(DetailINFO.index, format='%Y-%m-%d')
		self.Analysis(code, DetailINFO)


	def insert_history(self, code, sqlData):
		record_date = str(sqlData.index.values)[2:-2]
		open = float(sqlData['open'])
		high = float(sqlData['high'])
		close = float(sqlData['close'])
		low = float(sqlData['low'])
		volume = float(sqlData['volume'])
		sql = "INSERT INTO zhijia.stock_history_detail VALUES(null, " + code + " , " + str(open) + ", " + str(high) + ", " + str(close) + ", " + str(low) + ", " + str(volume) + ", \'" + str(record_date) + "\', NOW()) ;"
		# print (sql)
		cursor.execute(sql)
		db.commit()
		# print ("第二步查询并入《stock_history_detail》表完成！")


	def Analysis(self, code, DetailINFO):
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
		# for i, v in RSV1.items():
		# 	print('index: ', i, 'value: ', v)
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
		for tup in data.itertuples():
			index = tup[0]
			k = tup[2]
			d = tup[3]
			j = (3 * k) - (2 * d)
			data.loc[index, 'j'] = j
		detailDF = data.tail(100)
		# for i in data.itertuples():
		# 	print (i)
		# print ("第三步分析数据完成！")
		self.Summary(code, detailDF)

	def Summary(self, code, detailDF):
		# param = random.randint(0, 99)
		# print(param)
		param = -1
		index = detailDF.index[param]
		print (detailDF.iloc[param])
		close = detailDF.iloc[param, 0]
		k = detailDF.iloc[param, 1]
		d = detailDF.iloc[param, 2]
		j = detailDF.iloc[param, 3]
		# 止损指标
		param2 = 1.15
		sql = "SELECT count(1) FROM zhijia.stock_buy_sell WHERE code = \'" + code + "\' ;"
		cursor.execute(sql)
		results = cursor.fetchone()
		isexist = results[0]
		if isexist == 0:
			# sql = "INSERT INTO zhijia.stock_buy_sell values(null, " + str(code) + " , " + str(close) + ", " + str(k) + ", " + str(d) + ", " + str(j) + ", 10000, 0, 0, null);"
			sql = "INSERT INTO zhijia.stock_buy_sell VALUES(null, " + str(code) + ", " + str(k) + ", " + str(d) + ", " + str(j) + ", 0, 0, 10000, 0, -1, NOW()) ;"
			# print (sql)
			cursor.execute(sql)
			db.commit()
		sql = "SELECT flag,money,num FROM zhijia.stock_buy_sell WHERE code = \'" + str(code) + "\' ;"
		cursor.execute(sql)
		results = cursor.fetchone()
		flag = results[0]
		money = results[1]
		num = results[2]
		if k * param2 > d:
			if flag != 1:
				num = float(money) / float(close)
				money = 0
				sql = "UPDATE zhijia.stock_buy_sell set buy = " + str(close) + ", k = " + str(k) + ", d = " + str(d) + ", j = " + str(j) + ", money = " + str(money) + ", num = " + str(num) + ", flag = 1 WHERE code = \'" + code + "\' ;"
				# print (sql)
				print ("到达买入时间")
			else : 
				print ("买入正常无操作")
		elif k * param2 < d:
			if flag != -1:
				money = float(num) * float(close)
				num = 0
				sql = "UPDATE zhijia.stock_buy_sell set sell = " + str(close) + ", k = " + str(k) + ", d = " + str(d) + ", j = " + str(j) + ", money = " + str(money) + ", num = " + str(num) + ", flag = -1 WHERE code = \'" + code + "\' ;"
				# print (sql)
				print ("到达卖出时间")
			else :
				print ("卖出正常无操作")
		else :
			print ("正常无操作")
		cursor.execute(sql)
		db.commit()
		# print("第四步全部完成！")
		
	# 睡眠到第二天执行修改步数的时间
	def get_sleep_time(self):
		# 第二天日期
		tomorrow = datetime.date.today() + datetime.timedelta(days=1)
		# 第二天17点时间戳
		tomorrow_run_time = int(time.mktime(time.strptime(str(tomorrow), '%Y-%m-%d'))) + 61200
		# print(tomorrow_run_time)
		# 当前时间戳
		current_time = int(time.time())
		# print(current_time)
		return tomorrow_run_time - current_time
	
if __name__ == '__main__':
	while 1:
		db = pymysql.connect(host="192.168.146.130", port=63001, user="root", passwd="root", db="zhijia", charset='utf8')
		# db = pymysql.connect(host="192.168.0.115", port=50004, user="root", passwd="root", db="zhijia", charset='utf8')
		cursor = db.cursor()
		DetailINFO = ts.get_hist_data(code = '601318', start='2020-01-01')
		today = str(DetailINFO.head(1).index.values)[2:-2]
		sql = "select count(1) from stock_history_detail where record_date = \'" + str(today) + "\' ;"
		cursor.execute(sql)
		results = cursor.fetchone()
		isexist = results[0]
		if isexist == 0:
			code_list = Stock_Analysis().get_today_all_info()
			print ()
			for code in code_list:
				try:
					print ("============================================================")
					Stock_Analysis().queryDetail(str(code))
				except Exception as ex:
					print (ex)
			Stock_Analysis().queryDetail('300125')
		else:
			print ("该日期==>" + today + "<==已经执行过了，自动跳过!")
		db.commit()
		db.close()
		sleep_time = Stock_Analysis().get_sleep_time()
		print ("当日任务完成，当前作业时间是====>" + str(datetime.datetime.now()) + ",计算出来的睡眠时间是====>" + str(sleep_time))
		time.sleep(sleep_time)


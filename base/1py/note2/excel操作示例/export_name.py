# -*- coding:utf-8 -*-

import os
from openpyxl import load_workbook
from openpyxl import Workbook

source_file = "./usersdata.xlsx"
dst_file = "./names.sql"

def create_sql(s_file,d_file):
	t_wb = load_workbook(s_file)
	t_sheet = t_wb.get_sheet_by_name('Sheet1')
	f = open(d_file,'w',encoding='utf-8')
	i = 1
	#i = 523
	
	while(True):
		if not t_sheet['A%d' % i].value:
			break
		# id = t_sheet['A%d' % i].value		#id
		username = str(t_sheet['A%d' % i].value)		#姓名
		if username:
			sql = "update xx set is_del=1  where name = '%s' and x='221008';" % (username)

		f.write(sql)
		f.write("\n")
		i = i+1
	
	print("脚本生成成功!")
	
	f.close()

def main():
	s_file = source_file
	d_file = dst_file
	
	if not os.path.exists(s_file):
		print("源文件不存在，请检查")
		exit(0)
	create_sql(s_file,d_file)
	
if __name__ == "__main__":
	main()




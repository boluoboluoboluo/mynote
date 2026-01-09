# -*- coding:utf-8 -*-

import os
from openpyxl import load_workbook
from openpyxl import Workbook
import json

source_file = "./s.xlsx"
dst_file = "./d.json"

def create_file(s_file,d_file):
	t_wb = load_workbook(s_file)
	# t_sheet = t_wb.get_sheet_by_name('Sheet1')
	t_sheet = t_wb['Sheet1']


	i = 2
	
	re_list = []
	while(True):
		if not t_sheet['A%d' % i].value:
			break


		tmp_dict = {}
		tmp_dict['good_id'] = str(t_sheet['A%d' % i].value).strip()
		tmp_dict['good_name'] = str(t_sheet['B%d' % i].value).strip()
		tmp_dict['price'] = str(t_sheet['C%d' % i].value)
		tmp_dict['settle_price'] = str(t_sheet['D%d' % i].value).strip()
		tmp_dict['discount'] = str(t_sheet['E%d' % i].value).strip()
		tmp_dict['breakfast_amount'] = str(t_sheet['F%d' % i].value).strip()
		tmp_dict['settle_type'] = str(t_sheet['G%d' % i].value).strip()
		tmp_dict['packge_item_discount'] = ''
		
		re_list.append(tmp_dict)

		i = i+1
	
	with open(d_file,'w',encoding='utf-8') as file_obj:
		json.dump(re_list,file_obj,ensure_ascii=False)
	
	print("生成成功!")
	


def main():
	s_file = source_file
	d_file = dst_file
	
	if not os.path.exists(s_file):
		print("源文件不存在，请检查")
		exit(0)
	create_file(s_file,d_file)
	
if __name__ == "__main__":
	main()




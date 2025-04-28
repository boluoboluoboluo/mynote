# 批量生成sql，用于机构项目的导入
import os
import re
import sys
import hashlib

def main():
	sfile = 's.txt'	#
	dfile = 'd.sql'	#格式化后新增的sql脚本

	if not os.path.exists(sfile):
		print("源文件不存在，请检查")
		exit(0)


	fin = open(sfile,'r')
	fout = open(dfile,'a+')
	for row in fin:
		s = row.strip()

		sql = 'update hwc_firm_appointment a,' \
			'(select appointment_id from hwc_firm_order  where order_sn="' + s + '") o ' \
			' set a.ap_status=1 where a.id in(o.appointment_id);\n';
		
		# sql = 'update hwc_firm_users set password = "'+ e_pass +'" where id='+id+';\n'
		fout.write(sql)
	fin.close()
	fout.close()

	print("生成脚本成功")


if __name__ == '__main__':
	main()
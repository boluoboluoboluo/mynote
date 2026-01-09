import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from datetime import datetime
import os
import subprocess

#功能: 剪辑|合并 mp4视频

# 说明1:需本地安装ffmpeg
# 
# 说明2:
# 剪辑时,生成ts文件
# 合并时,把ts文件合并成mp4文件
# 这样才不会最后生成的视频出现不流畅现象
class vidcut:
	def __init__(self):
		self.root = tk.Tk()
		self.root.title("mp4视频剪辑")
		self.root.geometry("400x300")

		self.cut_filevar = tk.StringVar()		#响应式
		self.merge_filevar = tk.StringVar()

		rowcount=0
		cutfilebtn = tk.Button(self.root,text="请选择视频文件:",command=self.choose_vidfile)
		cutfilebtn.grid(row=rowcount,column=0,padx=(10,0),pady=(10,0),sticky="w")

		cutfileinput = tk.Entry(self.root,textvariable=self.cut_filevar,width=30,state="readonly")
		cutfileinput.config(fg="grey")
		cutfileinput.grid(row=rowcount,column=1,pady=(10,0),sticky="w")

		rowcount += 1
		startlabel = tk.Label(self.root,text="输入初始位置:")
		startlabel.grid(row=rowcount,column=0,padx=(10,0),sticky="w")

		startinput = tk.Entry(self.root)
		startinput.insert(0,"00:00:00")
		startinput.config(fg="grey")
		startinput.grid(row=rowcount,column=1,sticky="w")

		rowcount += 1
		endlabel = tk.Label(self.root,text="输入结束位置:")
		endlabel.grid(row=rowcount,column=0,padx=(10,0),sticky="w")

		endinput = tk.Entry(self.root)
		endinput.insert(0,"00:00:10")
		endinput.config(fg="grey")
		endinput.grid(row=rowcount,column=1,sticky="w")

		rowcount += 1
		cutbtn = tk.Button(self.root,text="剪辑",command=lambda:self.cut_vidfile(self.cut_filevar.get(),startinput.get().strip(),endinput.get().strip()))
		cutbtn.grid(row=rowcount,column=0,padx=(10,0),sticky="w")

		rowcount +=1
		titlelabel = tk.Label(self.root,text="--------------------------------------------------------------------")
		titlelabel.grid(row=rowcount,column=0,columnspan=2,sticky="w")

		rowcount +=1
		mergelabel = tk.Label(self.root,text="输入待合并的视频:")
		mergelabel.grid(row=rowcount,column=0,padx=(10,0),sticky="w")
		mergefilesinput = tk.Entry(self.root,text=self.merge_filevar,width=30)
		mergefilesinput.insert(0,"1.mp4|2.mp4|3.mp4")
		mergefilesinput.config(fg="grey")
		mergefilesinput.grid(row=rowcount,column=1,sticky="w")

		rowcount +=1
		mergebtn = tk.Button(self.root,text="合并为mp4",command=lambda:self.merge_vidfile(self.merge_filevar.get().strip(),"mp4"))
		mergebtn.grid(row=rowcount,column=0,padx=(10,0),sticky="w")

		self.root.mainloop()

	#选择文件
	def choose_vidfile(self):
		print("choose_file..")
		filepath = filedialog.askopenfilename()
		self.cut_filevar.set(filepath)

	#剪辑
	def cut_vidfile(self,cut_filepath,start,end):
		if not cut_filepath:
			messagebox.showerror("","请选择视频文件")
			return
		if not start:
			messagebox.showerror("","请输入初始位置")
			rturn
		if not end:
			messagebox.showerror("","请输入结束位置")
			return

		print("cut file ...")
		print(cut_filepath)

		start_timeobj = datetime.strptime(start,"%H:%M:%S")
		start_seconds = start_timeobj.hour * 3600 + start_timeobj.minute * 60 + start_timeobj.second
		end_timeobj = datetime.strptime(end,"%H:%M:%S")
		end_seconds = end_timeobj.hour * 3600 + end_timeobj.minute * 60 + end_timeobj.second
		cut_seconds = end_seconds - start_seconds

		file_suffix = cut_filepath.split(".")[-1] if "." in cut_filepath else ""
		
		# outfile = "out." + file_suffix
		outfile = "out.mp4"

		if os.path.exists(outfile):
			print(f"输出文件 {outfile} 已存在,请确认")
			messagebox.showerror("",f"输出文件 {outfile} 已存在,请确认")
			return

		command = "ffmpeg -ss " + start + " -i " + cut_filepath + " -t " + str(cut_seconds) + " -c copy " + outfile

		print(command)
		subprocess.run(command)

		messagebox.showinfo("",f"剪辑完成")

	#合并
	def merge_vidfile(self,files_str,suffix):

		outfile = "out.mp4"
		if os.path.exists(outfile):
			print(f"输出文件 {outfile} 已存在,请确认")
			messagebox.showerror("",f"输出文件 {outfile} 已存在,请确认")
			return

		if not files_str:
			messagebox.showerror("","请输入要合并的文件")
			return



		print("merge file ...")
		print(files_str)

		files = files_str.split("|")
		for fname in files:
			if not os.path.exists(fname):
				messagebox.showerror("",f"文件{fname}不存在,请确认")
				return

		# file_suffix = files_str.split("|")[0].split(".")[-1]

		ts_files_str = ""
		for fname in files:
			ts_fname = fname[0:fname.rfind(".")] + ".ts"		#文件名(前缀)
			command = 'ffmpeg -i "' + fname +  '" -c copy "' + ts_fname + '"'		#转ts
			subprocess.run(command)
			ts_files_str += "|"
			ts_files_str += ts_fname
		ts_files_str = ts_files_str[1:]

		command = 'ffmpeg -i "concat:' + ts_files_str +  '" -c copy ' + outfile
		print(command)
		subprocess.run(command)

		#清理ts文件
		for f in ts_files_str.split("|"):
			os.remove(f)
		print("merge done ...")

		messagebox.showinfo("",f"合并完成")

if __name__ == "__main__":
	vidcut()

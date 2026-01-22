import os
from PIL import Image

def compressPic(srcdir,dstdir):
	try:
		for filename in os.listdir(srcdir):
			if not os.path.exists(dstdir):
				os.makedirs(dstdir)

			srcfile = os.path.join(srcdir,filename)
			dstfile = os.path.join(dstdir,filename)
			
			if os.path.isfile(srcfile):
				simg = Image.open(srcfile)
				w,h = simg.size
				print(w,h)
				dimg = simg.resize((int(w/2),int(h/2)),Image.ANTIALIAS)
				dimg.save(dstfile)
				print(dstfile+"compressed succeeded")
				
				
			#如果是文件夹
			if os.path.isdir(srcfile):
				compressPic(srcfile,dstfile)
	except:
		print("something error..")
		
if __name__ == '__main__':
	compressPic('srcdir','dstdir')
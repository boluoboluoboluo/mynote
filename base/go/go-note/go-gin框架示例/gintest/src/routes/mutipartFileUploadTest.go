package main

import(
	"net/http"
	"fmt"
	"github.com/gin-gonic/gin"
)

func main(){
	r := gin.Default()
	//限制上传最大尺寸	（注意：实测并未限制）
	r.MaxMultipartMemory = 8 << 20
	r.POST("/upload",func(c *gin.Context){
		form,err := c.MultipartForm()
		if err != nil {
			c.String(http.StatusBadRequest,fmt.Sprintf("get err %s",err.Error()))
		}
		//获取所有图片
		files := form.File["files"]
		//遍历所有图片
		for _,file := range files {
			//保存
			if err := c.SaveUploadedFile(file,file.Filename); err != nil {
				c.String(http.StatusBadRequest,fmt.Sprintf("upload err %s",err.Error()))
				return
			}

		}
		c.String(200,fmt.Sprintf("upload ok %d files",len(files)))
	})
	
	r.Run(":8003")
}

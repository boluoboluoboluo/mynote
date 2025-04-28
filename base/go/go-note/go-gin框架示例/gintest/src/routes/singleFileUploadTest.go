package main

import(
	"net/http"
	"github.com/gin-gonic/gin"
)

func main(){
	r := gin.Default()
	//限制上传最大尺寸	（注意：实测并未限制）
	r.MaxMultipartMemory = 8 << 20
	r.POST("/upload",func(c *gin.Context){
		file,err := c.FormFile("file")
		if err != nil {
			c.String(500,"上传图片出错")
		}
		// c.JSON(200,gin.H{"message": file.Header})
		c.SaveUploadedFile(file,file.Filename)
		c.String(http.StatusOK,file.Filename)
	})
	
	r.Run(":8003")
}

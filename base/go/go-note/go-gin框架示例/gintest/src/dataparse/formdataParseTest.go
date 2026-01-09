package main

import(
	"net/http"
	"github.com/gin-gonic/gin"
)

//定义接收数据的结构体
type Login struct{
	User string `form:"username" json:"user" uri:"user" binding:"required"`
	Password string `form:"password" json:"password" uri:"password" binding:"required"`
}

func main(){
	r := gin.Default()
	r.POST("/loginForm",func(c *gin.Context){
		var form Login
		//根据请求头中的content-type自动推断
		if err := c.Bind(&form); err != nil {
			c.JSON(http.StatusBadRequest,gin.H{"error":err.Error()})
			return
		}
		//判断用户名密码
		if form.User != "root" || form.Password != "admin" {
			c.JSON(http.StatusBadRequest,gin.H{"status":"304"})
			return
		}
		c.JSON(http.StatusOK,gin.H{"status":"200"})
	})
	r.Run(":8003")
}
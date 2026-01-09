package main

import(
	"net/http"
	"fmt"
	"github.com/gin-gonic/gin"
)

func main(){
	r := gin.Default()
	r.GET("/user",func(c *gin.Context){
		//指定默认值
		//http://localhost:8003/user 才会打印默认值
		name := c.DefaultQuery("name","孙悟空")
		c.String(http.StatusOK,fmt.Sprintf("hello %s",name))
		//访问http://localhost:8003/user?name=猪八戒
		//浏览器显示 hello 猪八戒
	})
	
	r.Run(":8003")
}
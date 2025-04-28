package main

import(
	"net/http"
	"github.com/gin-gonic/gin"
)

func main(){
	//1.创建路由
	r := gin.Default()
	//2.绑定路由规则，执行的函数
	//gin.Context，封装了request和response
	r.GET("/",func(c *gin.Context){
		c.String(http.StatusOK,"hello world!")
	})

	r.POST("/xxxpost",getting)
	r.PUT("/xxxput")

	//3监听端口，默认在8080
	r.Run(":8083")
}

package main

import(
	"github.com/gin-gonic/gin"
	"fmt"
)

func main(){
	r := gin.Default()
	//路由组1，处理get请求
	v1 := r.Group("/v1")
	{
		v1.GET("/login",login)
		v1.GET("/submit",submit)
	}
	v2 := r.Group("/v2")
	{
		v2.POST("/login",login)
		v2.POST("/submit",submit)
	}
	r.Run(":8003")
}
func login(c *gin.Context){
	name := c.DefaultQuery("name","jack")
	c.String(200,fmt.Sprintf("hello %s\n",name))
}
func submit(c *gin.Context){
	name := c.DefaultQuery("name","lily")
	c.String(200,fmt.Sprintf("hello %s\n",name))
}
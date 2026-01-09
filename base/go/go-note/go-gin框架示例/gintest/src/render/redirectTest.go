package main

import (
    "net/http"

    "github.com/gin-gonic/gin"
)

func main() {
    r := gin.Default()
    r.GET("/index", func(c *gin.Context) {
        c.Redirect(http.StatusMovedPermanently, "/login")
    })
	r.GET("/login", func(c *gin.Context) {
        c.String(200,"hello")
    })
    r.Run(":8003")
}
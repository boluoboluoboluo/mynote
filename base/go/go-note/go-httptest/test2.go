package main

import(
	"fmt"
	"net/http"
)

type HelloHandlerStruct struct{
	content string
}

func (handler *HelloHandlerStruct) ServeHTTP(w http.ResponseWriter, r *http.Request){
	fmt.Fprintf(w,handler.content)
}

func main(){
	//第一种方式：
	// http.Handle("/",&HelloHandlerStruct{content:"hello world 2"})
	// http.ListenAndServe(":8003",nil)

	//第二种方式：
	var hd HelloHandlerStruct
	hd.content = "<div style='color:red;'>hello world 2</div>"

	http.Handle("/",&hd)
	http.ListenAndServe(":8003",nil)
}




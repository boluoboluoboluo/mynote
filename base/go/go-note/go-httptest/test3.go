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

	var hd HelloHandlerStruct
	hd.content = "<div style='color:red;'>hello world 3</div>"
	var hd2 HelloHandlerStruct
	hd2.content = "<div style='color:green;'>hello world3</div>"

	mux := http.NewServeMux()

	mux.Handle("/",&hd)
	mux.Handle("/welcome",&hd2)

	http.ListenAndServe(":8003",mux)
}




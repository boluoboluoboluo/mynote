package main 

import(
	"fmt"
	"test2/test"
)

//说明：公共函数以大写字母开始，私有函数以小写字母开头
//调用外部文件的方法和属性时，该属性或方法首字母必须大写


func main(){
	fmt.Println("hello")

	var a test.Struct_A


	fmt.Println(a.A)	//调用a文件的结构体的属性
	fmt.Println(a.Func_b())	//通过a文件调用b文件的方法
}
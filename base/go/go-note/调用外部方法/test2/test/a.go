package test


//说明：公共函数以大写字母开始，私有函数以小写字母开头
//Struct_b为匿名结构，此时Struct_A可以调用Struct_B实现的方法
type Struct_A struct{
	A int
	Struct_B
}

func (sa *Struct_A) Func_a() string{
	return "a文件Func_a方法"
}
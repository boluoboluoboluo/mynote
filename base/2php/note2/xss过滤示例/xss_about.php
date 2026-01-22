	
<?php
	
    //xss过滤
	function clean_xss($data){
         #字符串过滤
        if (! is_array ( $data ))
        {
            $data = trim ( $data );              #字符两边的处理
            $data = str_replace ( array ('"', "\\", "'", "/", "..", "../", "./", "//" ), '', $data );
            $data = strip_tags ( $data );        #从字符串中去除 HTML 和 PHP 标记
            $data = htmlspecialchars ( $data );  #特殊字符转换为HTML实体
            #匹配换空格
            $no = '/%0[0-8bcef]/'; 
            $data = preg_replace ( $no, '', $data );
            $no = '/%1[0-9a-f]/';
            $data = preg_replace ( $no, '', $data );
            $no = '/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]+/S';
            $data = preg_replace ( $no, '', $data );
            return $data;
        }
        #数组过滤
        $arr = array();
        foreach ($data as $k => $v) 
        {
            $temp = clean_xss($v);
            $arr[$k] = $temp;
        }
        return $arr;
     }
<?php
//模块控制器
class test4Controller{


	//解析上传的excel文件代码
    public function upload_excel(){

        $tmp_file = "";
        //处理上传的抢号数据
        if(!empty($_FILES['file_data']['name'])){
            $tmp_file = $_FILES['file_data']['tmp_name'];
            $file_types = explode(".", $_FILES ['file_data']['name']);
            $file_type = $file_types[count($file_types) - 1];
            /*判别是不是.xls文件，判别是不是excel文件*/
            if(strtolower($file_type) != "xlsx"){
                $result["content"] = "不是Excel文件，重新上传";
                $this->showMsg($result);
            }
        }else{
            $result["content"] = "请先上传文件";
             $this->showMsg($result);
        }

        
        include(ROOT_PATH."PHPExcel/PHPExcel.php");
        include(ROOT_PATH."PHPExcel/PHPExcel/IOFactory.php");
        include(ROOT_PATH."PHPExcel/PHPExcel/Reader/Excel5.php");
        $phpExcel = new PHPExcel();
        $phpReader = new PHPExcel_Reader_Excel2007();   //

        $phpExcel = $phpReader->load($tmp_file); // 载入excel文件
        $sheet = $phpExcel->getSheet(0); // 读取第一個工作表
        $highestRow = $sheet->getHighestRow(); // 取得总行数
        $highestColumm = $sheet->getHighestColumn(); // 取得总列数

        /** 循环读取每个单元格的数据 */
        $dataset=array();
        for ($row = 1; $row <= $highestRow; $row++){//行数是以第1行开始
            $tmp_arr = array();
            for ($column = 'A'; $column <= $highestColumm; $column++) {//列数是以A列开始
                array_push($tmp_arr,$sheet->getCell($column.$row)->getValue());
            }
            array_push($dataset,$tmp_arr);

        }
    }


}

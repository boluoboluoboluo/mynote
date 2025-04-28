<?php
//模块控制器
class test4Controller extends appController{

	//**************************************************** excel导出 start *****************************************************
	public function test_export(){
		include(ROOT_PATH."Qiaqia/Vendor/PHPExcel/PHPExcel.php");
	    include(ROOT_PATH."Qiaqia/Vendor/PHPExcel/PHPExcel/IOFactory.php");
	    include(ROOT_PATH."Qiaqia/Vendor/PHPExcel/PHPExcel/Reader/Excel5.php");
		$mulit_arr = array(
		    array('标题1', '标题2', '标题3'),
		    array('a', 'b', 'c'),
		    array('d', 'e', 'f')
		);
		$obpe = new PHPExcel();
		$obpe->setactivesheetindex(0);	//选中sheet
		// 修改sheet名称
    	$obpe->getActiveSheet()->setTitle("1");
		foreach($mulit_arr as $k=>$v){
		    $k = $k+1;
		    /* @func 设置列 */
		    $obpe->getactivesheet()->setcellvalue('A'.$k, $v[0]);
		    $obpe->getactivesheet()->setcellvalue('B'.$k, $v[1]);
		    $obpe->getactivesheet()->setcellvalue('C'.$k, $v[2]);
		}
		//创建一个新的工作空间(sheet)
		$obpe->createSheet();
		$obpe->setactivesheetindex(1);
		// 修改sheet名称
    	$obpe->getActiveSheet()->setTitle("2");
		//写入多行数据
		foreach($mulit_arr as $k=>$v){
		    $k = $k+1;
		    /* @func 设置列 */
		    $obpe->getactivesheet()->setcellvalue('A'.$k, $v[0]);
		    $obpe->getactivesheet()->setcellvalue('B'.$k, $v[1]);
		    $obpe->getactivesheet()->setcellvalue('C'.$k, $v[2]);
		} 
		//写入类容
		$obwrite = PHPExcel_IOFactory::createWriter($obpe, 'Excel5');
		//**导出至浏览器 start**
		header('Content-Type: application/vnd.ms-excel');
	    header('Content-Disposition: attachment;filename='.date('Ymd_His').'.xls');
	    header('Cache-Control: max-age=0');
		//**导出至浏览器 end**
		//保存文件
		// $obwrite->save('mulit_sheet.xls');	//如果不导出浏览器，可直接使用此行
		$obwrite->save("php://output");exit;
	}
	//**************************************************** excel导出 end *****************************************************


}

##### 导出excel

```php
//导出excel，
//phpexcel效率不行时，用此方法
public function exportData($info,$header=array()){
    $name = uniqid();
    if($info){
        $html = "<table>";
        if($header){
            $html .= "<tr>";
            foreach($header as $k=>$v){
                $html .= "<td>".$v."</td>";
            }
            $html .= "</tr>";
        }
        foreach($info as $k=>$v){
            $html .= "<tr>";
            $sre_len = count($v);
            for($i=0;$i<$sre_len;$i++){
            $html .= "<td>".array_shift($v)."</td>";
            }
            $html .= "</tr>";
        }
        $html .= "</table>";
        header('Content-Type: application/vnd.ms-excel');
        header('Content-Disposition: attachment;filename="' . $name . '.xls"');
        header('Cache-Control: max-age=0');
        echo $html;
    }else{
        //die('No Data');
    }
}
```


### js-jquery-ajax上传文件代码

```js
<script>
    //===========================上传报告 start===========================
    $('#report_browse').click(function(){
        $("#report_browse").val("");
        if(typeof FileReader === 'undefined'){
            alert("系统不支持");
            return;
        }
    });

    $("#report_upload").click(function(){	//点击上传
        var _this = $("#report_browse")[0];
        var s_file = _this.files[0];
        if(!s_file){
            alert("请先选择文件");
            return false;
        }

        var sufix = s_file.name.toLowerCase().split('.').splice(-1);		//后缀
        var tsize = (s_file.size/1024).toFixed(1);		//kb  ,保留1位小数
        // console.log(sufix);
        // var reg = /png|jpg|jpeg|bmp|gif|pdf/;
        var reg = /pdf/;	
        if(!reg.test(sufix)){
            alert("不支持的文件类型");
            return false;
        }
        if(tsize > 1024 * 5){
            alert("文件大小不能超过5M");
            return false;
        }

        var formData = new FormData();
        formData.append("file_data",s_file);

        $.ajax({
            type: "POST",
            url: "/admin/other/other_report_upload",
            data: formData,
            contentType: false,
            processData: false,
            mimeType:"multipart/form-data",
            success: function(res){
                var json_res = $.parseJSON(res);	//转成json对象
                if(json_res.error == 0){
                    var file_path = json_res.file_path; 
                    $("input[name='report_url'").val(file_path);
                    $("#upload_msg").html("<font color='green'>上传成功</font>");
                }else{
                    $("#upload_msg").html("<font color='red'>上传失败:"+json_res.content+"</font>");
                }
            },
            error:function(res){
                alert("系统错误");
            }
        });
        return false;
    });
    //===========================上传报告 end===========================
</script>
```


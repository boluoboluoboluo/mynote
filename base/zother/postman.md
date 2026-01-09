在 Postman 软件中，可以方便的查看参数是以什么形式发送的，对应的 Content-Type 是什么。

1. Body 中选择 “raw” ，则对应的Headers中的 “Content-Type” 是 “application/json” ，参数形式是 {"content":"很好"}
2. Body 中选择 “x-www-form-urlencoded” ，则对应的Headers中的 “Content-Type” 是“application/x-www-form-urlencoded” ，参数形式是Key-Value形式。
3. Body 中选择 “form-data” ， 则对应的Headers中的 “Content-Type” 是 “multipart/form-data” ，参数形式是Key-Value。
#### 安装

```sh
#命令
npm install @element-plus/icons
```



#### 全局方式引入

1. man.ts文件注册：

   ```ts
   import elementPlus from 'element-plus'
   import 'element-plus/dist/index.css'
   
   import * as ElIcon from '@element-plus/icons-vue'		//引入图标文件
   
   const app = createApp(App)
   
   for(const [key,component] of Object.entries(ElIcon)){	//注册
   	app.component(key,component)
   }
   
   ```

2. 测试文件代码：

   示例引入加号图标：`<el-icon><Plus/></el-icon>`

   ```html
   <template>
       <el-button type="success">
           <el-icon>
               <Plus/>
           </el-icon>
           添加
       </el-button>
   </template>
   ```



#### 局部引入

测试文件引入加号图标：

```html
<script setup lang="ts">
	import {Plus} from '@element-plus/icons-vue'
</script>
<template>
    <el-button type="success">
        <el-icon>
            <Plus/>
        </el-icon>
        添加
    </el-button>
</template>
```


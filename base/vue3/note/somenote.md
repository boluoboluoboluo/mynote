#### 安装模块，但是报无法找到模块 "xxx" 的声明文件

```ts
//在env.d.ts文件中添加如下代码，如果没有文件，则在根目录新建xx.d.ts文件
declare module "xxx"
```

#### vscode报错：找不到模块vue-router

描述：找不到模块“vue-router”。你的意思是要将 "moduleResolution" 选项设置为 "node"，还是要将别名添加到 "paths" 选项中?

解决方法：将"moduleResolution"选项设置为"node"，这个选项可以在TypeScript的配置文件（tsconfig.json）中进行设置，例如：

```ts
{
  "compilerOptions": {
    "moduleResolution": "node"
  }
}
```

#### vscode禁用vuter

```sh
vscode里插件vuter禁用，更换为=volar
```

#### 驼峰-中划线

```sh
变量中中划线和驼峰大写含义相同
```



#### ts隐式any报错问题

```vue
<template>
    <div class="box" style="padding-top:1rem;">
        <component :is="comps[currentComp]"></component>
    </div>	
</template>

<script setup lang="ts">
   	import {ref} from 'vue'
    import ArticleList from '../components/ArticleList.vue'
    import VideoList from '../components/VideoList.vue'
    import MusicList from '../components/MusicList.vue'
    
    const comps:any = {		//注意：在此处指定any类型
        ArticleList,
        VideoList,
        MusicList,
    }
    const currentComp = ref("VideoList")
</script>
```

#### 禁用恶意调试

```ts
//原理：只有控制台打开时会执行debugger方法，设置F12代开控制台时，页面无限执行debugger，可阻止恶意调试
(() => {
    function block() {
        setInterval(() => {
            debugger;
        }, 50);
    }
    try {
        block();
    } catch (err) {}
})();
```

#### vue3项目打包后405问题

```sh
#问题：打包后，在页面访问后端服务器接口，报错405
#原因：打包后，配置的跨域规则失效

#解决方式：
在后端web服务器配置文件配置反向代理
请参阅nginx反向代理相关笔记（略）
```




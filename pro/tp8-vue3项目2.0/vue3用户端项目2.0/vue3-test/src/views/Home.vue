<template>
	<div style="display:flex;">
		<div class="header"><Header></Header></div>
		<div :class="[dirClass,{mdirhidden:ishidden}]" :style="{height:winHeight}">
			<div class="" style="text-align:center;padding-top:1.5rem;">
				<p><el-link class="bl-fs-20" type="info" :underline="false"  @click="loadComps('ArticleList')">博客</el-link></p>
				<p><el-link class="bl-fs-20" type="info" :underline="false"  @click="loadComps('VideoList')">视频</el-link></p>
				<p><el-link class="bl-fs-20" type="info" :underline="false"  @click="loadComps('MusicList')">音乐</el-link></p>
				<p><el-link class="bl-fs-20" type="info" :underline="false"  @click="loadComps('PicList')">图片</el-link></p>
				<p><el-link class="bl-fs-20" type="info" :underline="false"  @click="loadComps('GameList')">游戏</el-link></p>
			</div>
		</div>
		<div class="bl-fs-14 bl-pt-10" :class="[contentClass]">
			<component :is="comps[currentComp]" :contentData="contentData" :parentMethod="loadComps"></component>
		</div>
	</div>
</template>
<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import {ref} from 'vue'
import Header from '../components/Header.vue'
import { isMobileOrPc } from "../utils/common"
import {api_media_data} from "@/utils/api"
import { ElMessage } from "element-plus"

import ArticleList from '../components/ArticleList.vue'
import VideoList from '../components/VideoList.vue'
import MusicList from '../components/MusicList.vue'
import PicList from '../components/PicList.vue'
import ArticleDetail from '../components/ArticleDetail.vue'
import VideoDetail from '../components/VideoDetail.vue'

let winHeight = (window.innerHeight * 0.05 - 2.5) + "rem";		//浏览器高度,0.05为px和rem比率
// console.log(localStorage.getItem("token"))

//动态挂载的组件
const comps:any = {
	ArticleList,
	VideoList,
	MusicList,
	PicList,
	ArticleDetail,
	VideoDetail,
}
const currentComp = ref("ArticleList")	//初始挂载
const contentData = ref()				//内容数据

//加载组件
async function loadComps(param:any,id?:any){
	let methodName = param 				//约定的api方法
	const data:any = await api_media_data(methodName,id)
	if(data.code == 1){
		currentComp.value = param		//组件
		contentData.value = data.data	//数据
	}else{
		ElMessage.error(data.msg)
	}
}
loadComps("ArticleList")
</script>
<script lang="ts">
const ishidden = ref(false)
const dirClass = ref("pcdir")
const contentClass = ref("pccontent")
if(isMobileOrPc()){		//如果是手机端
	ishidden.value = true
	dirClass.value = "mdir"
	contentClass.value = "mcontent"
}
//切换目录
export function mdir_toggle(){
	ishidden.value = !ishidden.value
}

</script>
<style scoped>
.header {
	width:100%;
	height:2.5rem;
	background-color:#151515;
	border-bottom:0.01rem solid #4a0000;
	position:fixed;
	top:0;
}
.pccontent{
	margin-top:2.5rem;
	width:80%;
}
.mcontent{
	margin-top:2.5rem;
	width:100%;
}
.pcdir{
	margin-top:2.5rem;
	width:20%;
	border-right: 0.01rem solid #4a0000;
}
.mdir{
	position:fixed;
	top:2.5rem;
	z-index: 999;
	width:30%;
	background-color:#151515;
	opacity:0.9;
	border-right: 0.05rem solid #4a0000;
	transition: transform .3s;
	transform: translateX(0);
}
.mdirhidden {
	transform: translateX(-110%);
}
</style>
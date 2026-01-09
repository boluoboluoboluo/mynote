<template>
	<div>
		<div  class="title-box">
			<el-icon class="bl-ml-10" v-if="isMobileOrPc()" @click="mdir_toggle">
				<Operation/>
			</el-icon>
		</div>
		<div class="navbar-box">
			<span v-if="isLogin()">
				<a href="" @click="logout">退出</a>
				<!-- <RouterLink to="/logout">退出</RouterLink> -->
			</span>
			<span v-else>
				<RouterLink to="/login">
					<el-link type="info">登录</el-link>
				</RouterLink>
			</span>
		</div>
	</div>
</template>
<script setup lang="ts">
	import {mdir_toggle} from "@/views/Home.vue"
	import { isMobileOrPc,login_check } from "../utils/common";
	import {useRouter} from 'vue-router'
	import {Fold} from "@element-plus/icons-vue"
	import {Operation} from "@element-plus/icons-vue"

	const router = useRouter()

	// function mdir_toggle(){
	// 	out_mdir_toggle()
	// }
	function isLogin(){
		return login_check()
	}
	function logout(){
		//TODO..后端退出登录代码
		localStorage.removeItem('token')
		router.push('/')
	}
</script>
<style scoped>
.title-box{
	display:inline-block;
	width:30%;
	text-align:left;
}
.navbar-box{
	width:69%;
	display: inline-block;
	text-align: right;
	line-height:2.5rem;
}
</style>

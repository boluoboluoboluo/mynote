<template>
	<div class="box bl-fs-16">
		用户名：<el-input v-model="username" placeholder="请输入" style="width:8rem;"></el-input>
		<br><br>
		密&nbsp;&nbsp;&nbsp;码：<el-input v-model="password" placeholder="请输入" show-password style="width:8rem;"></el-input>
		<br><br>
		<el-button @click="act_login">登录</el-button>
	</div>	
</template>
<script setup lang="ts">
	import {ref} from 'vue'
	import { ElMessage } from "element-plus"
	import {useRouter} from 'vue-router'
	import { userStore } from "@/stores/user"
	import {api_act_login} from "@/utils/api"
	import {md5} from "@/utils/common"

	const router = useRouter()
	const username = ref("")
	const password = ref("")

	//登录
	async function act_login(): Promise<void>{
		if(!username){
			ElMessage.error("用户名不能为空")
			return
		}
		if(!password){
			ElMessage.error("密码不能为空")
			return
		}

		let hash_password =  md5(password.value)
		let login_params = {username:username.value,password:hash_password}
		const data:any = await api_act_login(login_params)
		if(data.code == 1){
			ElMessage.success("success")
			userStore().userInfo = data.data.data
			localStorage.setItem("token",data.data.token)
			router.push('/')
		}else{
			ElMessage.error(data.msg)
		}
	}

</script>
<style scoped>
.box{
	text-align:center;
	margin-top:10rem;
}

</style>

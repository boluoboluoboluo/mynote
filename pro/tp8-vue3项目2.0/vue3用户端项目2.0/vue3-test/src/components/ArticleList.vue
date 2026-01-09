<template>
	<p>>博客</p>
	<div class="bl-pl-20">
		<div v-for="(v) in data.contentData">
			<p>
				<el-link class="bl-fs-20" type="info"  @click="loadComp('ArticleDetail', v.id )">{{ v.title }}</el-link>
				&nbsp;&nbsp;<span style="color:gray;vertical-align:baseline;">[{{ timestampToDate(v.updatetime) }}]</span>
				<br><span class="bl-ml-10" style="color:gray;vertical-align:baseline;">{{ v.desc }}</span>
			</p>
		</div>
	</div>
</template>
<script setup lang="ts">
	import {timestampToDate} from '@/utils/common'
	const data = defineProps(['contentData','parentMethod'])

	function loadComp(param:any,id:any){
		data.parentMethod(param,id)
	}


</script>


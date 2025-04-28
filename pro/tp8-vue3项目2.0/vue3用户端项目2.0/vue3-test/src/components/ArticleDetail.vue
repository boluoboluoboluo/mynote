<template>
	<div>
		<p>>博客</p>
		<div class="bl-pl-20 bl-text-center">
			<span>{{ data.contentData.title }}</span>
		</div>
		<div class="bl-ml-10">
			<span class="bl-ml-10" style="color:gray;">简介：{{ data.contentData.desc }}</span>
		</div>
		<div class="bl-ml-10" v-html="data.contentData.context">
		</div>

		<!-- <div v-for="(v) in data.contentData">
			<p>
				<el-link class="bl-fs-20" type="info"  @click="loadComp('ArticleDetail')">{{ v.title }}</el-link>
				&nbsp;&nbsp;<span style="color:gray;vertical-align:baseline;">[{{ timestampToDate(v.updatetime) }}]</span>
				<br><span class="bl-ml-10" style="color:gray;vertical-align:baseline;">{{ v.desc }}</span>
			</p>
		</div> -->
	</div>
</template>
<script setup lang="ts">
	// import {ref} from 'vue'
	import {timestampToDate} from '@/utils/common'

	const data = defineProps(['contentData','parentMethod'])
	

</script>


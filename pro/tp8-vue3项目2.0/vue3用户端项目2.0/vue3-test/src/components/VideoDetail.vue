<template>
	<div>
		<p>>视频</p>
		
		<div class="bl-ml-10" style="width:50%;margin:auto;">
			<video class="bl-hand" style="width:100%;" controls>
				<source  :src="'api/media/loadVideo?url='+data.contentData.url">
			</video>
			<p>
				<span class="bl-fs-16">{{ data.contentData.title }}</span>
				<br><span style="color:gray;vertical-align:baseline;">[{{ timestampToDate(data.contentData.updatetime) }}]</span>
				<br><span class="" style="color:gray;vertical-align:baseline;">简介：{{ data.contentData.desc }}</span>
			</p>
		</div>
	</div>
</template>
<script setup lang="ts">
	// import {ref} from 'vue'
	import {timestampToDate} from '@/utils/common'

	const data = defineProps(['contentData','parentMethod'])
	

</script>


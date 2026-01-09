<template>
	<p>>视频</p>
	<div class="bl-dis-flex" v-if="isMobileOrPc()">
		
		<div class=""  style="width:30%;" v-for="(v) in data.contentData">
			<div @click="loadComp('VideoDetail', v.id )">
				<video style="width:100%;">
					<source style="" :src="'api/media/loadVideo?url='+[v.url]" type="video/mp4">
				</video>
			</div>
			
		</div>
	</div>
	<div class="bl-dis-flex" v-else>
		
		<div class="" style="width:25%;" v-for="(v) in data.contentData">
			<div class=" bl-hand" @click="loadComp('VideoDetail', v.id )" >
				<video style="width:100%;" >
					<source style="" :src="'api/media/loadVideo?url='+[v.url]" type="video/mp4">
				</video>
			</div>
			<p>
				<el-link class="bl-fs-20" type="info"  @click="loadComp('VideoDetail', v.id )">{{ v.title }}</el-link>
				<br><span style="color:gray;vertical-align:baseline;">[{{ timestampToDate(v.updatetime) }}]</span>
				<br><span class="" style="color:gray;vertical-align:baseline;">{{ v.desc }}</span>
			</p>
		</div>
	</div>
</template>
<script setup lang="ts">
	import {timestampToDate} from '@/utils/common'
	import { isMobileOrPc } from '@/utils/common';

	const data = defineProps(['contentData','parentMethod'])


	function loadComp(param:any,id:any){
		console.log("ddd")
		data.parentMethod(param,id)
		
	}


</script>
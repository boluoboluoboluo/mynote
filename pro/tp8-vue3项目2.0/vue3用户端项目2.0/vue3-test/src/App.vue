
<template>
	<RouterView />
</template>
<script setup lang="ts">
import { isMobileOrPc } from "./utils/common";

var width = window.screen.width;
// 移动端 rem 单位适配
if (isMobileOrPc()) {
  // width * 100 / 750 = width / 7.5
  // 1rem = 100px
//   window.document.getElementsByTagName("html")[0].style.fontSize =
//     width / 4.5 + "px";
}else{
	// window.document.getElementsByTagName("html")[0].style.fontSize = "100px"
}
</script>
<style scoped>

</style>

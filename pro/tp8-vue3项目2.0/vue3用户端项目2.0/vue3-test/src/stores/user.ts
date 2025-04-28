import { ref } from 'vue'
import { defineStore } from 'pinia'

export const userStore = defineStore('user', () => {
	const userInfo = ref({})
	return { userInfo }
})



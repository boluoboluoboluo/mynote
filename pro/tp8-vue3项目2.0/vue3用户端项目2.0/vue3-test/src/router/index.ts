import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import NotFound from '../views/NotFound.vue'
import { login_check } from "../utils/common";
import { stubString } from 'lodash';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/login',
      name: 'login',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/Login.vue')
    },
	{ path: '/:pathMatch(.*)*', name: 'notFound', component: NotFound },
  ]
})

router.beforeEach((to, from, next) =>{

	let reg = RegExp(/^\/me\//)
	if(to.path.match(reg)){
		if(login_check()){
			next()
		}else{
			next('/login')
		}
	}else{
		next()
	}

	// 判断用户是否已经登录
	// if(login_check()) {
	// 	// 登录用户可以访问所有路由
	// 	next()
	// } else {
	// 	// 未登录用户只能访问部分路由
	// 	if (to.path === '/login' || to.path === '/register' || to.path=== '/') {
	// 		next()
	// 	} else {
	// 		next('/login')
	// 	}
	// }
})

export default router

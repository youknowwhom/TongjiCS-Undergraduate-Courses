import { createRouter, createWebHistory } from 'vue-router'
import { ElMessage } from 'element-plus'
import routes from './routers'

const router = createRouter({
  history: createWebHistory(''),
  routes
})

router.beforeEach((to, from, next) => {
  let token = localStorage.getItem('token')
  let role = localStorage.getItem('role')
  if(to.path === '/login' || to.path === '/signup'){
    next()
  }
  else{
    if(!token){
      ElMessage({'message':'您还未登录！', 'type':'error'})
      next('/login')
      return
    }

    let notAllow = true
    to.meta.roles.forEach(element => {
      if(element === role){
        notAllow = false
        next()
        return
      }
    })

    if(notAllow){
      ElMessage({'message':'您的身份不具备访问权限！', 'type':'error'})
      next('/login')
    }
  }
})

export default router
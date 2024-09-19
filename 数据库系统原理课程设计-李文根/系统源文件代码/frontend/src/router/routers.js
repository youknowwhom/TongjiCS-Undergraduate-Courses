export default [
  {
    path:'/',
    redirect:'/login'
  },
  {
    path: '/login',
    name: 'login',
    meta: {
      title: '登录页'
    },
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/signup',
    name: 'signup',
    meta: {
      title: '注册页'
    },
    component: () => import('@/views/Signup.vue')
  },
  {
    path: '/visualize/:id',
    name: 'visualize',
    meta: {
      title: '台风可视化',
      roles: ['regular']
    },
    component: () => import('@/views/Visualize.vue')
  },
  {
    path: '/personal',
    name: 'personal',
    meta: {
      title: '个人中心',
      roles: ['regular']
    },
    component: () => import('@/views/Personal.vue')
  },
  {
    path: '/message',
    name: 'message',
    meta: {
      title: '消息中心',
      roles: ['regular']
    },
    component: () => import('@/views/Message.vue')
  },
  {
    path: '/station',
    name: 'station',
    meta: {
      title: '气象站中心',
      roles: ['station']
    },
    component: () => import('@/views/Station.vue')
  }
]
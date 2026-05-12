const routes = [
  {
    path: '/',
    redirect: '/login',
  },

  {
    path: '/login',
    component: () => import('pages/AuthPage.vue')
  },

  {
    path: '/registration',
    component: () => import('pages/RegPage.vue')
  },

  {
    path: '/equipment',
    component: () => import('layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', component: () => import('pages/EquipmentPage.vue') }
    ]
  },

  {
    path: '/map',
    component: () => import('layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', component: () => import('pages/MapPage.vue') }
    ]
  },

  {
    path: '/users',
    component: () => import('layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', component: () => import('pages/UsersPage.vue') }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes

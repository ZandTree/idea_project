import Vue from 'vue'
import VueRouter from 'vue-router'
import Router from 'vue-router'
// https://stackoverflow.com/questions/62462276 ow-to-solve-avoided-redundant-navigation-to-current-location-error-in-vue
import {getterTypes} from '@/store/modules/auth'
import store from "@/store";

import Activate from '@/views/auth/Activate'
import ConfirmEmail from '@/views/auth/ConfirmEmail'


import Home from "@/views/Home";
import IdeaGeneral from '@/views/IdeaGeneral'
import IdeaSearch from '@/views/IdeaSearch'
import IdeaDetail from '@/views/IdeaDetail'
import IdeaCreate from '@/views/IdeaCreate'
import IdeaEdit from '@/views/IdeaEdit'
import IdeaFilter from '@/views/IdeaFilter'
import IdeasByTagSlug from '@/views/IdeasByTagSlug'
import IdeasByTagName from '@/views/IdeasByTagName'
import CategIdeas from '@/views/CategIdeas'
import PersonalFeed from '@/views/PersonalFeed'
// auth + profile
import Login from '@/views/auth/Login'
import SignUp from "@/views/auth/SignUp";
import PswForgotStart from "@/views/auth/PswForgotStart"
import SetPswReset from '@/views/auth/PswReset'
import SetPswChange from '@/views/auth/ChangePsw'
import PswForgotFailure from "@/views/auth/MsgPswResetFailure"
import ProfileDetail from '@/views/auth/ProfileDetail'
import AccountProfile from '@/views/auth/AccountProfile'
import EditProfile from '@/views/auth/ProfileEdit'
import DeleteAccount from '@/views/auth/DeleteAccount'
import FollowList from '@/views/FollowList'
import NotFound from '@/views/NotFound'
import NoPerms from '@/views/NoPerms'


Vue.use(VueRouter)
// https://stackoverflow.com/questions/62462276 ow-to-solve-avoided-redundant-navigation-to-current-location-error-in-vue
const routerPush = Router.prototype.push
Router.prototype.push = function push(location) {
return routerPush.call(this, location).catch(error => error)
};

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home,
    meta:{
      public:true
    }
  },
  {
    path: "/signup",
    name: "signup",
    component: SignUp,
    meta:{
      public:true
    }
  },
  {
    path: "/login",
    name: "login",
    component: Login,
    meta:{
      public:true
    }
  },
  
  {
    path: "/confirm-email-link/",
    name: "confirmEmail",
    component: ConfirmEmail,
    meta:{
      public:true
    }
  },
  {
    path: "/activate/:uid/:token",
    name: "activate",
    component: Activate,
    props:true,
    meta:{
      public:true
    }

  },
  {
    path: "/reset-password/",
    name: "resetForgotPsw",
    component: PswForgotStart,
    meta:{
      public:true
    }
  },
  {
    path: "/password/reset/confirm/:uid/:token",
    name: "setPswReset",
    component: SetPswReset,
    props:true,
    meta:{
      public:true
    }
  },
  {
    path: "/change-password/",
    name: "passwordChange",
    component: SetPswChange,
    meta:{
      public:false
    }
  },
  {
    path: "/reset-password-failure/",
    name: "resetForgotPswFailure",
    component: PswForgotFailure,
    meta:{
      public:true
    }
  },
  {
    path: '/general-ideas',
    name: 'ideaGeneral',
    component: IdeaGeneral,
    meta:{
      public:true
    }
  },
  {
    path: '/personal-feed/',
    name: 'personalFeed',
    component: PersonalFeed,
    meta:{
      public:false
    }
    
  },
  {
    path: '/idea-detail/:slug',
    name: 'ideaDetail',
    component: IdeaDetail,
    meta:{
      public:true
    }
  },
  {   
    path: '/idea-create',
    name: 'ideaCreate',
    component: IdeaCreate,
    meta:{
      public:false
    }
    
  },
  {   
    path: '/idea-edit/:slug',
    name: 'editIdea', 
    component: IdeaEdit,
    meta:{
      public:false
    }
  },
  
  {
    // to render all ideas for a given tag slug (unique)
    path: '/tags-slug/:slug',
    name: 'ideasBySlug',
    component: IdeasByTagSlug,
    meta:{
      public:true
    }
  },
  {
    // to render all ideas for a given tag name (unique)
    path: '/tags-name/:name',
    name: 'ideasByName',
    component: IdeasByTagName,
    meta:{
      public:true
    }
  },
  {
    // to render all ideas for a given category
    path: '/category-idea/:slug',
    name: 'categ',
    component: CategIdeas,
    meta:{
      public:true
    }
  },
  {
    path: '/idea/search/:term',
    name: 'search',
    component: IdeaSearch,
    meta:{
      public:true
    }
  },
  {
    // path: '/idea/:sort/',
    path: '/idea/filter/:sort/:featured',
    name: 'filter',
    component: IdeaFilter,
    meta:{
      public:true
    }
   
  },
  {
    path: '/profile/:id',
    name: 'profile',
    component: ProfileDetail,
    meta:{
      public:true
    }
  },
  // private profile routes
  {
    path: '/account-profile/:unid',
    name: 'accountProfile',
    component: AccountProfile,
    meta:{
      public:false
    }
  },
  {
    path: '/profile-edit/:unid',
    name: 'editProfile',
    component: EditProfile,
    meta:{
      public:false
    }
    
  },
  {
    path: '/profile-delete',
    name: 'deleteAccount',
    component: DeleteAccount,
    meta:{
      public:false
    }
  },
  {
    path: '/follow-view',
    name: 'followList',
    component: FollowList,
    meta:{
      public:true
    }
  },
  {
   path: '/about',
    name: 'About',
    meta:{
      public:true
    },
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/no-permissions',
    name: 'noPerms',
    component: NoPerms,
    meta:{
      public:true
    }
  },
  {
    path: '*',
    name: 'notFound',
    component: NotFound,
    meta:{
      public:true
    }
  },

]

const router = new VueRouter({
  // base: process.env.BASE_URL,
  mode: 'history',
  routes
})


router.beforeEach((to, from, next) => {

  if (!to.meta?.public && !store.getters[getterTypes.isLoggedIn]) {
    return next({
      name: "login",
      query: { next: to.fullPath },
    });
  }
  next();
});


export default router

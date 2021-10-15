import Vue from 'vue'
import Vuex from 'vuex'
import auth from '@/store/modules/auth'
import profile from '@/store/modules/profile'
import categs from '@/store/modules/categs'
import categsForForm from '@/store/modules/categForm'
import comments from '@/store/modules/comments'
import ideas from '@/store/modules/ideas'
import idea from '@/store/modules/singleIdea'
import ideaCreative from '@/store/modules/ideaCreative'
import ideaEdit from '@/store/modules/ideaEdit'
import follow from '@/store/modules/follow'
import tags from '@/store/modules/tags'


Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {   
    auth,
    categs,
    categsForForm,
    comments,
    idea,
    ideas,
    ideaCreative,
    ideaEdit,
    follow,
    profile,
    tags,

  }
})

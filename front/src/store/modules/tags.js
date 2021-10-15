import fetchTags from '@/api/tags'

export const actionTypes = {
    getTags:'[tags] Get tags',

}

export const mutationTypes = {
    LOADING_TAGS:'[tags] Load tags',
    GET_TAGS_SUCCESS:'[tags] Set list tags',
    GET_TAGS_FAILURE:'[tags] Fail list tags',
    
}
const state ={
    isLoading:false,
    data:null,
    error:null
}
const mutations = {
    [mutationTypes.LOADING_TAGS](state){
        state.isLoading = true
        state.data = null
    },
    [mutationTypes.GET_TAGS_SUCCESS](state,payload){
        state.isLoading = false,
        state.data = payload
    },
    [mutationTypes.GET_TAGS_FAILURE](state,error){
        state.isLoading = false
        state.error = error

    }
}
const actions = {
    async [actionTypes.getTags]({commit}){    
        commit(mutationTypes.LOADING_TAGS);
        try{
          const resp= await fetchTags.getTags()
          if(resp.status === 200){
            commit(mutationTypes.GET_TAGS_SUCCESS,resp.data)
            return resp.data      
            }
          }
          catch(err){
              commit(mutationTypes.GET_TAGS_FAILURE,err)
            
          }
        },
}

export default {
    state,
    actions,
    mutations,
    
    
  }

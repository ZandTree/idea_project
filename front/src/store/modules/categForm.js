import getCateg from '@/api/categs'

export const actionTypes = {    
    getCategsForm:'[categForm] Get categ for form idea'
}

export const mutationTypes = {
    LOADING_CATS_FORM:'[categForm] Load form categs',
    GET_CATS_FORM_SUCCESS:'[categForm] Success fetch categs for categForm',
    GET_CATS_FORM_FAILURE:'[categForm] Fail form categs',
}
const state ={
    isLoading:false,
    data:null,
    error:null
}
const mutations = {
    [mutationTypes.LOADING_CATS_FORM](state){
        state.isLoading = true
        state.data = null
    },
    [mutationTypes.GET_CATS_FORM_SUCCESS](state,payload){
        state.isLoading = false,
        state.data = payload
    },
    [mutationTypes.GET_CATS_FORM_FAILURE](state,error){
        state.isLoading = false
        state.error = error

    }
}
const actions = {
    async [actionTypes.getCategsForm]({commit}){  
        commit(mutationTypes.LOADING_CATS_FORM);  
        try{          
          const resp= await getCateg.getCategForForm()
          if(resp.status === 200){                         
            commit(mutationTypes.GET_CATS_FORM_SUCCESS,resp.data)
            return resp.data
            }
          }
          catch(err){
            commit(mutationTypes.GET_CATS_FORM_FAILURE,err)            
          }
        },
}

export default {
    state,
    actions,
    mutations,
    
    
  }

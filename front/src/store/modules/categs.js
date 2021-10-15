import getCateg from '@/api/categs'


export const actionTypes = {
    getCategs:'[categs] Get categ tree',
   
}

export const mutationTypes = {
    LOADING_CATEGS:'[cats] Load categories',
    GET_CATEGS_SUCCESS:'[cats] Success list categs',
    GET_CATEGS_FAILURE:'[cats] Fail get categs',
    
}
const state ={
    isLoading:false,
    data:null,
    error:null
}
const mutations = {
    [mutationTypes.LOADING_CATEGS](state){
        state.isLoading = true
        state.data = null
    },
    [mutationTypes.GET_CATEGS_SUCCESS](state,payload){
        state.isLoading = false,
        state.data = payload
    },
    [mutationTypes.GET_CATEGS_FAILURE](state,error){
        state.isLoading = false
        state.error = error

    }
}
const actions = {
    async [actionTypes.getCategs]({commit}){    

        commit(mutationTypes.LOADING_CATEGS);  
        try{
          const resp= await getCateg.getCategTree()
          if(resp.status === 200){                         
            commit(mutationTypes.GET_CATEGS_SUCCESS,resp.data)
            return resp.data
            }
          }
          catch(err){
            commit(mutationTypes.GET_CATEGS_FAILURE,err)
            
          }
        },
}

export default {
    state,
    actions,
    mutations,
    
    
  }

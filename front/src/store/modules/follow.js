import followAPI from '@/api/follow'

const state = {
    isLoading:null,
    error:null,
    netWorkErr:null,
    status500:null,
}
export const mutationTypes = {    

    START_UNFOLLOW_LOADING:'[follow] Start unfollow user',
    UNFOLLOW_SUCCESS:'[follow] Unfollow success',
    UNFOLLOW_FAILURE:'[follow] Unfollow failure',

    START_ADD_FOLLOWING:'[follow] Start add following',
    ADD_FOLLOWING_SUCCESS:'[follow] Add following success',
    ADD_FOLLOWING_FAILURE:'[follow]Add following failure',

    NETWORK_PROBELM:'[follow] Network problem',
    STATUS_500:'[follow] Status 500'

} 
export const actionTypes = {
    unFollowUser:'[Follow] Unfollow user',
    addToFollowing:'[Follow] Add to following',
    
}
const mutations = {
    [mutationTypes.START_UNFOLLOW_LOADING](state){
        state.isLoading = true        
    },
    [mutationTypes.UNFOLLOW_SUCCESS](){}, 
    [mutationTypes.UNFOLLOW_FAILURE](state,error){
        // at this point I don't know what errors I'll get
        state.isLoading = false
        state.error=error
    },
    [mutationTypes.NETWORK_PROBELM](state){
        state.netWorkErr = true    
        state.isLoading=false
    },
    [mutationTypes.STATUS_500](state){
        state.status500 = true    
        state.isLoading=false
    },
    [mutationTypes.RESET_NETWORK_PROBELM](state){
        state.netWorkErr = false      
    },
    [mutationTypes.RESET_STATUS_500](state){
        state.status500 = false  
        
    },
    [mutationTypes.START_ADD_FOLLOWING](state){
        state.isLoading = true        
    },
    [mutationTypes.ADD_FOLLOWING_SUCCESS](){}, 
    [mutationTypes.ADD_FOLLOWING_FAILURE](state,error){
        // at this point I don't know what errors I'll get
        state.isLoading = false
        state.error=error
    },
}
const actions = {
    async [actionTypes.unFollowUser]({commit},userId){
        commit(mutationTypes.START_UNFOLLOW_LOADING)         
        try{
          const resp = await followAPI.unFollow(userId)          
          commit(mutationTypes.UNFOLLOW_SUCCESS) 
           return resp
        }
        catch(err){            
            commit(mutationTypes.UNFOLLOW_FAILURE)
            return err
        }
    }, 
    async [actionTypes.addToFollowing]({commit},authorId){
        commit(mutationTypes.START_ADD_FOLLOWING) 
        const servResp = {}        
        try{
          const resp = await followAPI.addToFollowing(authorId)
          commit(mutationTypes.ADD_FOLLOWING_SUCCESS) 
          servResp.status = resp.status
          servResp.data = resp.data          
          return servResp
        }
        catch(err){
            servResp = err
            commit(mutationTypes.ADD_FOLLOWING_FAILURE)
            if(err.response === undefined){
                commit(mutationTypes.NETWORK_PROBELM)
                servResp.servDown = true  
                return servResp
            }
            return servResp
        }
    } 
} 

export default {
    actions,
    state,    
    mutations
    
    
  }

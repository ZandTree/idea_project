import ideaAPI from '@/api/idea'

const state = {
    data:null,
    isLoading:false,
    error:null,
    status403:null    
    
}

export const mutationTypes = {
    SET_IDEA_LOADING:'[single idea] Load idea start',
    GET_IDEA_SUCCESS:'[single idea] Get idea success',
    GET_IDEA_FAILURE:'[single idea] Get idea failure',

    DELETE_IDEA_LOADING:'[single idea] DELETE idea start',
    DELETE_IDEA_SUCCESS:'[single idea] DELETE idea success',
    DELETE_IDEA_FAILURE:'[single idea] DELETE idea failure',
    STATUS_403:'[single idea] status 403 No perms',

    LIKE_START:'[single idea] GIVE like start',
    SET_LIKE_SUCCESS:'[single idea] UPDATE like idea success',
    LIKE_FAILURE:'[single idea] UPDATE like idea failure',

    GET_INITIAL_LIKE_START:'[single idea] GET initial like start',
    GET_INITIAL_LIKE_SUCCESS:'[single idea] GET like idea success',
    GET_INITIAL_LIKE_FAILURE:'[single idea] GET like idea failure',

    RATING_START:'[single idea] GIVE rating start',
    SET_RATING_SUCCESS:'[single idea] SET rating success',
    RATING_FAILURE:'[single idea] RATING idea failure',   
}
export const actionTypes = {
    getIdea:'[single idea] Get one idea',
    deleteIdea:'[single idea] Delete idea',
    handleLike:'[single idea] Handle Like',
    getLikeState:'[single idea] Get initial state of like',
    handleRating:'[single idea] Handle Rating',   
    
}
const mutations = {
    [mutationTypes.SET_IDEA_LOADING](state){
        state.isLoading = true
        // let op: all prev data will be out|=> met een schone lei beginnen
        state.data = null
      },
    [mutationTypes.GET_IDEA_SUCCESS](state,payload){
        state.isLoading = false
        state.data = payload
    }, 
    [mutationTypes.GET_IDEA_FAILURE](state,error){
        // at this point I don't know what errors I'll get
        state.isLoading = false
        state.error=error
    },
    // at this point delete func does not much but nice to have for feature
    [mutationTypes.DELETE_IDEA_LOADING](){},   
    [mutationTypes.DELETE_IDEA_SUCCESS](state){        
        state.data = null
    }, 
    [mutationTypes.DELETE_IDEA_FAILURE](state,err){
        state.isLoading = false
        state.error = err
        state.status403 = true
    },
    [mutationTypes.STATUS_403](state){
        state.isLoading = false       
        state.status403 = true
    },
    [mutationTypes.LIKE_START](state){},
    [mutationTypes.SET_LIKE_SUCCESS](state){},
    [mutationTypes.LIKE_FAILURE](state,err){
        state.error=err
    },
    [mutationTypes.GET_INITIAL_LIKE_START](){},
    [mutationTypes.GET_INITIAL_LIKE_SUCCESS](){},
    [mutationTypes.GET_INITIAL_LIKE_FAILURE](state,err){
        state.error=err
    },
    [mutationTypes.RATING_START](state){},
    [mutationTypes.SET_RATING_SUCCESS](state){},
    [mutationTypes.RATING_FAILURE](state,err){
        state.error=err
    },       
    
}
const actions = {
    async [actionTypes.getIdea]({commit},{slug}){
        commit(mutationTypes.SET_IDEA_LOADING);
        try{
           // let op: you can get resp.data already ( see api) if you want            
           const resp = await ideaAPI.getOneIdea(slug)  
            commit(mutationTypes.GET_IDEA_SUCCESS,resp.data)
            return resp           

        } catch(err){
            console.log("error by getOneIdea request",err)
            // example: incorrect url in request ot dj server
            commit(mutationTypes.GET_IDEA_FAILURE,err)            
            
        }          
    },
    async [actionTypes.deleteIdea]({commit},{slug}){
        
        commit(mutationTypes.SET_IDEA_LOADING);
        try{
           // let op: you can get resp.data already ( see api) if you want            
           const resp = await ideaAPI.deleteIdea(slug) 
            
            commit(mutationTypes.DELETE_IDEA_SUCCESS)                        
            return resp           
        } catch(err){            
            // example: incorrect url in request ot dj server
            commit(mutationTypes.DELETE_IDEA_FAILURE,err)        
            commit(mutationTypes.STATUS_403)  
            return err      
        }          
    },
    // async [actionTypes.register]({commit},creds){
    async [actionTypes.handleLike]({commit},likeInfo){      
        commit(mutationTypes.LIKE_START);        
        const servResp = {}         
        try{
            
            const resp = await ideaAPI.giveLike(likeInfo) 
            commit(mutationTypes.SET_LIKE_SUCCESS);           
            // resp.data = {"like":true/false}
            servResp.status = resp.status
            servResp.data = resp.data 
                               
            return servResp            

        } catch(err){
            commit(mutationTypes.LIKE_FAILURE,err);
            servResp.status = err.response.status
            return servResp     
          
            
        }          
    },
    async [actionTypes.getLikeState]({commit},ideaId){      
        // commit(mutationTypes.GET_INITIAL_LIKE_START);        
        const servResp = {}         
        try{
            const resp = await ideaAPI.getInitialLikeState(ideaId)
            servResp.status = resp.status
            servResp.data = resp.data 
            return servResp

        } catch(err){
            commit(mutationTypes.GET_INITIAL_LIKE_FAILURE,err);
            servResp.status = err.response.status
            return servResp     
          
            
        }          
    },
    async [actionTypes.handleRating]({commit},ratingInfo){      
        commit(mutationTypes.RATING_START); 
           
        try{                  
            const resp = await ideaAPI.giveRating(ratingInfo) 
            commit(mutationTypes.SET_RATING_SUCCESS);           
            // resp.data = {"rating":3}                      
            return resp          

        } catch(err){            
            commit(mutationTypes.RATING_FAILURE,err); 
            
        }          
    },
    
}


export default {
    state,    
    mutations,
    actions
    
  }

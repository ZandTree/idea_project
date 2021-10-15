import ideaAPI from '@/api/idea'

const state = {
    data:null,
    isLoading:false,
    error:null,    
    // pagination          
    count:0,
    prev:'',
    next:'',
    
}

export const mutationTypes = {
    SET_IDEAS_LOADING:'[ideas] Load ideas start',
    GET_IDEAS_SUCCESS:'[ideas] Get ideas success',
    GET_IDEAS_FAILURE:'[ideas] Get ideas failure',
    // GET_TERM_LOOKUP:'[ideas] Get lookUp search',
    SEARCH_IDEAS_LOADING:'[ideas] Search ideas start',
    SEARCH_IDEAS_SUCCESS:'[ideas] Search ideas success',
    SEARCH_IDEAS_FAILURE:'[ideas] search ideas failure',
    SET_COUNT:'[ideas] Set ideas count',
    SET_PREV:'[ideas] Set ideas prev',
    SET_NEXT:'[ideas] Set ideas next',       
       

}
export const actionTypes = {
    getIdeas:'[ideas] Get ideas',
    searchIt:'[ideas] Make search in ideas',
    
}

const actions = {
    async [actionTypes.getIdeas]({commit},{apiUrl}){
        // console.log("store dispatching getIdeas")
        // console.log("api url in store is",apiUrl)
        commit(mutationTypes.SET_IDEAS_LOADING);
        try{
            // instead of apiUrl(str)=> {object, к можно деструктурировать}
           const resp = await ideaAPI.getIdeas(apiUrl)            
            commit(mutationTypes.GET_IDEAS_SUCCESS,resp.data.results)
            commit(mutationTypes.SET_NEXT,resp.data.next)
            commit(mutationTypes.SET_PREV,resp.data.previous)
            commit(mutationTypes.SET_COUNT,resp.data.count)             
            return resp            

        } catch(err){
            commit(mutationTypes.GET_IDEAS_FAILURE)
        }          
    },
    
}
const mutations = {
    [mutationTypes.SET_IDEAS_LOADING](state){
        state.isLoading = true
        // let op: all prev data will be out|=> met een schone lei beginnen
        state.data = null
      },
    [mutationTypes.GET_IDEAS_SUCCESS](state,payload){
        state.isLoading = false
        state.data = payload
    }, 
    [mutationTypes.GET_IDEAS_FAILURE](state,error){
        // at this point I don't know what errors I'll get
        state.isLoading = false
        state.error=error
    },
    [mutationTypes.SET_COUNT](state,count){        
        state.count = count
    },     
    [mutationTypes.SET_PREV](state,prev){        
        state.prev = prev
    },     
    [mutationTypes.SET_NEXT](state,next){        
        state.next = next
    },      
    [mutationTypes.GET_TERM_LOOKUP](state,term){        
        state.lookUp = term
    },      
    
}


export default {
    state,    
    mutations,
    actions
    
  }








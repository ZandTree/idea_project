// function-ty that changes state ( create/edit ideas)
import ideaAPI from '@/api/idea'

const state = {
    data:null,
    isSubmitting:false,
    servErrs:{
        status:null,
        categErr:null,
        featuredErr:null,
        titleErr:null,
        leadTextErr:null,
        mainTextErr:null,
        tagsErr:null,
        thumbnailErr:null,
        nonFieldErrs:null,
        netWorkErr:null,
        status500:null
      },
    
}

export const mutationTypes = {    

    CREATE_IDEA_START:'[creativeIdea] CREATE idea start',
    CREATE_IDEA_SUCCESS:'[creativeIdea idea] CREATE idea success',
    CREATE_IDEA_FAILURE:'[creativeIdea idea] CREATE idea failure',
    // network-problem
    NETWORK_PROBELM:'[CreateIdea idea] NETWORK_PROBELM',
    STATUS_500:'[CreateIdea idea] STATUS 500 SERVER ERROR',
}
export const actionTypes = {
    createIdea:'[creativeIdea] Create idea'    
}
const mutations = {    
    [mutationTypes.CREATE_IDEA_START](){
        state.isSubmitting = true
        state.servErrs = {}
    },   
    [mutationTypes.CREATE_IDEA_SUCCESS](state,idea){   
        state.isSubmitting = false     
        state.data = idea
    }, 
    [mutationTypes.CREATE_IDEA_FAILURE](state){
        state.isSubmitting = false
        
    },
    [mutationTypes.NETWORK_PROBELM](state){
        state.netWorkErr = true    
        state.isSubmitting=false
    },
    [mutationTypes.STATUS_500](state){
        state.err500 = true    
        state.isSubmitting=false
    },    
}
const actions = {    
    async [actionTypes.createIdea]({commit},ideaInput){
        commit(mutationTypes.CREATE_IDEA_START);
        const servResp = {}
        try{
           // let op: you can get resp.data already ( see api) if you want            
           const resp = await ideaAPI.createIdea(ideaInput)             
            commit(mutationTypes.CREATE_IDEA_SUCCESS)  
            servResp.slug = resp.data.slug 
            servResp.status = 201                                
            return servResp           
        } catch(err){            

            if(err.response === undefined){
                commit(mutationTypes.NETWORK_PROBELM)
                servResp.servDown = true  
                return servResp
            }else if(err.response.status === 500) {
                commit(mutationTypes.STATUS_500)                  
                servResp.status = err.response.status                
                return servResp
            } else{     
                servResp.status = err.response.status
                servResp.categErr = err.response.data.categ
                servResp.featuredErr = err.response.data.featured
                servResp.titleErr = err.response.data.title
                servResp.leadTextErr = err.response.data.lead_text
                servResp.mainTextErr = err.response.data.main_text
                servResp.tagsErr = err.response.data.detail||err.response.tags
                servResp.thumbnailErr = err.response.data.thumbnail
                servResp.nonFieldErrs = err.response.data.non_field_errors                
                // example: incorrect url in request ot dj server            
                commit(mutationTypes.CREATE_IDEA_FAILURE)  
                return servResp
                }     
        }          
    },
}


export default {
    state,    
    mutations,
    // getters,
    actions
    
  }

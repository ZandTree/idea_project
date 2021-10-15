import getCommentAPI from '@/api/comments'

export const actionTypes = {
    sendRootComm:'[comments] Send root comment',
    fetchCommentList:'[comments] Get all comments',
    editComm:'[comments] Edit comment',
    deleteComm:'[comments] Delete comment'
   
}

export const mutationTypes = {
    SEND_COMMENT_SUCCESS:'[comm] Sent comm  success',
    SEND_COMMENT_FAILURE:'[comm] Sent comm failure',

    LOADING_COMMENTS_START:'[comm] Load comments start',
    FETCH_COMMENTS_SUCCESS:'[comm] Fetch comments success',
    FETCH_COMMENTS_FAILURE:'[comm] Fetch comments failure',

    EDIT_COMMENT_START:'[comm] Edit comment start',
    EDIT_COMMENT_SUCCESS:'[comm] Edit comment success',
    EDIT_COMMENT_FAILURE:'[comm] Edit comment failure',

    DELETE_COMMENT_START:'[comm] Delete comment start',
    DELETE_COMMENT_SUCCESS:'[comm] Delete comment success',
    DELETE_COMMENT_FAILURE:'[comm] Delete comment failure',

    NETWORK_PROBELM:'[comm] NETWORK_PROBELM',
    STATUS_500:'[comm] STATUS 500 SERVER ERROR',
    
}
const state ={
    isLoading:false,
    data:null,
    error:null,
    flagRerender:false,
    servErrs:{
        status:null,       
        netWorkErr:null,
        status500:null
      },

}  
//const insert = function(arr,index,item){
//    return [
//        ...arr.slice(0,index),
//        item,
//        ...arr.slice(index)
//    ]
//}
const mutations = {
    [mutationTypes.SEND_COMMENT_SUCCESS](state,newComm){
        state.isLoading = false
        state.data.push(newComm)

    },
    [mutationTypes.SEND_COMMENT_FAILURE](state,error){
        state.isLoading = false
        state.error = error
    },
    [mutationTypes.LOADING_COMMENTS_START](state){
        state.isLoading = true        
    },
    [mutationTypes.FETCH_COMMENTS_SUCCESS](state,payload){
        state.isLoading = false
        state.data = payload
    },
    [mutationTypes.FETCH_COMMENTS_FAILURE](state,error){
        state.isLoading = false
        state.error = error
    },
    [mutationTypes.EDIT_COMMENT_START](state){
        state.isLoading = true        
    },
    [mutationTypes.EDIT_COMMENT_SUCCESS](state,editedComm){
        state.isLoading = false        
        state.data.forEach((comm)=>{            
            if(comm.id===editedComm.id){
                comm.body=editedComm.body
                
            }          
        })        
    },
    [mutationTypes.EDIT_COMMENT_FAILURE](state,error){
        state.isLoading = false
        state.error = error
    },
    [mutationTypes.DELETE_COMMENT_START](){},
        
    [mutationTypes.DELETE_COMMENT_SUCCESS](state,commId){
          
        state.data.map((comm)=>{
            if(comm.id===commId){
                comm.author_comment='comment deleted'
                comm.body = 'comment deleted'
                // comm.created_at should be null otherwise wierd effect of filter on string in Comment.vue
                comm.created_at = null
            }
        })
        
    },      
    [mutationTypes.DELETE_COMMENT_FAILURE](state,error){       
        state.error = error
    },
    [mutationTypes.NETWORK_PROBELM](state){
        state.netWorkErr = true  
        state.servErrs.netWorkErr=true 
    },
    [mutationTypes.STATUS_500](state){
        state.err500 = true  
        state.servErrs.status500=true  
    },    
}
const actions = {
    async [actionTypes.sendRootComm]({commit},commentData){ 
        commit(mutationTypes.EDIT_COMMENT_FAILURE,null)
        commit(mutationTypes.SEND_COMMENT_FAILURE,null)
        const servResp = {}        
        try{          
            const resp= await getCommentAPI.sendRootComment(commentData)
            commit(mutationTypes.SEND_COMMENT_SUCCESS,resp.data)
            servResp.status = resp.status
            servResp.data = resp.data
            return servResp
        }catch(err){
            commit(mutationTypes.SEND_COMMENT_FAILURE,err)
            if(err.response ===undefined){
                commit(mutationTypes.NETWORK_PROBELM)
                servResp.servDown = true  
                return servResp  
            }else if(err.response.status===500){
                commit(mutationTypes.STATUS_500)
                servResp.status =err.response.status
                return servResp
            }else{
                
                servResp.status=err.response.status
                servResp.body=err.response.body
                
                return servResp
            }            
        }        
    },    
    async [actionTypes.editComm]({commit},{id,body}){ 
        
        const servResp = {}
        let data = {
            body:body
        }
        
        try{          
        const resp= await getCommentAPI.editComment(id,data)         
        commit(mutationTypes.EDIT_COMMENT_SUCCESS,resp.data)
        servResp.status = resp.status
        servResp.data = resp.data
        return servResp
        
        }catch(err){
            commit(mutationTypes.EDIT_COMMENT_FAILURE,err)
            if(err.response ===undefined){
                commit(mutationTypes.NETWORK_PROBELM)
                servResp.servDown = true  
                return servResp  
            }else if(err.response.status===500){
                commit(mutationTypes.STATUS_500)
                servResp.status =err.response.status
                return servResp
            }else{
                servResp.status=err.response.status
                servResp.body=err.response.body                
                return servResp
            }            
        }        
    },    
    async [actionTypes.fetchCommentList]({commit},ideaSlug){         
        commit(mutationTypes.LOADING_COMMENTS_START);  
        try{          
            const resp= await getCommentAPI.fetchAllComments(ideaSlug) 
            commit(mutationTypes.FETCH_COMMENTS_SUCCESS,resp.data)
            return resp
        }catch(err){
            commit(mutationTypes.FETCH_COMMENTS_FAILURE,err)
        }        
    } ,
    async [actionTypes.deleteComm]({commit},commId) {
        
        const servResp ={}
        try{
            const resp= await getCommentAPI.deleteComment(commId) 
        commit(mutationTypes.DELETE_COMMENT_SUCCESS,commId)
        servResp.status = resp.status        
        return servResp

        }catch(err){
            commit.DELETE_COMMENT_FAILURE(err)
            
            if(err.response ===undefined){
                commit(mutationTypes.NETWORK_PROBELM)
                servResp.servDown = true  
                return servResp  
            }else if(err.response.status===500){
                commit(mutationTypes.STATUS_500)
                servResp.status =err.response.status
                return servResp
            }else{
                servResp.status=err.response.status
                servResp.body=err.response.body
                return servResp
            }       
        }
    }  
}
    

export default {
    state,
    actions,
    mutations,
    
    
  }


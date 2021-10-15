import profileAPI from '@/api/auth'

const state = {
    data:'',
    myprofile:"mio",
    isLoading:false,
    error:null,
    err500:null,
    netWorkErr:null  
     
}
export const actionTypes = {
    retrieveProfile:'[profile] Get profile',
    showPersonalInfo:'[profile] Owner profile',   
    editPersonalInfo:'[profile] Edit personal profile'   
    
}
const actions = {
    
     async [actionTypes.retrieveProfile]({commit},id){
        //retrieve public info
          
        commit(mutationTypes.START_PROFILE_LOADING);
        const servResp={}
        try{
           const resp = await profileAPI.getProfile(id)
            
            commit(mutationTypes.GET_PROFILE_SUCCESS,resp.data)   
            
            servResp.data = resp.data; 
            servResp.status = resp.status                       
            return servResp            

        } catch(err){
            commit(mutationTypes.GET_PROFILE_FAILURE,err)
            if(err.response === undefined){
                servResp.servDown = true
                return servResp                
            }
            servResp.status = err.response.status
            return servResp
        }          
    },
    async [actionTypes.showPersonalInfo]({commit},unid){
    
        commit(mutationTypes.RESET_ERROR)             
        commit(mutationTypes.RESET_NETWORK_PROBELM)
        commit(mutationTypes.RESET_STATUS_500) 
        commit(mutationTypes.START_PROFILE_LOADING);
        const servResp={}
        try{

           const resp = await profileAPI.profileOwnerAction(unid)            
            
            commit(mutationTypes.GET_PROFILE_SUCCESS,resp.data)                        
            servResp.data = resp.data; 
            servResp.status = resp.status                       
            return servResp           

        } catch(err){
            commit(mutationTypes.GET_PROFILE_FAILURE,err)

            if(err.response === undefined){
                commit(mutationTypes.NETWORK_PROBELM),     
                servResp.servDown = true
                return servResp                
            }
            if(err.response ===500){
                commit(mutationTypes.STATUS_500)
            }
            servResp.status = err.response.status
            // STATUS_500:
            console.log("sending servResp tp vue, see status")
            return servResp
            
        }          
    },
    async [actionTypes.editPersonalInfo]({commit},{unid,profileData}){
        commit(mutationTypes.CHANGE_PROFILE_LOADING);
        const servResp = {}
        try{

           const resp = await profileAPI.profileOwnerEdit(unid,profileData)            
            
            commit(mutationTypes.CHANGE_PROFILE_SUCCESS,resp.data)   
            servResp.status = resp.status
            servResp.data = resp.data                     
            return resp            

        } catch(err){
            
            // commit(mutationTypes.CHANGE_PROFILE_FAILURE,err)   
            if(err.response===undefined){
                // commit(mutationTypes.NETWORK_PROBELM)
                servResp.servDown = true 
                return servResp                 
            }else if(err.response.status === 500){
                // commit(mutationTypes. STATUS_500)                
                servResp.status = err.response.status                
                return servResp
            } else{        
                servResp.status = err.response.status
                servResp.imgErr = err.response.data.image
                servResp.bioErr = err.response.data.bio
                servResp.websiteErr = err.response.data.website
                // commit(mutationTypes.CHANGE_PROFILE_FAILURE,err)  
                return servResp
            }              
        }          
    },    

}

export const getterTypes = {
    currentProfile:'[profile] currentProfile',
    
}
export const mutationTypes = {
    START_PROFILE_LOADING:'[profile private] Load profile start',
    GET_PROFILE_SUCCESS:'[profile private] Get profile success',
    GET_PROFILE_FAILURE:'[profile private] Get profile failure',
    
    CHANGE_PROFILE_LOADING:'[profile private] Edit profile start',
    CHANGE_PROFILE_SUCCESS:'[profile private] Edit profile success',
    CHANGE_PROFILE_FAILURE:'[profile private] Edit profile failure',
    NETWORK_PROBELM:'[profile private] NETWORK_PROBELM', 
    STATUS_500:'[profile private] STATUS 500 SERVER ERROR',  
    RESET_NETWORK_PROBELM:'[profile private] RESET NETWORK_PROBELM', 
    RESET_STATUS_500:'[profile private] RESET STATUS 500 SERVER ERROR',  
    RESET_ERROR:'[profile private] RESET GENERAL ERROR'

}

const mutations = {
    [mutationTypes.START_PROFILE_LOADING](state){
        state.isLoading = true
        // let op: all prev data will be out|=> met een schone lei beginnen
        // state.data = null
      },
    [mutationTypes.GET_PROFILE_SUCCESS](state,payload){
        state.isLoading = false
        state.data = payload
        localStorage.setItem("profile",JSON.stringify(payload))
    }, 
    [mutationTypes.GET_PROFILE_FAILURE](state,error){
        // at this point I don't know what errors I'll get
        state.isLoading = false
        state.error=error
        state.data = null
    },
    [mutationTypes.CHANGE_PROFILE_LOADING](state){
        state.isLoading = true
        // let op: all prev data will be out|=> met een schone lei beginnen
        // if state.data = null |=> no data  in case of errors
      },
    [mutationTypes.CHANGE_PROFILE_SUCCESS](state,payload){
        state.isLoading = false
        state.data = payload
    }, 
    [mutationTypes.CHANGE_PROFILE_FAILURE](state,error){
        // at this point I don't know what errors I'll get
        state.isLoading = false
        state.error=error
    },
    [mutationTypes.NETWORK_PROBELM](state){
        state.netWorkErr = true    
        state.isLoding=false
    },
    [mutationTypes.STATUS_500](state){
        state.err500 = true    
        state.isLoading=false
    }, 
    [mutationTypes.RESET_STATUS_500](state){
        state.err500 = false    
        
    }, 
    [mutationTypes.RESET_NETWORK_PROBELM](state){
        state.netWorkErr = false    
        
    }, 
    [mutationTypes.RESET_ERROR](state){
        state.error = false    
        
    }, 
}
const getters = {
    [getterTypes.currentProfile]:state=>{
      return state.data||JSON.parse(localStorage.getItem('profile'))
    }
}    


export default {
    state,    
    mutations,
    actions,
    getters
    
  }

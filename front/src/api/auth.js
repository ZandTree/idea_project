import axios from '@/api/axios'
import simpleAPI from '@/api/plainAxios'

const register = (creds)=>{
    return axios.post('/auth/users/',creds)
}
const activate = (creds)=>{
    return axios.post('/auth/users/activation/',creds)
}
const login = (creds)=>{
    return axios.post('/auth/jwt/create/',creds)
}

// req by Menu mounted
const getUser = ()=>{
    return axios.get('/auth/users/me/')
}

// req to get a new access token each 15 min
const getNewAccessToken = (refreshToken)=>{
    return axios.post('/auth/jwt/refresh/',refreshToken)
}
// link for new psw instead og forgotten
const confirmEmailPswForget = (creds)=>{
    return axios.post('/auth/users/reset_password/',creds)
}
const requestNewPsw = (creds)=>{
    return axios.post('/auth/users/reset_password_confirm/',creds)
}
// link to change current psw 
const requestChangePsw = (creds)=>{
    return axios.post('/auth/users/set_password/',creds)
}

const getProfile = (id)=>{
    // public access profile
    return simpleAPI.get(`/api/v1/profile-info/${id}/`)
}

const profileOwnerAction = (unid)=>{
    // private access to profile section in Menu
    return axios.get(`/api/v1/profile-owner/${unid}/`)
}

const profileOwnerEdit = (unid,profileData)=>{
    // private access to edit profile 
    return axios.patch(`/api/v1/profile-owner/${unid}/`,profileData)
}

const deleteAccount = (unid)=>{    
    return axios.delete(`api/v1/profile-owner/${unid}/`)
}



export default {
    activate,
    confirmEmailPswForget,
    deleteAccount,
    getUser,
    getNewAccessToken,
    getProfile,
    login,
    profileOwnerAction,
    profileOwnerEdit,
    requestNewPsw,
    requestChangePsw,
    register,

    

}    
import axios from '@/api/axios'
import simpleAPI from '@/api/plainAxios'


// simpleAPI: no need of  creds
const getIdeas = (apiUrl)=>{
    return simpleAPI.get(apiUrl)
}
const getOneIdea = (slug)=>{
    return simpleAPI.get(`api/v1/ideas-collection/ideas/${slug}/`)

}


// axios : for requests where creds are needed
const deleteIdea = (slug)=>{
    return axios.delete(`/api/v1/ideas-collection/ideas/${slug}/`)
}
// looks like getOneIdea but it's NOT; get idea before editing
const getIdeaBeforeEdit = (slug)=>{
    return axios.get(`api/v1/ideas-collection/ideas/${slug}/`)
    
}

const createIdea = (ideaInput)=>{
    return axios.post(`/api/v1/ideas-collection/ideas/`,ideaInput)
}

const editIdea = (slug,ideaInput)=>{
    return axios.put(`/api/v1/ideas-collection/ideas/${slug}/`,ideaInput)
}

const getInitialLikeState = (ideaId)=>{
    return axios.get(`/api/v1/ideas-collection/relations/${ideaId}/`)
    
}

const giveLike = (likeInfo)=>{
    return axios.patch(`/api/v1/ideas-collection/relations/${likeInfo.id}/`,likeInfo.like)
    
}
const giveRating = (ratingInfo)=>{
    return axios.patch(`/api/v1/ideas-collection/relations/${ratingInfo.id}/`,ratingInfo.rating)
    
}
export default {    
    getIdeas,
    getOneIdea,
    deleteIdea,
    createIdea,
    editIdea,
    getIdeaBeforeEdit,
    getInitialLikeState,
    giveLike,
    giveRating
    

}    
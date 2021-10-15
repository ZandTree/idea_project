import axios from '@/api/axios'
import simpleAPI from '@/api/plainAxios'

const sendRootComment = (commentData)=>{
    return axios.post('/api/v1/ideas-collection/comments/',commentData)
}

const editComment = (commentId,commentData)=>{
    return axios.patch(`/api/v1/ideas-collection/comments/${commentId}/`,commentData)
}

const deleteComment = (commentId)=>{
    return axios.delete(`/api/v1/ideas-collection/comments/${commentId}/`)
}

const fetchAllComments = (ideaSlug)=>{
    return simpleAPI.get(`/api/v1/idea/comments/${ideaSlug}/`)
}

export default {
    editComment,
    deleteComment,
    fetchAllComments,
    sendRootComment,
}

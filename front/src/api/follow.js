import axios from '@/api/axios'

const unFollow = (userId)=>{
    return axios.post('/api/v1/unfollow/',userId)
}

const addToFollowing = (authorId)=>{    
    return axios.post('/api/v1/add-following/',authorId)
}

export default{
    unFollow,
    addToFollowing
}
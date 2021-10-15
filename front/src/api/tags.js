import simpleAPI from '@/api/plainAxios'

const getTags = ()=>{    
    return simpleAPI.get(`/api/v1/tags/`)
}
const getByTagName = (tagSlug)=>{    
    return simpleAPI.get(`/api/v1/tags-name/${tagSlug}`)
}


export default {    
    getTags,
    getByTagName
    

}    
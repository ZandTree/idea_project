import simpleAPI from '@/api/plainAxios'
  
const getCategTree = ()=>{    

    return simpleAPI.get(`/api/v1/categories/`)
}
const getCategForForm = ()=>{
    return simpleAPI.get('/api/v1/categories-create-idea/')
}
export default {    
    getCategTree,
    getCategForForm
    

}    
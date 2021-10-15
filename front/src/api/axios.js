import axios from 'axios'

//let baseUrl = 'https://www.tanyacoding.nl:443'
let baseUrl = 'http://127.0.0.1:8000'


axios.defaults.baseURL=baseUrl

axios.interceptors.request.use(config=>{
    const token = localStorage.getItem('accessToken')
    const authorizationToken = token? `JWT ${token}`: null
    config.headers.Authorization = authorizationToken
    return config
})




export default axios


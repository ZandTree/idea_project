<template>
   <div class="container">       
        <div class="row">            
            <div class="col col-md-10" >
                <div class='container'>
                    <div class="wrapper">
                        <h1>Verify your Account:</h1>
                        <button @click="goGoogle" class="btn btn-success">                
                            Create account via Google
                        </button>
                        </div>
                        
                    </div> 
            </div>
        </div>
    </div>
</template>
<script>
// import authAPI from '@/api/auth'
import simpleAPI from '@/api/plainAxios'
import {actionTypes} from '@/store/modules/auth'
/*

 https://accounts.google.com/o/oauth2/auth?client_id=320657379112-c4dg445fj0fttecolqtcsudlt1g179l1.apps.googleusercontent.com&redirect_uri=http://localhost:8000/google&state=fWXQvou9GS3lSFVoju4NZQmN3FbaVES2&response_type=code&scope=https://www.googleapis.com/auth/userinfo.email+https://www.googleapis.com/auth/userinfo.profile+openid+openid+email+profile

const registerGoogle = ()=>{
    console.log("api auth prepares url to send ")
    let url = 'http://localhost:8000'
    return simpleAPI.get(`/auth/o/google-oauth2/?redirect_uri=${url}/google`)
}


http://localhost:8000/http:/localhost:8080/google?code=4%2F0AX4XfWjnMZRuKbiCr_be2Re9MNCum6LqwOzqS4ghMSJvaMjPjNxMKZcxVXIP1HMqzuAFmw&scope=email%20profile%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile%20openid&authuser=0&prompt=consent
*/
export default {
    name:'AppGoogle',
    data(){
        return{
            successMsg:"",
            errorMsg:"",  
            
        }
    },
    methods:{        
        goGoogle(){
        console.log("google chosen")
        let url = 'http://localhost:8000'
        simpleAPI.get(`/auth/o/google-oauth2/?redirect_uri=${url}/google`)
        .then((resp)=>{
            console.log("resp is line 34 start:",resp)
            console.dir(resp)
            if(resp.status===200){                
                console.log('more?',resp.data)
                let redirectUrl = resp.data.authorization_url
                console.log("got url from google ",redirectUrl)
                window.location.replace(redirectUrl)             
                      

            }
        })
        .catch(err=>console.log("err line 367",err))
        },
    
    }, 
    
}
</script>
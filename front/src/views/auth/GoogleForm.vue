<template>
    <div class="container">       
        <div class="row">            
            <div class="col col-md-10" >
                <div class='container'>
                    <div class="wrapper">
                        <h2>I am a google form!!!!!!!!!!!!!!!!!!!</h2>
                        <h1>Verify your Account via Google:</h1>
                        <button @click="goToGoogle" class="btn btn-success">                
                            Create account via Google
                        </button>
                        
                        </div>
                        
                    </div> 
                    
            </div>
        </div>
    </div>
</template>
<script>
/*
http://localhost:8000/http:/localhost:8080/google?state=7YILDMmPPbUeA3zvgBawZcYQ0CMA8y9P&code=4%2F0AX4XfWhqYmeJroSHC_UDw1E3GLMgGO42mnpdWsUKIu_A2e7PXfAnbxZtcxFonOBIbzNBSA&scope=email%20profile%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile%20openid&authuser=0&prompt=consent
###########################
http://localhost:8000/http:/localhost:8080/google?code=4%2F0AX4XfWjnMZRuKbiCr_be2Re9MNCum6LqwOzqS4ghMSJvaMjPjNxMKZcxVXIP1HMqzuAFmw&scope=email%20profile%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile%20openid&authuser=0&prompt=consent


*/

import simpleAPI from '@/api/plainAxios'
// import {actionTypes} from '@/store/modules/auth'
export default {
    name:'AppGoogleForm',
    data(){
        return{
            state:null,
            code:null,
            successMsg:"",
            errorMsg:""
        }
    },
    methods:{
        async goToGoogle(state,code){
           console.log("making config and collecting data before POST") 
           if(state&&code&& !localStorage.getItem('accessToken')){
            const config = {
                headers:{
                    'Content-Type':'application/x-www-form-urlencoded'
                }
            }
            const details = {
                'state':state,
                'code':code
            }
            console.log("details:",details)
            console.log("deail keys",Object.keys(details))
            const formBody = Object.keys(details).map(key=> encodeURIComponent(key)+'='+encodeURIComponent(details[key])).join('&')
            console.log("form body is",formBody)
            // console.log("form body keys",Object.keys(formBody))
            try{                
                const resp = await simpleAPI.post(`http://localhost:8000/auth/o/google-oauth2/?${formBody}`,config);
                console.log("resp is",resp)
                if(resp.data.access){
                    console.log("google gives me an access token");
                    this.$store.dispatch(actionTypes.getUser,resp.data.access)
                }
                this.$router.push({name:'home'})
            }catch(err){
                console.log("signing up with google is failed")
                console.log(Object.keys(err))
                console.dir(err)
                console.log('data',err.response.data)
            }
        }            
      }       
    },
    created(){
        let urlParams = new URLSearchParams(window.location.search);
        this.state = urlParams.get('state'); 
        this.code = urlParams.get('code')
        console.log("line 81 state",this.state)
        console.log("line 82 code",this.code)
        this.goToGoogle(this.state,this.code)
    }
}
</script>
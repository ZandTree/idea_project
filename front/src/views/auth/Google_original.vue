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
import authAPI from '@/api/auth'
import {actionTypes} from '@/store/modules/auth'
/*

 https://accounts.google.com/o/oauth2/auth?client_id=320657379112-c4dg445fj0fttecolqtcsudlt1g179l1.apps.googleusercontent.com&redirect_uri=http://localhost:8000/google&state=fWXQvou9GS3lSFVoju4NZQmN3FbaVES2&response_type=code&scope=https://www.googleapis.com/auth/userinfo.email+https://www.googleapis.com/auth/userinfo.profile+openid+openid+email+profile

*/
export default {
    name:'AppGoogle',
    data(){
        return{
            successMsg:"",
            errorMsg:"",
            state:null,
            code:null,
            successMsg:"",
            errorMsg:""
        }
    },
    methods:{
        
      goGoogle(){
      console.log("google chosen")
      this.$store.dispatch(actionTypes.registerGoogle)
      .then((resp)=>{
        console.log("resp is line 34 start:",resp)
        if(resp.status===200){
            console.log("resp status 1st step: 200")
          let redirectUrl = resp.data.authorization_url
          console.log("got url from google ",redirectUrl)
          window.location.replace(redirectUrl)
          console.log("line 45 where is google form? and state -code")
        //   this.$router.push({name:'google-form'})          
            this.goToGoogle()

        }
      })
      .catch(err=>console.log("err line 367",err))
    },
    async goToGoogle(){
            let urlParams = new URLSearchParams(window.location.search);
            let state = urlParams.get('state'); 
            console.log('line 60 state',state)
            let code = urlParams.get('code')
            console.log('line 62 code',code)
            // this.goToGoogle(this.state,this.code)
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
            console.log("details are",details)
            const formBody = Object.keys(details).map(key=> encodeURIComponent(key)+'='+encodeURIComponent(details[key])).join('&')
            console.log("form body is",formBody)
            try{                
                const resp = await authAPI.post(`http://localhost:8000/auth/o/google-oauth2/?${formBody}`,config);
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
    
}
</script>
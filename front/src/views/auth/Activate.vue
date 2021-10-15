<template>
    <div class="container">
        <div class="messages row mb-2">
        <div v-if="errorMsg" class="errorMsg col-md-12">
            Errors: {{errorMsg}}
            <b-icon icon="exclamation-circle-fill" variant="danger"></b-icon>        
        </div>
        <div v-if="successMsg" class="flesh-msg col-md-12">
            <b-icon icon="three-dots" animation="cylon" font-scale="4"></b-icon>  {{successMsg}} 
            <b-icon icon="exclamation-circle-fill" variant="info"></b-icon>
        </div>
        </div>
         <div class="row">            
            <div class="col col-md-10" >
                <div class='container'>
                    <div class="wrapper">
                        <h1>Verify your Account:</h1>
                        <button  @click="activateAccount" class="btn btn-success">                
                            Verify
                        </button>
                        </div>
                        
                    </div> 
            </div>
        </div>
    </div>
</template>
<script>
import {actionTypes} from '@/store/modules/auth'
export default {
    name:'AppActivate',
    data(){
        return{
            successMsg:"",
            errorMsg:""
        }
    },
     methods:{
        activateAccount(){
           let uid= this.$route.params.uid;
           let token = this.$route.params.token; 
            this.$store.dispatch(actionTypes.activate,{
                uid:uid,
                token:token
            })
            .then((resp)=>{
                console.log("activate view got resp",resp)
                if(resp === 204){
                    console.log("email is confirmed");
                    this.successMsg = "You email is confirmed and your account is succesfully created"
                    setTimeout(()=>{
                        this.$router.push({name:"login"});  
                                         
                    },5000)
                     
                }
            }).catch((err)=>{
                this.errorMsg = "Something went wrong.Please contact us to clearify the problem";
                console.log("err",err)
            })            
        }       
    }
}
</script>

<style scoped>


.errorMsg{
    background-color: rgb(236, 187, 195);
    height: 50px;
    
}
</style>
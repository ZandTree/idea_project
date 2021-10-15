<template>
    <div class="container">
        <div class="messages row mb-2 mt-4">
        <div v-if="errorMsg" class="errorMsg col-md-12">
            Error message: {{errorMsg}}
            <b-icon icon="exclamation-circle-fill" variant="danger"></b-icon>        
        </div>      
            
        <div v-if="successMsg" class="successMsg col-md-12 mt-5 mb-3">
            <p>{{successMsg}}</p> 
            <!-- <b-icon icon="exclamation-circle-fill" variant="info"></b-icon> -->
        </div>
        </div>
         <div class="row">            
            <div class="col col-md-10" >
                <div class='container'>
                    <div v-if="isLoading"><app-loader></app-loader></div>
                    <div class="wrapper">
                        <h2>Do you really want to delete your account?</h2>                        
                        <b-form @submit.prevent="requestDeleteAccount">
                            <div class="d-flex justify-content-between">
                            <b-col cols="6">
                            <b-button type="submit" variant="outline-danger">Yes, delete my account</b-button>                            
                            </b-col >              
                            <b-col cols=6>
                                <router-link :to="{ name: 'home' }" class="btn btn-outline-success" 
                                >No</router-link>
                            </b-col>
                               
                            </div>

                            <div class="errMsg" v-if="servErr.currentPsw">
                                
                            </div>
                            <div class="warn" v-if="servErr.currentPsw">
                                <ul>
                                    <li v-for="pswErr in servErr.currentPsw" :key="pswErr.id">
                                        {{pswErr}}
                                    </li>
                                </ul>
                            </div>     

                        

<!-- django server is down -->
<!-- {{servErr}} -->
                        <div v-if="servErr.servDown" class="warn col-md-12 mb-3 mt-5">
                            Error message: {{servDownMsg}}
                            <b-icon icon="exclamation-circle-fill" variant="danger"></b-icon>        
                        </div>  
                        <div class="errorMsg col-md-12 mb-3" v-if="tokenExp">
                        <div class="px-1">{{unauthMsg}}</div>
                        </div>
<!-- buttons group -->
                                          
                     
                </b-form>  
<!--go home!--  -->
               
            </div>                    
          </div> 
        </div>
      </div>
    </div>
</template>
<script>
import {mapState,mapMutations,mapGetters} from 'vuex'

import {actionTypes} from '@/store/modules/auth'
import {getterTypes} from '@/store/modules/auth'
import {mutationTypes} from '@/store/modules/auth'
import AppLoader from '@/components/Loader'
export default {
    name:'AppDeleteAccount',
    components:{         
         AppLoader
    },
    data(){
        return{
            successMsg:"",
            errorMsg:"",
            currentPsw:'',            
            //front-side vars/errors
            //fieldRequired: "This field is required",
            
                       
            // server side err's
            servErr:{servDown:false},
            servDownMsg:'Sorry. Our server"s exper temp problems.Try again a little bit later',            
            tokenExp:false,
            unauthMsg:'Sorry your login session is expired.Please login again',                     
            
        }
    },    
    computed:{
        ...mapState({
            isLoading:state=>state.auth.isLoading,                                                  
           
        }),
        ...mapGetters({
            currentUser:getterTypes.currentUser            
      }),
                
    },
    methods:{
        requestDeleteAccount(){  
            const data = this.currentUser.unid  
            console.log("data line 114: del account",data)   
            this.$store.dispatch(actionTypes.deleteAccount,data)
            .then((resp)=>{
                // also for servErr's
                console.log("in  vue",resp)
                // console.log(Object.keys(resp))
                if(resp.servDown){
                    console.log("dj serv is down, see rr?")
                    this.servErr.servDown = true
                }else if(resp.status === 204){
                    console.log("account deleted, re-directing to home");
                    this.successMsg = "Your account has been deleted"
                    this.$store.commit(mutationTypes.CLEAR_CREDS)
                    console.log("Ls clean")
                    setTimeout(()=>{
                        this.$router.push({name:"home"}); 
                        window.location.reload() 
                                         
                    },1000)
                     
                }else if(resp.status===401){
                    console.log("status 401 unauth-ed",resp.status)                                      
                    this.tokenExp = true                
                   
                }else if(resp.status ===403){
                    console.log("status 403.Forbidden")
                    this.errorMsg = "Permission denied"
                    return
                }else if(resp.status===400){
                    console.log("status 400 calling",resp.status)
                    // let msg = resp.pswErr
                     this.servErr.currentPsw = resp.pswErr                  
                }
            }).catch((err)=>{
                // incorrect psw => page not found 404 !
                console.log(Object.keys(err))
                console.log("final err",err)
                this.errorMsg = "Something went wrong during password change.Please try a little bit later" 
                
            })            
        },
             
    }
}
</script>

<style scoped>
.successMsg{
    background-color: rgb(192, 219, 164);
    height: 50px;
}

.warn {
  background-color: rgb(240, 194, 194);
  padding:3px 10px;
  border-radius: 3px;
  /* height: 50px; */
}
.control-label::after{
    content: " *";
    color: red;
}
.border{
  display: flex;
  margin: 0px;
  border-color: transparent;
}
.border .col-md-10 {
  padding-left:0px;
}
.col-md-10 >input{
    border-color: transparent;
    border-radius: 5px;
}
.link-decor{  
  color:rgb(35, 35, 39);
  text-decoration:none;
}
.link-decor:hover{
  color:rgb(221, 216, 216);
}
/* input .search-txt */
/* .search-txt {
    background: rgba(255,255,255,0.4);
    border: 1px solid rgba(128,128,128,0.4);
    border-radius: 15px;
    outline: none;
    float:left;
    padding: 0 10px;
    color:#000;
    font-size: 20px;
    transition:0.4s;
    line-height: 40px;
    width:200px;
    margin-right: .3rem;
}

.search-txt[type=password] {
  -webkit-transition: background-color .35s ease-in-out;
  transition: background-color .35s ease-in-out;
  -webkit-transition:width .35s ease-in-out;
  transition: width .35s ease-in-out;
}
.search-txt[type=password]:focus {
  width: 250px;
  background-color: rgba(255,255,255,0.6);
  border-color:gray;
} */

</style>
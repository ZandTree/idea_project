<template>
<div>
<header >     
<div>
  <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand href="#" @click="goHome">
      <b-icon-house-door></b-icon-house-door></b-navbar-brand>
      
    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item href="#">
          <router-link :to="{ name: 'home' }" class="link-decor" exact active-class="active">Home</router-link> 
        </b-nav-item>
      <template v-if="isAnonymous">
        <!-- <b-nav-item href="#">Link</b-nav-item>
        <b-nav-item href="#">Anonymous</b-nav-item> -->
        <b-nav-item href="#" >
            <router-link :to="{ name: 'login' }" class="link-decor" active-class="active">Login</router-link>
          </b-nav-item>
        <b-nav-item href="#" >
            <router-link :to="{ name: 'signup' }" class="link-decor" active-class="active">SignUp</router-link>
        </b-nav-item>
        <!-- <b-nav-item href="#" >
            <router-link :to="{ name: 'google' }" class="link-decor" active-class="active"
              >Login via Google</router-link>
        </b-nav-item> -->
      </template>    

      <b-nav-item href="#"><router-link :to="{ name: 'ideaGeneral' }" class="link-decor" active-class="active"
              >Ideas</router-link></b-nav-item>
      </b-navbar-nav>      

      <!-- Right aligned nav items d-flex justify-content-between-->
      <b-navbar-nav class="ml-auto">
        <b-nav-form class="">
          <b-form-input v-model="term" size="sm" class="mr-2 pt-2 top-adjust" placeholder="Search"></b-form-input>
          <b-button @click="doSearch" size="sm" class="" type="submit">Search</b-button>

          <!-- <b-form-input v-model="term" size="sm" class="mr-sm-2" placeholder="Search"></b-form-input> -->
          <!-- <b-button @click="doSearch" size="sm" class="my-2 my-sm-0" type="submit">Search</b-button> -->
        </b-nav-form>       
          <template v-if="isLoggedIn">
              <b-nav-item href="#" >
                <router-link :to="{ name: 'ideaCreate' }" class="link-decor" active-class="active"
                  >New Idea</router-link>
            </b-nav-item>
              <!-- <b-nav-item href="#">IsLoggedIn</b-nav-item>               -->
              <b-nav-item href="#" >
                <a href="#" @click="doSignOut" class="link-decor" >Sign Out</a>
              </b-nav-item> 
              <b-nav-item href="#" >
                <b-icon icon="person-fill"></b-icon>
                <a href="#" class="link-decor" >Welcome, &nbsp;{{currentUser.username}}</a>
              </b-nav-item>
              <b-nav-item-dropdown right>
                <!-- Using 'button-content' slot -->
                  <template #button-content>
                    <b-icon-tools></b-icon-tools>
                  </template>
                  <b-dropdown-item href="#" @click="showProfile">Profile</b-dropdown-item>
                  <b-dropdown-item href="#" @click="changePsw">Change Password</b-dropdown-item>
                  <b-dropdown-item href="#" @click="deleteAccount" class="danger">Delete Account</b-dropdown-item>
                </b-nav-item-dropdown>  
          </template>       
          </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</header>  
 
  <!-- TODO: warning: user should know that his session is (almost)expired -->   
  <app-warning-server-no-responding v-if="servDown" @close="close">
    <template v-slot:header>
        <h3>Warning</h3>
    </template>
      <template v-slot:body>
        <h4>Our serve experiencing temporary problems. Will will fix them as soon as possible</h4>
    </template>    
  </app-warning-server-no-responding>
</div> 
</template>
<script>
import {mapGetters} from 'vuex'
import {mapState} from 'vuex'
import {actionTypes} from '@/store/modules/auth'
import {actionTypes as profileActionTypes} from '@/store/modules/profile'
import {getterTypes} from '@/store/modules/auth'

import AppDeleteAccountConfirmation from '@/components/Modal.vue'
import AppWaringServerNotResponding from '@/components/Modal.vue'


export default {
    name:'Menu',
    components:{
      AppDeleteAccountConfirmation,
      AppWaringServerNotResponding
    },
    data(){
      return {
        term:'',
        makeModalVisible: false,
        makeModalVisible2: false,        
      }
    },
    computed:{
      ...mapGetters({
        currentUser:getterTypes.currentUser,
        isLoggedIn:getterTypes.isLoggedIn,
        isAnonymous:getterTypes.isAnonymous,        
        }),
        ...mapState({           
           
            error:state=>state.auth.error,            
            servDown:state=>state.auth.noRespServer,
            
        }),         
     
    },
    methods:{
      doSignOut(){        
        this.$store.dispatch( actionTypes.signOut)
        window.location.reload()
        
      },
      doSearch(){
        this.$router.push({name:'search',params:{term:this.term}})       
        this.term = ''
      },
      changePsw(){        
        this.$router.push({name:'passwordChange'}) 
        
      },
      showProfile(){        
         const unid = this.currentUser.unid        
         this.$store.dispatch(actionTypes.getUser)
         this.$store.dispatch(profileActionTypes.showPersonalInfo,unid)
        .then((resp)=>{
          if(resp.status===200){            
            this.$router.push({name:'accountProfile',params:{unid}})
          }else if(resp.status===401){
            this.$router.push({name:'login'})
          }else if(resp.status===500){
            alert("Sorry.Something went wrong on the server.Will will fix it as soon as possible.")
            
          }else{            
            this.$router.push({name:'accountProfile',params:{unid}})
          }
        })          
        .catch((err)=>{
          // console.log(err.servDown)
          this.$router.push({name:'accountProfile',params:{unid}})
        })
      },
      deleteAccount(){              
        this.$router.push({name:'deleteAccount'})
      },
      //close modal
      close(){
        this.makeModalVisible = false
        this.$router.push({name:'home'})
      },
      goHome(){
        console.log("going home?")
        this.$router.push({name:'home'})
      }
      
      
    },
    mounted(){
      this.$store.dispatch(actionTypes.getUser)
      .then((resp)=>{              
          if(resp===200){
            console.log(resp) //undefined            
          }else if(resp===401){
            console.log(resp) //undefined
            let refreshToken = localStorage.getItem('refreshToken')
            if(refreshToken){
              const timeNow = Math.ceil(Date.now()/1000)              
              const tokenRefreshPayload = JSON.parse(atob(refreshToken.split('.')[1]));
              const expTerm = tokenRefreshPayload.exp
              if(expTerm>timeNow){                             
                this.$store.dispatch(actionTypes.fetchFreshAccessToken,refreshToken)
                .then((resp)=>{
                  // console.log(resp) 
                  this.$store.dispatch( actionTypes.getUser)                 
                })
                .catch((err=>{
                  console.log(err)
                }))
            }else{
              // refresh token is NOT valid"
              alert("Your session expired,please login again.")
              localStorage.clear()             
            }           

            }
            // if(!refreshToken){
            //   console.log("No refresh tokend")
            // }
          }
          else if(resp===500){
            console.log(resp)
          }
      })
      .catch((err)=>{
        console.log(err)
      })     
      
     }, 
    created(){
     setInterval(()=>{ 
       
       // sending request for a new access token each 30 min
       // 1 min = 60000 millisec 30 min => 18 060 000 millisec( lifespan access token =35 min)      
       let refreshToken = localStorage.getItem('refreshToken')
       if(refreshToken){
            // deel if refresh present
             const now = Math.ceil(Date.now()/1000)
            //  console.log("now is ",now)
             const tokenRefreshPayload = JSON.parse(atob(refreshToken.split('.')[1]));
             const expTerm = tokenRefreshPayload.exp
            //  console.log("exp term: ",expTerm)
             //TODO: warning if time gap aproaches 1 min (60)
             // const oneMinWarning = 60         
            // if refresh valid
            if(expTerm>now){
                // console.log("refresh token present and valid")
                this.$store.dispatch(actionTypes.fetchFreshAccessToken,refreshToken)
                .then((resp)=>{
                  console.log("OK")                  
                })
                .catch((err=>{
                  console.log(err)
                }))
            }
            else{
              // if refresh is NOT valid => call mutation to clear LS and     
              //alert("your session expired, login again,please")
               this.$store.commit(mutationTypes.CLEAR_CREDS)      
              

            }            
            
        }
         // deel refresh NOT present 
      //  else{
      //    console.log("refresh token NOT found")
      //  }
        
       }, 1800000 );
      
      
    }
}
</script>

<style scoped>

.menu-nav{
    background-color: bisque;
}
.bg-info-2{
  background-color: brown;
  color:white;
}
.link-decor{
  color:white;
  text-decoration:none;
}
.link-decor:hover{
  color:rgb(221, 216, 216);
}
.active{
  background-color: rgb(245, 239, 239);
  color:black;
  padding:5px 10px;
  border: 1px solid white;
  border-radius: 3px;
}
.dropdowm-item .danger{
  color:red;
  background-color: burlywood;
}
/* input search form */
.top-adjust{
  margin-top:20px;
  padding-top:16px;
  margin-bottom:20px;
}
</style>

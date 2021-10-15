<template>
    <div class="container">
      <div class="flash-msg"></div>
        <div class="row mx-auto  my-5 main-login">            
            <div class="col col-md-10 col-sm-6 py-3" > 
              <b-form @submit.prevent="passwordForgotten"> 
<!-- email  -->
                <b-form-group
                  id="input-group-1"
                  label="Email"
                  label-for="input-1"                  
                >               
                  <b-form-input
                    id="input-1"
                    v-model.trim="email"
                    type="email"
                    placeholder="Enter email"
                    :class="{ 'is-invalid warning': this.$v.email.$error }"
                    @blur="$v.email.$touch()"           
                  ></b-form-input>                                            
<!-- front-side errors email-->            
                <b-form-invalid-feedback v-if="emailRequired" 
                  >{{ fieldRequired }}
                </b-form-invalid-feedback>
                <b-form-invalid-feedback v-if="inValidEmail" 
                  >This field should be a valid email</b-form-invalid-feedback>
            </b-form-group>                  
<!-- server errors: email errors:email doesn't exist -->
                <div class="warn mb-1" v-if="emailErr">
                  <ul>
                    <li v-for="err in emailErr" :key="err.id">
                      {{err}}
                    </li>
                  </ul>
                </div>
<!-- server errors: non-field errors -->
                <div class="warn mb-1" v-if="nonFieldErr">
                  <ul>
                    <li v-for="err in nonFieldErr" :key="err.id">
                      {{err}}
                    </li>
                  </ul>
                </div>
                <!-- django server is down -->
                <div class="warn mb-3" v-if="netWorkErr">
                  <div class="px-1">Sorry. Our server has temporary problems.Please try to login later</div>
                </div>
                <div class="warn mb-3" v-if="unAuthorized">
                  <div>{{unAuthorized}}</div>
                </div>
                
                <div class="warn mb-3" v-if="personDoesNotExist">
                  <div>Something went wrong. Please check your email address</div>
                </div>
                <div class="warn mb-3" v-if="finalErr">
                  <div>Something went wrong during reset password.</div>
                </div>
                <div class="flesh-msg mb-3" v-if="successMsg">
                  <div>{{successMsg}}</div>
                </div>
                <b-row >
                  <b-col cols="6">
                    <b-button type="submit" 
                    :disabled="formInValid" variant="success">Submit</b-button>
                  </b-col >       
                </b-row>        
            </b-form> 
            <p class="mt-3">
            <router-link :to="{name:'home'}">Home</router-link>
          </p>         
      </div>
    </div>
  </div>         
</template>

<script>

import {required, email}  from "vuelidate/lib/validators";
import {actionTypes} from '@/store/modules/auth'
export default {
    name:'AppPswForgot',
     data(){
      return {
        
        email:'',
        psw:'',        
        status:'',       
        emailErr:null,        
        nonFieldErr:null,
        netWorkErr:null,
        unAuthorized:null,
        finalErr:false,
        personDoesNotExist:false,
        successMsg:'',
        // front valid 
        fieldRequired: "This field is required",        
      } 
    },
     validations: {
    email: { required, email },
    
    },
    computed:{
      formInValid() {
      return this.$v.$invalid;
    },    
    emailRequired() {
      return this.$v.email.$dirty && !this.$v.email.required;
    },
    inValidEmail() {
      return this.$v.email.$dirty && !this.$v.email.email;
    },
    },
     methods:{
        passwordForgotten(){
         let data={email:this.email}
        //  console.log("type of data: ",typeof data.email)
        //  console.log("data: ",data.email)
         // request link psw reset based on email
        this.$store.dispatch(actionTypes.confirmEmailForgottenPsw,data)
          .then((resp)=>{  
            // console.log("got resp from store:",resp)
            if(resp.status===204){
              console.log("Login comp and status",resp.status)
              // re-direct to page with msg: check your email
              this.$router.push({ name: "confirmEmail" });
            }else if(resp&&resp.status===400){
              console.log("status 400 ")
              this.personDoesNotExist = true
            }
            else{
              console.log("status rest != 204,!=400")
            }
          }).catch((err)=>{   
           //user banned?        
             console.log("catch in psw forgotten component ERROR",err.message)
            //  console.dir(err)
             this.$router.push({ name: "resetForgotPswFailure"});
             //alert("A server/network error occured.Sorry about this - we will get it fixed shortly. ");
                          
          })          
              
     }  
    }
}
</script>
<style scoped>
.warn {
  background-color: rgb(240, 194, 194);
  border-radius: 3px;
}
.warn ul li{
  list-style-type:none;
}
.flesh-msg{
  background-color: darkgoldenrod;
}
.main-login {

  padding:2rem;
  background-color: blanchedalmond;
  box-shadow: 0 0 10px 10px rgba(0,0,0,.05);
  border-radius: 0.5rem;
} 
.point-it{
  cursor: pointer;
  background-color: white;
  margin-left: 0px;
  text-align: center;
}
.border{
  display: flex;
  margin: 0px;
  
}
.border .col-md-10 {
  padding-left:0px;
}


</style>
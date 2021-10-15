<template>
    <div class="container">
        <div class="messages row mb-2 mt-4">
        <div v-if="errorMsg" class="errorMsg col-md-12">
            Error message: {{errorMsg}}
            <b-icon icon="exclamation-circle-fill" variant="danger"></b-icon>        
        </div>      
            
        <div v-if="successMsg" class="successMsg col-md-12">
            <b-icon icon="three-dots" animation="cylon" font-scale="4"></b-icon>  {{successMsg}} 
            <b-icon icon="exclamation-circle-fill" variant="info"></b-icon>
        </div>
        </div>
         <div class="row">            
            <div class="col col-md-10" >
                <div class='container'>
                    <div v-if="isLoading"><app-loader></app-loader></div>
                    <div class="wrapper">
                        <h1>Change you password:</h1>                        
                        <b-form @submit.prevent="requestNewPassword">
<!-- current password -->
                <div class="d-flex justify-content-between">
                                            <div class="control-label">Current Password</div>
                                            <div>Show Password</div>
                            </div> 
                            <b-form-group id="input-group-2" class="required psw-show">          
                                <label id="input-group-2" class="label-psw">Current password</label> 
                               
                                    <b-form-input
                                        id="input-2"
                                        class="search-text password"
                                        
                                        v-model.trim="currentPsw"
                                        autocomplete="off"
                                        :type="showPassword ? 'text' : 'password'"
                                        @blur="$v.currentPsw.$touch()"
                                        :class="{ 'is-invalid warning': this.$v.currentPsw.$error }"          
                                    ></b-form-input>
                                    <button class="unmask" type="button" title="Mask/Unmask password"
              @click="toggleShowPws" >Unmask</button>
                                    
                                   
<!--psw front side errors  -->
                           <b-form-invalid-feedback v-if="currentPswRequired" 
                            >{{ fieldRequired }}
                            </b-form-invalid-feedback>    
<!--psw serv side errors  -->
                            <div class="errMsg" v-if="servErr.currentPsw">
                                
                            </div>
                            <div class="warn" v-if="servErr.currentPsw">
                                <ul>
                                    <li v-for="pswErr in servErr.currentPsw" :key="pswErr.id">
                                        {{pswErr}}
                                    </li>
                                </ul>
                            </div>     

                        </b-form-group>
<!-- new psw -->
<div class="d-flex justify-content-between">
                                            <div class="control-label">New Password</div>
                                            <div>Show Password</div>
                            </div> 
                            <b-form-group
                                    id="input-group-3" class="required psw-show"                
                                    description="Password should contain at least one capital letter: (A-Z); at least one digit: 0-9; at least one special character (! @ $ % #) and be at least 6 chars long"                
                                >
                                <label id="input-group-3" class="label-psw">New Password</label> 
                                
                                    <b-form-input
                                        id="input-3"
                                        v-model.trim="newPsw"
                                        autocomplete="off"
                                        :type="showPassword ? 'text' : 'password'"
                                        @blur="$v.newPsw.$touch()"
                                        class="password"
                                        :class="{ 'is-invalid warning': this.$v.newPsw.$error }"          
                                    ></b-form-input>
                        <button class="unmask" type="button" title="Mask/Unmask password"
              @click="toggleShowPws" >Unmask</button>            
<!-- new psw front side errors  -->
                                <b-form-invalid-feedback v-if="inValidPswMinLen" class="invalid-feedback"
                                    >password should at least
                                    {{ $v.newPsw.$params.minLength.min }} chars
                                </b-form-invalid-feedback>
                                <b-form-invalid-feedback v-if="inValidPswMaxLen" class="invalid-feedback"
                                    >password should at most {{ $v.newPsw.$params.maxLength.max }} chars
                                </b-form-invalid-feedback>
                                <b-form-invalid-feedback v-if="newPswRequired" 
                                >{{ fieldRequired }}
                                </b-form-invalid-feedback>  
                                <ul class="mistake" v-if="$v.newPsw.$dirty && inCorrectPsw">
                                    <li class="" v-for="note in inCorrectPsw" :key="note.id">{{ note }}</li>
                                </ul>
                            </b-form-group>  
              
<!-- new psw server errors: password errors -->
                            <div class="warn mb-1" v-if="servErr.newPsw">
                                <ul>
                                    <li v-for="pswErr in servErr.newPsw" :key="pswErr.id">
                                        {{pswErr}}
                                    </li>
                                </ul>
                            </div>            
<!-- new re-psw -->
                            <b-form-group id="input-group-4" class="required"> 
                            <label id="input-group-4" class="control-label">Confirm new password</label>             
                            <b-form-input
                                id="input-4"
                                type="password"
                                placeholder="Repeat your password, please"
                                v-model.trim="newPsw2"
                                autocomplete="off"
                                @blur="$v.newPsw2.$touch()"
                            :class="{ 'is-invalid warning': this.$v.newPsw2.$error }"         
                            ></b-form-input>
<!-- front re-psw errors -->
                            <b-form-invalid-feedback
                                v-if="$v.newPsw2.$dirty && !$v.newPsw2.sameAs"
                                class="invalid-feedback"
                                >Passwords must be identical
                            </b-form-invalid-feedback>
                            <b-form-invalid-feedback v-if="newPsw2Required"> 
                                {{ fieldRequired }}
                            </b-form-invalid-feedback>  
                        </b-form-group>
<!-- server newPsw2 errors  -->
                            <div class="warn mb-1" v-if="servErr.newPsw2">
                                <ul>
                                    <li v-for="pswErr in servErr.newPsw2" :key="pswErr.id">
                                        {{pswErr}}
                                    </li>
                                </ul>
                            </div> 
<!-- server errors: non-field errors -->

                        <div class="warn mb-1" v-if="servErr.nonFieldErr">
                        <ul>
                            <li v-for="err in servErr.nonFieldErr" :key="err.id">
                            {{err}}
                            </li>
                        </ul>
                        </div>
<!-- django server is down -->
                        <div v-if="servErr.servDown" class="errorMsg col-md-12 mb-3">
                            Error message: {{servDownMsg}}
                            <b-icon icon="exclamation-circle-fill" variant="danger"></b-icon>        
                        </div>  
                        <div class="errorMsg col-md-12 mb-3" v-if="tokenExp">
                        <div class="px-1">{{unauthMsg}}</div>
                        </div>
<!-- buttons group -->
                    <b-row class="text-center mt-4">
                    <b-col cols="6">
                        <b-button type="submit"  variant="success" :disabled="formInValid">Submit</b-button>
                    </b-col >
                    <b-col cols="6">
                        <router-link :to="{name:'home'}">
                        <b-button  variant="primary">Home</b-button>
                        </router-link>
                    </b-col>
                    </b-row>    
                </b-form>  

<!--go home!--  -->
               
            </div>                    
          </div> 
        </div>
      </div>
    </div>
</template>
<script>
import {actionTypes} from '@/store/modules/auth'
import {mapState} from 'vuex'
import {required, minLength,  maxLength,  sameAs } from "vuelidate/lib/validators";
import AppLoader from '@/components/Loader'
export default {
    name:'AppChangePsw',
    components:{         
         AppLoader
    },
    data(){
        return{
            successMsg:"",
            errorMsg:"",
            currentPsw:'',
            newPsw:'',            
            newPsw2:"",
            //front-side vars/errors
            fieldRequired: "This field is required",
            // toggle password visiabilty
            showPassword: false,            
            // server side err's
            servErr:{},
            servDownMsg:'Sorry. Our server"s exper temp problems.Try again a little bit later',            
            tokenExp:false,
            unauthMsg:'Sorry your login session is expired.Please login agaon',
                      
            
        }
    },
    validations: {
        currentPsw:{required},
        newPsw: {
        required,
        minLength: minLength(8),
        maxLength: maxLength(128),
        },
        newPsw2: {
        required,
        minLength: minLength(8),
        maxLength: maxLength(128),
        sameAs: sameAs("newPsw"),
        },
    },
    computed:{
        ...mapState({
            isLoading:state=>state.auth.isLoading,                                       
           
        }),
        formInValid() {
            return this.$v.$invalid
        },        
        currentPswRequired() {
        return this.$v.currentPsw.$dirty && !this.$v.currentPsw.required;
        },
        newPswRequired() {
      return this.$v.newPsw.$dirty && !this.$v.newPsw.required;
        },
        newPsw2Required() {
        return this.$v.newPsw2.$dirty && !this.$v.newPsw2.required;
        },
        inValidPswMinLen() {
        return this.$v.newPsw.$dirty && !this.$v.newPsw.minLength;
        },
        inValidPswMaxLen() {
        return this.$v.newPsw.$dirty && !this.$v.newPsw.maxLength;
        },
        
        inCorrectPsw() {
        const customErrors = [];
        if (!this.$v.newPsw.$dirty) return customErrors;
        !/(?=.*[A-Z])/.test(this.newPsw) &&
            customErrors.push("Your passsword should have a capital letter");
        !/(?=.*\d)/.test(this.newPsw) &&
            customErrors.push("Your password should have a digit");
        !/([!@$%#])/.test(this.newPsw) &&
            customErrors.push("Your password should have a special chars like !@$%#");
        return customErrors;
        },
    },
    methods:{
        // http://127.0.0.1:8080/password/reset/confirm/Mg/5lr-5ae0f38bc9d739679076
        requestNewPassword(){           
            this.$store.dispatch(actionTypes.setNewPswAChange,{
                currentPsw:this.currentPsw,
                newPsw:this.newPsw,
                newPsw2:this.newPsw2
            })
            .then((resp)=>{
                // also for servErr's
                // console.log("resp in ChangePsw vue",resp)
                // console.log(Object.keys(resp))
                if(resp.servDown){
                    this.servDown = true
                }else if(resp.status === 204){
                    console.log("new psw created, re-directing to login");
                    this.successMsg = "Your password has been  succesfully changed"
                    setTimeout(()=>{
                        this.$router.push({name:"home"});  
                                         
                    },5000)
                     
                }else if(resp.status===401){
                    console.log("status 401 unauth-ed",resp.status)                                      
                    this.tokenExp = true                
                   
                }else if(resp.status===400){
                    console.log("status 400 calling",resp)
                    this.servErr = resp                  
                }
            }).catch((err)=>{
                this.errorMsg = "Something went wrong during password change. Be sure that you use a correct current" 
                
            })            
        },
        toggleShowPws() {
        this.showPassword = !this.showPassword;
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
  border-radius: 3px;
  height: 50px;;
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
/* toggle eye mask-unmask psw */
.psw-show { 
  position: relative; 
  }

.label-psw { 
  position: absolute;
  left:-9999px;
  text-indent: -9999px;
} 

.password + .unmask {
  position: absolute;
  right: 74px;
  top: 12px;
  text-indent: -9999px;
  width: 25px;
  height: 25px;
  background: #aaa;
  border-radius: 50%;
  cursor:pointer;
  border: none;
  -webkit-appearance:none;
}
.password + .unmask:before {
  content: "";
  position:absolute;
  top:4px; left:4px;
  width: 17px;
  height: 17px;
  background: #e3e3e3;
  z-index:1;
  border-radius: 50%;
}
.password[type="text"] + .unmask:after {
  content: "";
  position:absolute;
  top:6px; left:6px;
  width: 13px;
  height: 13px;
  background: #aaa;
  z-index:2;
  border-radius: 50%;
} 
@media all and (max-width:700px){
  .password+.unmask{
    right:15px;
  }
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
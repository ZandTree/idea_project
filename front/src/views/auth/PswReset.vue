<template>
    <div class="container">
        <div class="messages row mb-2">
        <div v-if="errorMsg" class="errorMsg col-md-12">
            Error message: {{errorMsg}}
            <b-icon icon="exclamation-circle-fill" variant="danger"></b-icon>        
        </div>      
        <div v-if="pswResetFailure" class="errorMsg col-md-12">
            Link you are trying to use is not more available.
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
                        <h1>Please, set your new password</h1>                        
                        <b-form @submit.prevent="requestNewPassword">
<!-- psw -->
            <div class="d-flex justify-content-between">
                              <div >Password</div>
                              <div>Show Password</div>
              </div> 
                <b-form-group
                        id="input-group-3" class="required psw-show"                
                        description="Password should contain at least one capital letter: (A-Z); at least one digit: 0-9; at least one special character (! @ $ % #) and be at least 6 chars long"                
                    >
                    <label id="input-group-3" class="control-label label-psw">Password</label> 
                        <b-form-input
                            id="input-3"
                            v-model.trim="psw"
                            :type="showPassword ? 'text' : 'password'"
                            @blur="$v.psw.$touch()"
                            class="password"
                            :class="{ 'is-invalid warning': this.$v.psw.$error }"          
                        ></b-form-input>
                        <button class="unmask" type="button" title="Mask/Unmask password"
                                @click="toggleShowPws" >Unmask
                        </button>
             
<!--psw front side errors  -->
                    <b-form-invalid-feedback v-if="inValidPswMinLen" class="invalid-feedback"
                        >password should at least
                        {{ $v.psw.$params.minLength.min }} chars
                    </b-form-invalid-feedback>
                    <b-form-invalid-feedback v-if="inValidPswMaxLen" class="invalid-feedback"
                        >password should at most {{ $v.psw.$params.maxLength.max }} chars
                    </b-form-invalid-feedback>
                    <ul class="mistake" v-if="$v.psw.$dirty && inCorrectPsw">
                        <li class="" v-for="note in inCorrectPsw" :key="note.id">{{ note }}</li>
                    </ul>
                </b-form-group>                
<!-- psw server errors: password errors -->
                            <div class="warn mb-1" v-if="servResp.pswErr">
                            <ul>
                                <li v-for="pswErr in servResp.pswErr" :key="pswErr.id">
                                {{pswErr}}
                                </li>
                            </ul>
                            </div>            
<!-- re-psw -->
                            <b-form-group
                                id="input-group-4" class="required"> 
                            <label id="input-group-4" class="control-label">Confirm password</label>             
                            <b-form-input
                                id="input-4"
                                type="password"
                                placeholder="Repeat your password, please"
                                v-model="psw2"
                                @blur="$v.psw2.$touch()"
                            :class="{ 'is-invalid warning': this.$v.psw2.$error }"         
                            ></b-form-input>
<!-- front re-psw errors -->
                            <b-form-invalid-feedback
                                v-if="$v.psw2.$dirty && !$v.psw2.sameAs"
                                class="invalid-feedback"
                                >Passwords must be identical
                            </b-form-invalid-feedback>
                            </b-form-group>
<!-- server errors: non-field errors -->
                        <div class="warn mb-1" v-if="servResp.nonFieldErr">
                        <ul>
                            <li v-for="err in servResp.nonFieldErr" :key="err.id">
                            {{err}}
                            </li>
                        </ul>
                        </div>
<!-- django server is down -->
                        <div class="warn mb-3" v-if="servResp.netWorkErr">
                        <div class="px-1">{{servResp.netWorkErr}}</div>
                        </div>
<!-- buttons group -->
                    <b-row class="text-center mt-4">
                    <b-col cols="6">
                        <b-button type="submit"  variant="success" :disabled="$v.$invalid && $v.$error">Submit</b-button>
                    </b-col >
                    <b-col cols="6">
                        <b-button type="reset" variant="danger">Reset</b-button>
                    </b-col>
                    </b-row>    
                </b-form>                        
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
    name:'AppPswReset',
    components:{         
         AppLoader
    },
    data(){
        return{
            successMsg:"",
            errorMsg:"",
            oldLink:"Send a request to reset paswwrod again.Don't use old link in email box",
            psw:"",
            psw2:"",
            // server side err's
            servResp:{
            status:'',    
            pswErr:null,
            nonFieldErr:null,
            netWorkErr:null
            },
            //front-side vars/errors
            fieldRequired: "This field is required",
            // toggle password visiabilty
            showPassword: false,
        }
    },
    validations: {
        psw: {
        required,
        minLength: minLength(8),
        maxLength: maxLength(128),
        },
        psw2: {
        required,
        minLength: minLength(8),
        maxLength: maxLength(128),
        sameAs: sameAs("psw"),
        },
    },
    computed:{
        ...mapState({
            isLoading:state=>state.auth.isLoading,
            pswResetFailure:state=>state.auth.pswResetFailure,
                           
           
        }),
        pswRequired() {
        return this.$v.psw.$dirty && !this.$v.psw.required;
        },
        inValidPswMinLen() {
        return this.$v.psw.$dirty && !this.$v.psw.minLength;
        },
        inValidPswMaxLen() {
        return this.$v.psw.$dirty && !this.$v.psw.maxLength;
        },
        inCorrectPsw() {
        const customErrors = [];
        if (!this.$v.psw.$dirty) return customErrors;
        !/(?=.*[A-Z])/.test(this.psw) &&
            customErrors.push("Your passsword should have a capital letter");
        !/(?=.*\d)/.test(this.psw) &&
            customErrors.push("Your password should have a digit");
        !/([!@$%#])/.test(this.psw) &&
            customErrors.push("Your password should have a special chars like !@$%#");
        return customErrors;
        },
    },
    methods:{
        // http://127.0.0.1:8080/password/reset/confirm/Mg/5lr-5ae0f38bc9d739679076
        requestNewPassword(){
           let uid= this.$route.params.uid;
           let token = this.$route.params.token; 
            this.$store.dispatch(actionTypes.setNewPswAfterForget,{
                uid:uid,
                token:token,
                psw:this.psw,
                psw2:this.psw2

            })
            .then((resp)=>{
                console.log("activate view got resp",resp)
                if(resp.status === 204){
                    console.log("new psw created, re-directing to login");
                    this.successMsg = "New password is is succesfully created, go to login"
                    setTimeout(()=>{
                        this.$router.push({name:"login"});  
                                         
                    },5000)
                     
                }
            }).catch((err)=>{
                this.errorMsg = "Something went wrong.Please contact us to clearify the problem";
                console.log("err",err)
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
.errorMsg{
    background-color: rgb(236, 187, 195);
    height: 50px;
    
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
  top: 9px;
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
</style>
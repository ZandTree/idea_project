<template>
  <div class="container py-md-5 py-4">    
    <div class="row">
      <!-- <div class="long">       -->
       <div class="col col-md-10 py-2 mx-auto">
        <div v-if="profile" class="card mb-3 p-2" style="width: 56rem;" >
        <h1>Change your profile,</h1>   
        <div class="card-body">
<!-- form -->
          <b-form               
          @submit.prevent="onSubmit"
          ref="profileSubmitForm"
          enctype="multipart/form-data">
<!-- website -->
          <b-form-group id="input-group-1" label="Your Web Site:" label-for="input-1">
                <b-form-input
                  id="input-1"
                  v-model="website"
                  placeholder="Enter website address" 
                  :class="{ 'is-invalid warning': this.$v.website.$error }"
                  @blur="$v.website.$touch()"                 
                ></b-form-input>
<!-- front  website errors -->
                <b-form-invalid-feedback v-if="inValidWebsiteNotUrl" class="invalid-feedback"
                  >Enter a valid url,please
                </b-form-invalid-feedback>  
                <b-form-invalid-feedback v-if="inValidWebsiteMaxLen" class="invalid-feedback"
                >Lead text should at most {{ $v.website.$params.maxLength.max }} chars
                </b-form-invalid-feedback> 


          </b-form-group>    
<!-- <p >Errs:{{servResp}}</p> -->
<!-- backend website errors: model has URLField   -->              
          <div v-if="servResp.websiteErrs">
                <ul>
                  <li class="warning" v-for="err in servResp.websiteErrs" :key="err.id">
                    {{ err }}
                  </li>
                </ul>
          </div>              
<!-- bio -->
          <b-form-group id="input-group-2" label="Bio :" label-for="input-2">
            <b-form-input
              id="input-2"
              placeholder="Bio"
              v-model.trim="bio"
              :class="{ 'is-invalid warning': this.$v.bio.$error }"
            @blur="$v.bio.$touch()"                                      
            ></b-form-input>
<!-- front side bio errors -->
          <b-form-invalid-feedback v-if="inValidBioMaxLen" class="invalid-feedback"
              >Lead text should at most {{ $v.bio.$params.maxLength.max }} chars
          </b-form-invalid-feedback>


          </b-form-group>
<!-- server bio errors -->
          <div v-if="servResp.bioErrs">
              <ul>
                <li class="warning" v-for="err in servResp.bioErrs" :key="err.id">
                  {{ err }}
                </li>
              </ul>
          </div>
<!-- (profile) image  -->
                <b-form-group id="input-group-5" label="Upload File">
                  <div class="file-wrap">          
                  <label class="file-select mr-sm-2">
                    <div class="select-button">
                      <span v-if="image&&image.name">Current file: {{image.name}}</span>
                      <span v-if="image&&!image.name">Current file: {{getShortName}}</span>
                      <span v-if="!image">Select File</span>
                    </div>   
                  <input
                    id="image"
                    type="file"
                    ref="file"
                    accept=".jpg,.jpeg,.png"
                    @change="onFileChange"
                    @click="clearCheckboxUploadFile"                     
                  />
                  </label>
                  <span class="clearable-file-input">
                      <label class="text-mute">Remove file
                      <input
                        id="checkbox_img"
                        type="checkbox"
                        ref="check"
                        v-model="checked"
                        name="image_clear"
                        @change="detachFile"
                      />
                      </label>
                  </span>                        
                  </div>
                  <p class="text-mute">Allowed images with extentions: .png,.jpg/.jpeg</p> 
<!-- front-side success upload file  TODO: do I need it?-->
                   
                   <div class="msg mb-2 py-2" v-if="localErr" :class="`${localErr ? 'is-danger' : 'is-success'}`">
                    <div class="msg-body" v-if="alertHeavyFile">{{heavyFileMsg }}</div>
                    
                    <div class="msg-body mb-1" v-if="formatNotAllowed">
                      Only images are allowed
                    </div> 
                   <b-button @click="userSawErrors" class="mt-2">initial state</b-button>
                    
                              
                </div>  
<!-- server side errors upload file(too big; ext not allowed) -->
                  <!-- <div v-if="servImgErrs">
                    <ul>
                      <li class="warning" v-for="err in servImgErrs" :key="err.id">
                        {{ err }}
                      </li>
                    </ul>
                  </div> -->
                </b-form-group>
               
                <b-button type="submit" class="btn btn-secondary"
                  :disabled="submitButDisable">Edit It</b-button>                                
                </b-form>
<!-- general errors          -->                 
<!-- django server is down or err-500 -->
          <div class="warning mb-3 mt-3" v-if="servResp.netWorkErr">
            <div class="px-1">{{servResp.netWorkErr}}</div>
          </div>                 
        </div>
        </div>
        <div v-if=!profile class="is-danger not-welcome">You are not allowed to see this page</div>

        </div>
      </div>   
      
  </div>
</template>
              
            
<script>
import {mapGetters} from 'vuex'
import {getterTypes} from '@/store/modules/auth'
import {actionTypes} from '@/store/modules/profile'
import {mapState} from 'vuex'
import optimizePhoto from '@/assets/js/resizeIt.js'
import getFileNameFromUrl from '@/assets/js/shortName.js'
import { maxLength, url } from "vuelidate/lib/validators";

export default {
  name:'ProfileEdit',
  data(){
      return {     
        bio:'',
        image:'',
        checked:false,
        // website
        website:'',                         
        // upload file 
        checked: false, 
        localErr:false,
        formatNotAllowed:false,
        resizedImage:null,                            
        alertHeavyFile:null, 
        heavyFileMsg:null,

        
        // all UI msg(?) 
        browserFileUploadMsg:null,
        servResp:{
          status:null,
          bioErrs:null,
          imageErrs:null,
          websiteErrs:null,          
          netWorkErr:null,          
        },
      }
    },
   validations:{
      bio:{maxLength:maxLength(2048)},
      website:{url, maxLength:maxLength(120) },     
    },  
  computed:{
      ...mapState({            
            profile:state=>state.profile.data,
            isLoading:state=>state.profile.isLoading,
            error:state=>state.profile.error,
                      
        }),       
        ...mapGetters({
          currentUser:getterTypes.currentUser,
        }), 
      
      getShortName(){
        // return only file name from aws url link
        return getFileNameFromUrl(this.image)
      },
     
    formInValid() {
      return this.$v.$invalid;
      },
      submitButDisable(){
        return this.formInValid||this.alertHeavyFile||this.formatNotAllowed
      },
    inValidBioMaxLen() {
      return this.$v.bio.$dirty && !this.$v.bio.maxLength;
    },  
    inValidWebsiteMaxLen() {
      return this.$v.website.$dirty && !this.$v.website.maxLength;
    },  
    inValidWebsiteNotUrl() {
      return this.$v.website.$dirty && !this.$v.website.url;
    },  
         
    
  },
  methods:{
      onSubmit(){
        // console.log('editing profile')
        const unid = this.currentUser.unid
        const profileData = new FormData()
        // console.log(unid,this.website,this.bio)
        profileData.append('bio',this.bio)
        profileData.append('website',this.website) 
        if(this.image !==''){
          profileData.append('image',this.image)
        }else{
          profileData.append('image','')
        }
               
        this.$store.dispatch(actionTypes.editPersonalInfo,{unid,profileData})
        .then((resp)=>{
          console.log("from store resp",resp)
          if(resp.status ===200){
            this.$router.push({name:'accountProfile',params:{unid:unid}})
          }else if(resp.servDown){
            this.servResp.netWorkErr = 'Sorry. Our server is enduring some problems.Please try later'
          }else if(resp.status === 500){
             this.servResp.netWorkErr = 'A server/network error occured.Sorry about this - we will get it fixed shortly.'
          }else{
            console.log("errror 400?",resp.status)
            this.servResp.status = resp.status
            this.servResp.websiteErrs = resp.websiteErr
            this.servResp.imageErrs = resp.imageErr
            this.servResp.bioErrs = resp.bioErr
            
          }
        }).catch((err)=>{
          console.log("final error",err)
        })
      },     
      async onFileChange(){
        console.log('file changing')
        this.$refs.check.checked = false
        this.browserFileUploadMsg = ''
        console.log('inital path to uploaded img is:',this.$refs.file.value)
        let img = this.$refs.file.files[0]
        const allowedTypes = ['image/jpeg', 'image/png', 'image/jpg']
        const MAX_SIZE = 2000000
        const tooBig = img.size > MAX_SIZE
        if(allowedTypes.includes(img.type)&&!tooBig){
          this.image = img
          console.log("ready to send img",this.image.size)
          console.log("path to file is:",this.$refs.file.value)
          // resizing image with util (7-8 times)
          const resizedImage = await optimizePhoto(this.image)
          this.image = new File([resizedImage],this.image.name)
        }else{
          this.localErr = true
          if(tooBig){
            this.alertHeavyFile = true
            this.heavyFileMsg = `File too large.MAX sise is ${MAX_SIZE / 1000}kB`
          }
          if(!allowedTypes.includes(img.type)){
            this.formatNotAllowed = true
          }
        }
      },
      clearCheckboxUploadFile(){
        console.log('clear checkbox upload')
        this.$refs.check.checked=false
      },
       detachFile(){
         // user wants to remove img to replace it/or upload aother one if file too large/ext problem
        console.log('checkbox clicked so detach file')
        this.$refs.file.value= ''// path to file on
        console.log('done,after detachment image path is:',this.$refs.file.value)
        this.localErr = false
        this.image = ''
        this.resizedImage=null

      },
      userSawErrors(){
        this.alertHeavyFile=false
        this.formatNotAllowed=false
        this.localErr=false
      }
    },
    created(){
      // console.log("create and got profile",this.profile)
      let src = this.profile
      this.website = src.website
      this.bio= src.bio
      this.image=src.image
    
  }    
}
</script>
<style scoped>

body {
  height: 100vh;
  margin: 0; padding: 0;

  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: row;

  font-family: 'Nunito', sans-serif;
  background-color: blanchedalmond;
  /* color: rgb(50, 50, 50); */
}
.warning{
  background-color: #e4b1b6;
  border-radius: 5px;
  padding:5px 10px;
}
.flashErrs{
  cursor: pointer;
}
/* style Digital Ocean */
.file-select > .select-button {
  padding: 0.5rem;
  /* color: white; */
  background-color: #d8dee4;
  border-radius: 0.3rem;
  text-align: center;
  font-weight: bold;
}
/* Don't forget to hide the original file input! */
.file-select > input[type='file'] {
  display: none;
}
/* end digitalOcaen */

/* .text-mute {
  font-size: 16px;
}
.file-wrap {
  display: flex;
  justify-content: space-around;
  padding: 0.5rem;
}
.msg {
  border-radius: 6px;
  color: white;
} */

  

</style>

<template>
    <div>
      <section >
          <p class="text-muted"><span class="control-label">Fields marked with </span> are required</p>
          
<!-- loader  submit         -->
            <div class="col-xs-12 col-md-10 py-3 text-center offset-md-1">
              <app-loader v-if="isSubmitting"></app-loader>
            </div>
 <!-- errors  -->
<!-- django server is down -->
            <div class="warn mb-3" v-if="errors.netWorkErr">
              <div class="px-1">{{errors.netWorkErr}}</div>
            </div>      
 <!-- form  -->
          <b-form
                @submit.prevent="onSubmit"      
                enctype="multipart/form-data"
                novalidate > 
<!-- imported component categories -->
                <app-categ-input
                    :set-categ-names="categories"
                    :categ="categ"
                    @getCateg="readCategVal">
                   >
                </app-categ-input>
<!-- server errors category  -->                 
                <div class="warn mb-1" v-if="errors.categErr">
                  <ul>
                    <li v-for="err in errors.categErr" :key="err.id">
                      <!-- {{err}} -->
                      Choose a category,please
                      <!-- Invalid pk "0" - object does not exist. -->
                    </li>
                  </ul>
                </div>
<!-- title -->
                <b-form-group id="input-group-1" class="text-left">
                  <label for="input-1" class="control-label">Title</label>
                    <b-form-input           
                    id="input-1"
                    class="control-label"
                    v-model.trim="title"
                    :class="{ 'is-invalid warning': this.$v.title.$error }"
                    @blur="$v.title.$touch()"
                    ></b-form-input>
<!-- front-side errors title-->  
                <b-form-invalid-feedback v-if="titleRequired" class="invalid-feedback"
                  >{{ fieldRequired }}
                </b-form-invalid-feedback>
                <b-form-invalid-feedback v-if="inValidTitleMaxLen" class="invalid-feedback"
              >Title should at most {{ $v.title.$params.maxLength.max }} chars
              </b-form-invalid-feedback> 
              
                </b-form-group>
<!-- server errors title         -->
                <div class="warn mb-1" v-if="errors.titleErr">
                  <ul>
                    <li v-for="err in errors.titleErr" :key="err.id">
                      {{err}}
                    </li>
                  </ul>
                </div>
<!-- leadtext -->
                <b-form-group id="input-group-2" class="text-left">
                  <label for="input-2" class="control-label">Lead text</label>
                    <b-form-input
                    id="input-2"
                    :class="{ 'is-invalid warning': this.$v.leadText.$error }"
                    @blur="$v.leadText.$touch()"
                    v-model.trim="leadText"
                    ></b-form-input>
<!-- front-side errors  leadText-->              
                <b-form-invalid-feedback v-if="leadTextRequired" class="invalid-feedback"
                  >{{ fieldRequired }}
                </b-form-invalid-feedback>  
                <b-form-invalid-feedback v-if="inValidLeadTextMaxLen" class="invalid-feedback"
              >Lead text should at most {{ $v.leadText.$params.maxLength.max }} chars
              </b-form-invalid-feedback>   
                </b-form-group>
<!-- server side leadText errors (incl: Ensure this field has no more than 240 characters)                -->
                <div class="warn mb-1" v-if="errors.leadTextErr">
                  <ul>
                    <li v-for="err in errors.leadTextErr" :key="err.id">
                      {{err}}
                    </li>
                  </ul>
                </div>
  <!-- front side leadText errors  -->
  <!-- TODO -->

<!-- mainText -->
                <b-form-group id="input-group-3" class="text-left">
                  <label for="input-3" class="control-label">Main Text</label>
                    <b-form-textarea
                    id="input-3"
                    :class="{ 'is-invalid warning': this.$v.mainText.$error }"
                    @blur="$v.mainText.$touch()"
                    v-model="mainText"
                    placeholder="What is this idea about..."                    
                    rows="20"
                    max-rows="6"
                    ></b-form-textarea>
<!-- front-side errors  mainText-->                       
                <b-form-invalid-feedback v-if="mainTextRequired" class="invalid-feedback"
                  >{{ fieldRequired }}
                </b-form-invalid-feedback> 
                <b-form-invalid-feedback v-if="inValidMainTextMaxLen" class="invalid-feedback"
                >Main text should at most {{ $v.mainText.$params.maxLength.max }} chars
                </b-form-invalid-feedback>    
            
              </b-form-group>
<!-- server side mainText errors  -->
                <div class="warn mb-1" v-if="errors.mainTextErr">
                  <ul>
                    <li v-for="err in errors.mainTextErr" :key="err.id">
                      {{err}}
                    </li>
                  </ul>
                </div>         
<!-- tags -->
                
                <b-form-group id="input-group-4" class="text-left"
                description="Tags are not required; length should be less than 50 chars and not contain % { $ }"   
                >
                  <label id="input-group-4">Tags </label> 
                  
                    <b-form-input          
                    id="input-4"
                    v-model.trim = "tags"
                    :class="{ 'is-invalid warning': this.$v.tags.$error }"
                    @blur="$v.tags.$touch()"
                    ></b-form-input>
<!-- front side tags erros -->
                <b-form-invalid-feedback v-if="inValidTagsMaxLen" class="invalid-feedback"
                >Tags text should be at most {{ $v.tags.$params.maxLength.max }} chars
                </b-form-invalid-feedback>  
                <ul class="mistake" v-if="$v.tags.$dirty && inCorrectTags">
                  <li class="" v-for="note in inCorrectTags" :key="note.id">{{ note }}</li>
                </ul> 
                </b-form-group>
                
<!-- server side tags errors -->
                <div class="warn mb-1" v-if="errors.tagsErr">
                    <h5>Tags error: {{errors.tagsErr}}</h5>
                  
                </div>                  
<!-- thumnail -->
          <b-form-group id="input-group-5" label="Upload File" inline>
            <div class="file-wrap">
              <label class="file-select mr-sm-2">
                <div class="select-button">
                  <span v-if="thumbnail&&thumbnail.name">Current file: {{thumbnail.name}}</span>
                  <span v-if="thumbnail&&!thumbnail.name">Current file: {{getShortName}}</span>
                  <span v-if="!thumbnail">Select File</span>
                  
                </div>
                <input
                  id="thumbnail"
                  type="file"
                  ref="file"
                  accept=".jpg,.jpeg,.png"
                  @change="onFileChange"
                  @click="clearCheckboxUploadFile"
                />
              </label>
              <span class="clearable-file-input">
                <label class="text-mute">
                  <input
                    id="checkbox_img"
                    v-model="checked"
                    type="checkbox"
                    ref="check"
                    @change="detachFile"
                    name="thumbnail_clear"
                  />
                  Remove file
                </label>
              </span>
            </div>
            <p class="text-mute">Allowed images with extentions: .png,.jpg/.jpeg</p>
            <!-- <p>wwwstate thumbnail {{thumbnail}}</p>
            <p>wwwedit: {{edit}}</p> -->
       
          </b-form-group> 
<!-- server side errors upload file(too big; ext not allowed) -->            
            <div v-if="errors.thumbnailErr">
              <div class="warn mb-1" v-if="errors.thumbnailErr">
                  <ul>
                    <li v-for="err in errors.thumbnailErr" :key="err.id">
                      {{err}}
                    </li>
                  </ul>
                </div>  
            </div> 
 <!-- front-side errors upload file-->
            <div class="msg mb-2 py-2" v-if="localErr" :class="`${localErr ? 'is-danger' : 'is-success'}`">
                <div class="msg-body mb-1" v-if="alertHeavyFile">{{ alertHeavyFile }}</div>
                <div class="msg-body" v-if="formatNotAllowed">
                  Only images are allowed
                </div>
             <b-button @click="userSawErrors" class="mt-2">initial state</b-button>                
            </div>
 <!-- server side Bad request not auth-ed -->
          <div v-if="errors.error400">
              <div class="warn mb-1">
                 <p class="is_danger"><strong>{{errors.error400.badRequest}}</strong></p> 
              </div>  
            </div> 
          <div v-if="errors.notAuthorized">
              <div class="warn mb-1">
                 <p class="is_danger"><strong>{{errors.notAuthorized.notAuthorized}}</strong></p> 
              </div>  
            </div>
          <div v-if="errors.noPerms">
              <div class="warn mb-1">
                 <p class="is_danger"><strong>{{errors.noPerms.noPermission}}</strong></p> 
              </div>  
            </div>
<!-- end server side bad request not auth-ed-->
            <b-button type="submit" variant="primary" class="pull-xs-right btn btn-large btn-success"
            :disabled="submitButDisable">
                Publish Idea
            </b-button>     
          </b-form>
             
      </section>        
    </div>    
</template>                
                
<script>
import AppCategInput from '@/components/categs/CategInput'
import AppValidationErrors from '@/components/ValidationErrors'
import AppLoader from '@/components/Loader'
import tagsHelp from '@/helpers/tagsHelper'
import optimizePhoto from '@/assets/js/resizeIt.js'
import getFileNameFromUrl from '@/assets/js/shortName.js'
import { required, maxLength} from  "vuelidate/lib/validators";

export default {
    name:'AppIdeaForm',
    components:{
        AppCategInput,
        AppLoader,
        AppValidationErrors,        
    },
    props:{
        categories:{
           type:Array,
           required:true

        },
        initialValues:{
            type:Object,
            required:true
        },
        errors:{
            type:Object,
            
        },
        isSubmitting:{
            type:Boolean,
            required:true
        },
        action:{
          type:String
        }
    },
    data(){
        return {
            // TODO: categs,author
            categ:this.initialValues.categ,
            title: this.initialValues.title,
            leadText: this.initialValues.leadText,
            mainText: this.initialValues.mainText,                
            featured: this.initialValues.featured,
            tags: this.initialValues.tags,            
            // upload file 
            thumbnail: this.initialValues.thumbnail,                 
            checked: false, 
            localErr:false,
            formatNotAllowed:false,
            resizedThumbnail:null,                            
            alertHeavyFile:null,  
            // clickRemoveFile:false, 
            //front-side errors
            categInputPresent:false,
            fieldRequired: "This field is required", 
            customSubmitPort:this.isSubmitting,
            customCategErr:false       
        }
    },
    validations:{
      categ:{required},
      title:{required,maxLength:maxLength(120)},
      leadText:{required,maxLength:maxLength(120)},
      mainText:{required,maxLength:maxLength(2048)},
      tags:{maxLength:maxLength(50)}

    },
    methods:{
        onSubmit(){         
            const data = new FormData()
            data.append('categ ', this.categ)
            data.append('title', this.title)
            data.append('lead_text', this.leadText)
            data.append('main_text', this.mainText)             
            if(this.tags){
            // clean tag string from '@$%#' 
            const cleanTags = tagsHelp.trimInputTag(this.tags);            
            data.append('tags', cleanTags)         
            }
            if (this.resizedThumbnail) {              
            data.append('thumbnail', this.resizedThumbnail)
          } else if(this.clickRemoveFile){
            
            // user removes attached file so this.thumbnail = ""
            data.append('thumbnail', '')
          }else if(!this.clickRemoveFile
                  &&typeof this.thumbnail==='string'
                  &&this.thumbnail.includes('https://boterland.s3.amazonaws.com')){
            data.append('thumbnail',this.initialValues.thumbnail)
          }
          else{         
            data.append('thumbnail','')
          }          
            this.$emit('ideaSubmit',data)            
        },
        readCategVal(cat){            
            this.categ = cat            
        },
        async onFileChange() {
          // clear prev error msg and uncheck state
          this.$refs.check.checked = false
          this.localErr = false
          // this.browserFileUploadMsg = ''
          
          // temp variable for uploaded img to check size && type;
          let img = this.$refs.file.files[0]
          const allowedTypes = ['image/jpeg', 'image/png', 'image/jpg']
          // const MAX_SIZE = 20
          const MAX_SIZE = 2000000
          const tooBig = img.size > MAX_SIZE
          if (allowedTypes.includes(img.type) && !tooBig) {
            // accept image only if type &&size OK; this thumnail will keep the name/size of uploaded img
            this.thumbnail = img          
            
            // this.browserFileUploadMsg = 'loading this file'
            // resize uploaded image with custom js util (aprox 7-8- times)
            const resizedPhoto = await optimizePhoto(this.thumbnail)
            // resizedPhoto is blob|=> convert it to a file
            this.resizedThumbnail = new File([resizedPhoto], this.thumbnail.name)
            
          } else {
            this.localErr = true
            // this.browserFileUploadMsg = tooBig ? `File too large.MAX sise is ${MAX_SIZE / 1000}kB`: `Only images are allowed`
            if (tooBig) {             
              this.alertHeavyFile = `File too large.MAX sise is ${MAX_SIZE / 1000}kB`
              // this.browserFileUploadMsg = `File too large.MAX sise is ${MAX_SIZE / 1000}kB`
            }
            if (!allowedTypes.includes(img.type)) {              
              this.formatNotAllowed = true //`Only images are allowed`
              // this.browserFileUploadMsg = `Only images are allowed`
            }
          }
          
        },
        clearCheckboxUploadFile(){
          // if upload button clicked|=> intention to upload a (new) file|=> checkbox input gets cleared
          
          this.$refs.check.checked = false // boolean
        },
        detachFile(){
          this.$refs.file.value = '' // path to file on local machine
          this.localErr = false
          // this.thumbnail = null
          this.clickRemoveFile=true
          this.thumbnail = ''
          this.resizedThumbnail = null
          // this.alertHeavyFile = false;
          // this.formatNotAllowed = false;
        },
        userSawErrors(){
        this.alertHeavyFile=false
        this.formatNotAllowed=false
        this.localErr=false
      }
    },
    computed:{
      formInValid() {
      return this.$v.$invalid;
      },
      submitButDisable(){
        return this.formInValid||this.customSubmitPort||this.alertHeavyFile||this.formatNotAllowed||this.categ===0
      },
      categRequired(){
        return this.categ===0
      },
      // return only file name from aws 3 url link
      getShortName(){
        if(this.thumbnail){
          return getFileNameFromUrl(this.thumbnail)

        }else{
          return ""
        }
      },
      titleRequired() {
        
      return this.$v.title.$dirty && !this.$v.title.required;
    },
      leadTextRequired() {
      return this.$v.leadText.$dirty && !this.$v.leadText.required;
    },
      mainTextRequired() {
      return this.$v.mainText.$dirty && !this.$v.mainText.required;
    },
    inValidTitleMaxLen() {
      return this.$v.title.$dirty && !this.$v.title.maxLength;
    },
    
    inValidLeadTextMaxLen() {
      return this.$v.leadText.$dirty && !this.$v.leadText.maxLength;
    },
    inValidMainTextMaxLen() {
        return this.$v.mainText.$dirty && !this.$v.mainText.maxLength;
    },
    inValidTagsMaxLen() {
        return this.$v.tags.$dirty && !this.$v.tags.maxLength;
    },
    inCorrectTags() {
      const tagsErrors = [];
      if (!this.$v.tags.$dirty) return tagsErrors;     
      
      /([{%$}])/.test(this.tags)&&      
        tagsErrors.push("Tags should not contain digits chars like @$%#");
        return tagsErrors
      
    },
    
  }   
}
</script>
<style scoped>
.warn{
    background-color: cornsilk;
}  
.mistake {
  color: red;
  text-align: left;
  font-size: 0.8rem;
}

/* style Digital Ocean */
.file-select > .select-button {
  padding: 0.5rem;
  color: white;
  background-color: #84898e;
  border-radius: 0.3rem;
  text-align: center;
  font-weight: bold;
}
/* Don't forget to hide the original file input! */
.file-select > input[type='file'] {
  display: none;
}
/* end digitalOcaen */
.text-mute {
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
}
                   
 /* .input-area {
  outline: none;
  border: 1px solid #d8d8d8 !important;
  box-shadow: none !important;
  border-radius: 0 !important;
  background-color: #ffffff;
  height: 150px;
  flex-grow: 1;
  padding: 10px !important;
  font-family: inherit;
  transition: 0.3s;
  font-size: 16px;
  font-weight: 300;
  height: 400px;
  color: #000000;
  letter-spacing: 1px;
  overflow: hidden;
  overflow-y: scroll;
  resize: none;
 }                   */
                

</style>
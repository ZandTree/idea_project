<template>
    <div>
        <div class="mb-5 mx-auto" >
            <!-- <p>submit label</p>{{submitLabel}}-->
            <!-- <p>creaning the form: {{cleanForm}}</p> -->
          <form @submit.prevent="onSubmit" ref="zoo" >  
            <div class="form-group">
              <label for="body">Comment (max {{ $v.body.$params.maxLength.max }} chars)</label>
                <textarea id="body" 
                cols="30" rows="12"
                class="body-bg  w-100 h-50 my-2"
                :class="{ 'is-invalid warning body-warning': this.$v.body.$error }"
                v-model="body" 
                @blur="$v.body.$touch()"  
                placeholder="Remember be nice">
                </textarea>
<!-- front-side errors body-->
              
                <b-form-invalid-feedback v-if="bodyRequired" class="invalid-feedback"
                  >{{ fieldRequired }}
                </b-form-invalid-feedback>
                <b-form-invalid-feedback v-if="inValidBodyMaxLen" class="invalid-feedback"
                    >Comment should at most {{ $v.body.$params.maxLength.max }} chars
                </b-form-invalid-feedback> 
             
            </div> 
            <div class="d-flex justify-content-around">
            <button class="btn btn-success" type="submit"
            :disabled="formInValid">{{submitLabel}}</button>           
            

            <button v-if="hasCancelButton" class="btn btn-primary" @click="handleCancel">Cancel</button>

            <button v-if="hasCancelButtonRoot" class="btn btn-primary" @click="handleCancelRootComment">Cancel</button>
            </div>                 
             
                  
          </form>
            <!-- <button  class="btn btn-primary" @click="ha">Ha Ha</button> -->
         
           
    </div>
    </div>
</template>
<script>
import {required, maxLength}  from "vuelidate/lib/validators";
export default {
    name:'CommentForm',
    props:{
        cleanForm:{
            type:Boolean
        },
        activeComment:{
          type:Object||null
        },        
        hasCancelButton:{
            type:Boolean
        },
        hasCancelButtonRoot:{
            type:Boolean
        },
        initialBody:{
            type:String
        },
        parentId:{
            type:Number||null
        },
        replyToId:{
            type:Number||null
        },
        submitLabel:{
            type:String,
            required:true
        },
        
        success:{
            type:Boolean
        },
        
        
    },
    data(){
        return{
            body:this.initialBody,
            fieldRequired: "This field is required",
            // bug winthin during Cancel(root comment) reset serves as port to display front error
            
        }
    },
    validations: {
    body: { required, maxLength:maxLength(6500) },
    
    },
    methods:{       
        onSubmit(){
            // this.handleSubmit(this.text)
                      
            if(this.submitLabel==='Edit'){
                let commentData = {
                    body:this.body                
                }
                this.$emit('updateComment',commentData)

            }else if(this.submitLabel==='Reply'){
                let commentData = {
                body:this.body,
                parent:this.parentId
                }
                this.$emit('reply',commentData)
            }else if(this.submitLabel==='Write'&&!this.formInValid){
                
                let commentData = {
                body:this.body,
                parent:null
                }
                this.$emit('addRootComment',commentData)
                if(this.cleanForm){                    
                    this.body = ""                    
                }
            }
            
        },
        handleCancel(){                                
            this.$emit('handleCancel')
        },
        handleCancelRootComment(){
            this.$emit('handleCancelRootComment')
        }

    },
    computed:{
        getBodyText(){
            return this.initialBody
        },
        cleaning(){
            return this.cleanForm
        },
        formInValid() {
        return this.$v.$invalid;
        },
        bodyRequired() {
            return this.$v.body.$dirty && !this.$v.body.required;
        },
        inValidBodyMaxLen() {
            return this.$v.body.$dirty && !this.$v.body.maxLength;
        },
      
    },
    watch: {
        cleaning() {
            // console.log("watcher here; see changes")
            this.body=''
        },
    }
}
</script>
<style scoped>
.body-bg{
    background-color: rgb(252, 249, 249);
    color:black;
}
/* if chars amount > maxLength this class will be added to textarea */
.body-warning { 
  box-shadow: 1px 3px #f3c9c9;
  opacity: 0.6;
   
}
</style>
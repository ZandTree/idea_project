<template>
<div class="container-fluid mt-3">
      <h3 class="mb-4 text-center">Edit your Idea</h3>
      <div class="row py-3">
<!-- loader   fetch        -->
            <div class="col-xs-12 col-md-10 py-3 text-center offset-md-1">
              <app-loader v-if="isLoading"></app-loader>
            </div>        

<!-- form             -->
            <div class="col-xs-12 col-md-10 py-3 text-center offset-md-1">            
                <app-idea-form v-if="initialValues"
                  :action="edit"
                  :categories ="categList" 
                  :initial-values="initialValues"
                  :errors="servResp"                  
                  :is-submitting="isSubmitting"
                  @ideaSubmit="submitEd"
                ></app-idea-form>
                <!-- :errors="validationErrors" -->
            </div>

<!-- temp loader for downloading an image -->
            <!-- <div class="col-xs-12 col-md-10 py-3 text-center offset-md-1">
              <app-loader></app-loader>
            </div>-->
          <div class="col-xs-12 col-md-10 py-3 text-center offset-md-1">
              <app-loader v-if="loadImg"></app-loader>
          </div> 
    </div>  
  </div>
</template>

<script>
import {mapState} from 'vuex'
import AppIdeaForm from '@/components/IdeaForm'
// import AppValidationErrors from '@/components/ValidationErrors'
import {actionTypes as categActionType} from '@/store/modules/categForm'
import {actionTypes as ideaActionType} from '@/store/modules/ideaEdit'
import tagsHelp from '@/helpers/tagsHelper'

import AppLoader from '@/components/Loader'

// import mapState from 'vuex'

export default {
  name: 'AppIdeaEdit',
  components:{
    AppIdeaForm,
    AppLoader,
    // AppValidationErrors
  },
  data(){
    return {
      categList:[],
      // initial values should be computed property
      // only categ field should be pre-filled      
      edit:'edit',
      servResp:{
          status:null,
          categErr:null,
          featured:null,
          titleErr:null,
          leadTextErr:null,
          mainTextErr:null,
          // errors         
          tagsErr:null,
          thumbnailErr:null,
          netWorkErr:null,
          // err500:null,
          nonFieldErr:null,
          // err 401
          notAuthorized:null
          
        },
        // temp vars for uploading img(postpone re-direct to idea detail)
        loadImg:false      
    }
  },
  methods:{   
    submitEd(ideaInput){      
      const slug = this.$route.params.slug
     
    // this.$store.dispatch(singleIdeaActionType.getIdea,{slug:this.$route.params.slug}) 
     this.$store.dispatch(ideaActionType.editIdea,{slug,ideaInput})
     .then((resp)=>{       
       if(resp.status ===200){
        this.loadImg = true
         setTimeout(()=>{           
            this.$router.push({name:'ideaDetail',params:{slug} }) 
            // tmp loader stops after 4 sec (waiting for img upload to aws)
            this.loadImg = false                 
          },4000)
        // this.$router.push({name:'ideaDetail',params:{slug} })      
       }else if(resp.servDown){
         this.servResp.netWorkErr = 'Sorry. Our server is enduring some problems.Please try later'
       }else if(resp.status === 500){
         this.servResp.netWorkErr = 'A server/network error occured.Sorry about this - we will get it fixed shortly.'
       }else{
            // this.servResp.status = resp.status
            this.servResp.categErr = resp.categErr
            this.servResp.titleErr = resp.titleErr
            this.servResp.leadTextErr = resp.leadTextErr
            this.servResp.mainTextErr = resp.mainTextErr
            this.servResp.tagsErr = resp.tagsErr
            this.servResp.featuredErr = resp.featuredErr
            this.servResp.thumbnail = resp.thumbnailErr
            this.servResp.nonFieldErr = resp.nonFieldErr
            if(resp.status===403){
              this.servResp.noPerms = {
                noPermission:
                "Sorry.You don't have permission to to this"
              }
              this.$router.push({name:'noPerms'})
            }
            if(resp.status===400){              
              this.servResp.error400 = {
                badRequest:
                "Sorry.Error 400. Something went wrong during editing.Please try later"}

            }if(resp.status===401){
              this.servResp.notAuthorized = {
                notAuthorized:"Sorry.Your session is expired.Please login again."
              }
            }

          } 
          
         
     }).catch(err=> console.log("final err",err))
   
    }
  },
  created(){
    // fetching array of categories
    const slug=this.$route.params.slug
    this.$store.dispatch(categActionType.getCategsForm)
    .then((resp) => {
      const arrCategNames = [
        {
          text: 'Choose... ',
          value: null,
          disabled: true,
          selected: true,
        },
      ]
      resp.forEach((item) => {
        arrCategNames.push({ text: item.name, value: item.id })
      })
      this.categList = arrCategNames      
      
    })
    .catch(err=>console.log(err)),

    // fetching idea
    // const slug = this.$route.params.slug
    this.$store.dispatch(ideaActionType.getIdea,slug)
    .then((resp)=>{
      console.log(resp.status)
    }).catch(err=>console.log("can't fetch idea with this slug",err))
  },
    computed:{
          ...mapState({
              isLoading:state=>state.ideaEdit.isLoading,
              isSubmitting: state=> state.ideaEdit.isSubmitting,
              idea:state=>state.ideaEdit.idea,
              errors:state=>state.ideaEdit.servErrs
              // validationErrors: state=>state.ideaCreative.servErrs,
              // tags:state=>state.ideaCreative.data

          }),
          initialValues(){
            if(!this.idea){
              return null
              // return {categ:'',title:'',leadText:'',mainText:'',tags:'',thumbnail:'',featured:''}
            }else{
              const tagToString = tagsHelp.convertTagsListToString(this.idea.tags)
              return {
                categ:this.idea.categ,
                categName:this.idea.categ_name,
                title:this.idea.title,
                leadText:this.idea.lead_text,
                mainText:this.idea.main_text,
                featured : this.idea.featured,
                tags:tagToString,
                thumbnail:this.idea.thumbnail,
                slug:this.idea.slug,

              }
            }
          }
          
      }
  
  
}
</script>


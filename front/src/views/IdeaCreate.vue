<template>
<div class="container-fluid mt-3">
      <h3 class="mb-1 text-center">Create a new Idea</h3>
      <!-- <p>create errs:{{validationErrors}}</p> -->

      <div class="row py-3">
<!-- loader           -->
            <!-- <div class="col-xs-12 col-md-10 py-3 text-center offset-md-1">
              <app-loader v-if="isSubmitting"></app-loader>
            </div> -->
<!-- errors     -->            

<!-- form             -->
            <div class="col-xs-12 col-md-10 py-3 text-center offset-md-1">            
                <app-idea-form
                  :action="create" 
                  :categories="categories"
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
import {actionTypes as ideaActionType} from '@/store/modules/ideaCreative'
import AppLoader from '@/components/Loader'

// import mapState from 'vuex'

export default {
  name: 'AppIdeaCreate',
  components:{
    AppIdeaForm,
    AppLoader,
    // AppValidationErrors
  },
  data(){
    return {
      categories:[],
      initialValues:{
        // only categ field should be pre-filled
        categ:0,
        title:'',
        leadText:'',
        mainText:'',
        thumbnail:null,
        featured:false,
        tags:''        
        },
        create:'create',
        servResp:{
          status:null,
          categErr:null,
          featuredErr:null,
          titleErr:null,
          leadTextErr:null,
          mainTextErr:null,
          tagsErr:null,
          thumbnailErr:null,
          netWorkErr:null,
          // err500:null,
          nonFieldErr:null
        },
        // temp vars for uploading img(postpone re-direct to idea detail)
        loadImg:false      
    }
  },
  methods:{   
    submitEd(ideaInput){      
         
     this.$store.dispatch(ideaActionType.createIdea,ideaInput)
     .then((resp)=>{
       
       if(resp.slug||resp.status ===201){
          this.loadImg = true
         setTimeout(()=>{           
            this.$router.push({name:'ideaDetail',params:{slug:resp.slug} })
            this.loadImg = false                  
          },4000)
        this.$router.push({name:'ideaDetail',params:{slug:resp.slug} })      
       }else if(resp.servDown){
         this.servResp.netWorkErr = 'Sorry. Our server is enduring some problems.Please try later'
       }else if(resp.status === 500){
         this.servResp.netWorkErr = 'A server/network error occured.Sorry about this - we will get it fixed shortly.'
       }else if(resp.status === 403){
         this.servResp.nonFieldErr = 'Not authorized access'
         this.$router.push({name:'noPerms'}) 
       }else{
         
            this.servResp.categErr = resp.categErr
            this.servResp.featuredErr = resp.featuredErr 
            this.servResp.titleErr = resp.titleErr
            this.servResp.leadTextErr = resp.leadTextErr
            this.servResp.mainTextErr = resp.mainTextErr
            this.servResp.tagsErr = resp.tagsErr
            this.servResp.thumbnail = resp.thumbnailErr
            this.servResp.nonFieldErr = resp.nonFieldErr
          }       
         
     }).catch(err=> console.log("final err",err))
    //  this.loadImg = false 
    }
  },
  created(){
    this.$store.dispatch(categActionType.getCategsForm)
    .then((resp) => {
      // console.log("resp",resp)
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
      this.categories = arrCategNames
      
      
    })
    .catch(err=>console.log(err))
  },
    computed:{
          ...mapState({
              isSubmitting: state=> state.ideaCreative.isSubmitting,
              validationErrors: state=>state.ideaCreative.servErrs,
              // tags:state=>state.ideaCreative.data

          }),
          
      }
  
  
}
</script>

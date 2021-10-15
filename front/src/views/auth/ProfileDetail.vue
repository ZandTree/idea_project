<template> 
  <section class="row min-vh-100 mt-1">
      <div class="col-md-10 min-vh-100 mx-auto p-0">
        <div class="d-flex align-items-center 
                    justify-content-center 
                    flex-column
                    text-center
                    min-vh-100
                    custom-wrap">          
            <div>        
              <div v-if="!noImgShow" >                
                <img  :src="profile.image"  class="rounded-circle img-w" alt="profile image">    
                </div>
                <div v-if="noImgShow" >
                <!-- style="max-width: 100%; width: 250px; object-fit: cover"   -->
                <b-avatar size="144px"></b-avatar>
                </div>
            </div>                   
            <!-- <img  v-else alt="profile image" class="rounded-circle" src="/220px.jpg"> -->
            <h1 class="display-4">Profile: {{profile.name}}</h1>
            <div class="d-flex justify-content-between col-md-12 p-4">
<!-- people i'm following -->
              <div v-if="profile.count_following"  class="d-flex flex-column">
                <b-button v-b-toggle.collapse-1 class="m-1  btn-light">
                  Follows {{profile.count_following}}  <b-icon-diagram2-fill></b-icon-diagram2-fill>
                </b-button>                
                <!-- Element to collapse -->
                <b-collapse id="collapse-1">
                  <b-card v-for="person in profile.following" :key="person.id">
                    <router-link :to="{ name: 'profile',params:{id:person.id} }" class="link-decor">
                      {{person.username}}&nbsp;&nbsp;&nbsp; <b-avatar size="sm"></b-avatar>
                    </router-link>                    
                  </b-card>
                </b-collapse>
                <!-- <button class="btn-light m-1 rounded-corner"
                data-toggle="tooltip" data-placement="right" title="See more">
                    <b-icon-eyeglasses></b-icon-eyeglasses>
                </button>   -->                
              </div>
<!-- people following me -->
            <div v-if="profile.followers"  class="d-flex flex-column">               
              <b-button v-b-toggle.collapse-2 class="m-1  btn-light">
                Followed {{profile.count_followers}} <b-icon-diagram2></b-icon-diagram2> 
              </b-button>
              <!-- Element to collapse -->
              <b-collapse id="collapse-2">
                <b-card v-for="person in profile.followers" :key="person.id">
                  <router-link :to="{ name: 'profile',params:{id:person.user_id} }" class="link-decor">
                    {{person.username}} &nbsp;&nbsp;&nbsp;<b-avatar size="sm"></b-avatar>
                  </router-link>                  
                </b-card>
              </b-collapse>     
            </div>           
          </div>
<!-- end followers             -->
            <!-- <div class="d-flex  mx-auto"> -->
            <p class="mb-3 lead"><strong>Bio: </strong> {{profile.bio}}Lorem ipsum dolor sit amet consectetur adipisicing elit. Cum itaque nam ipsa, officia fugiat maxime molestiae voluptas explicabo error, expedita autem suscipit, accusamus eligendi obcaecati corrupti culpa veniam eos nesciunt.
            </p>
            
            <p v-if="profile.website">Website: {{profile.website}}</p>
            <p class="lead px-2" v-if="profile.image"><strong>Website:</strong>{{profile.website}}</p>
            <!-- </div> -->
           
            <button type="button" class="btn btn-success btn-lg">
              Contact
            </button>
            <div class="errMsgs mt-3">
              <div v-if="serErr500" class="warn">{{errMsg500}}</div>
            </div>
            <div class=" mt-2">
              <div v-if="netWorkErr" class="warn">{{netWorkMsgErr}}</div>
            </div>
        </div>
      </div>
  </section> 
</template>
            
<script>
import {actionTypes} from '@/store/modules/profile'
// import simpleAPI from '@/api/plainAxios'
export default {
  name:'ProfileDetail',
  data(){
      return {
          profile:{},
          netWorkErr:null,
          netWorkMsgErr:'A network error occured.Sorry about this - we will get it fixed shortly',
          serErr500:null,
          errMsg500:"A server network error occured.Sorry about this - we will get it fixed shortly"
      }
  },
  methods:{
      showProfile(){        
        this.$store.dispatch(actionTypes.retrieveProfile,this.$route.params.id)
         .then((servResp)=>{
           if(servResp.servDown){              
               this.netWorkErr = true
               return
           }else{
             const status = servResp.status              
              if(status === 200){
                console.log("status 200",status)
                this.profile = servResp.data
                // console.log(Object.keys(this.profile))
              }else if(status ===500){
                console.log("ser error 500")
                this.serErr500 = true
              }
            }
         })
         .catch(err=>console.log("final err",err))

      },
      
  },
  created(){
      this.showProfile()
      // this.showProfile({id}:{id:this.$route.params.id})
  },
  computed:{
    noImgShow(){    
      return this.profile.image===null   
    },
    currentPath() {
        //  console.log("route.path is",this.$route.path)
         return this.$route.path
        },
    
  },
  watch: {
        currentPath(){
            // console.log("watcher base url; see changes")
            this.showProfile()
        }
    },     
}
</script>
<style scoped>
.custom-wrap{
  background-color: blanchedalmond;
} 
/* button to see list of "following" */
.rounded-corner {
  border-radius: 5px;
  cursor: pointer;
}
.img-w{
  max-width: 60%;
}
.link-decor{
  text-decoration: none;
  color:black;
  cursor: pointer;
}
</style>

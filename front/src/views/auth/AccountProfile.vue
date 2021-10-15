<template>
<div>
  <section class="row min-vh-100 px-2" v-if="profile">
<!-- loader     -->
        <div class="col-xs-12 col-md-10 py-3 text-center offset-md-1">
              <app-loader v-if="isLoading"></app-loader>
        </div>
<!-- errors          -->
<!-- django server is down ect-->
            <div class="warn mb-3" v-if="error">
              <div class="px-1">{{errorMsg}}</div>              
            </div>  
            <div class="warn mb-3" v-if="err500">
              <div class="px-1">{{errMsg500}}</div>              
            </div>  
            <div class="warn mb-3" v-if="netWorkErr">
              <div class="px-1">{{netWorkMsgErr}}</div>              
            </div>  
      <ul class="nav nav-tabs">
          <li class="nav-item">
                <a class="nav-link disabled" href="#">
                    <b-avatar size="48px"></b-avatar>
                </a>
            </li>
            <!-- <li class="nav-item">
                <a class="nav-link" href="#" active-class="active">Current Profile</a>
            </li> -->
            <li class="nav-item">                
                <router-link :to="{name:'editProfile',params:{unid:profile.unid}}"
                class="nav-link" active-class="active"
                >Edit Profile
                </router-link>               
            </li>
            <!-- <li class="nav-item disabled">
                <a class="nav-link" href="#">Edit Profile</a>
            </li> -->            
      </ul>      
      <div class="col-md-8 min-vh-100 mx-auto" v-if="profile">
        <div class="d-flex align-items-center 
                    justify-content-center 
                    flex-column
                    text-center
                    min-vh-100
                    ">
            <!-- style="max-width: 100%; width: 250px; object-fit: cover"          -->            
            <div>        
              <div v-if="!noImgShow" >                
                <img  :src="profile.image" class="img-thumbnail" alt="profile image">    
             </div>
             <div v-if="noImgShow" >
              <!-- style="max-width: 100%; width: 250px; object-fit: cover"   -->
              <b-avatar size="48px"></b-avatar>
            </div>
            </div>                   
            <!-- <img  v-else alt="profile image" class="rounded-circle" src="/220px.jpg"> -->
            <h1 class="display-4">Profile: {{profile.name}}</h1>

<!-- section with 2 buttons: left "following" right "followers" -->
            <div class="d-flex justify-content-between col-md-12">
              <button class="btn-light m-1 rounded-corner"
                data-toggle="tooltip" data-placement="right" title="Edit list"
                @click="showFollowing">
                    <b-icon-pencil-square></b-icon-pencil-square>
              </button>  
              <button class="btn-light m-1 rounded-corner"
                data-toggle="tooltip" data-placement="left" title="Edit list"
                @click="showFollowers">
                <b-icon-eyeglasses></b-icon-eyeglasses>
              </button>  

            </div>
            <div class="d-flex justify-content-between col-md-12">
<!-- section people i'm following -->
            <div v-if="profile.count_following"  class="d-flex flex-column">
              <b-button v-b-toggle.collapse-1 class="mb-1 btn-light">
                Following: {{profile.count_following}} {{presentCountFollowing}} <b-icon-person-plus-fill></b-icon-person-plus-fill>
                
              </b-button>
              <!-- Element to collapse -->
              <b-collapse id="collapse-1">
                <b-card v-for="person in profile.following" :key="person.id" class="mb-1 mt-1">
                  <router-link :to="{ name: 'profile',params:{id:person.id} }" class="link-decor">
                    {{person.username}}
                  </router-link>                  
                </b-card>
              </b-collapse>                          
            </div>
            <div v-else>
              <p>Your are not following any author</p>
            </div>
<!--block  people following me -->
            <div v-if="profile.count_followers"  class="d-flex flex-column">               
              <b-button v-b-toggle.collapse-2 class="m-1  btn-light">
                Followed by: {{profile.count_followers}} 
                {{presentCountFollowers}} <b-icon-person-plus-fill></b-icon-person-plus-fill> 
              </b-button>
              <!-- Element to collapse -->
              <b-collapse id="collapse-2">
                <b-card v-for="person in profile.followers" :key="person.id" class="mt-1">
                  <router-link :to="{ name: 'profile',params:{id:person.user_id} }" class="link-decor">
                    {{person.username}} (temp var: {{person.user_id}})
                  </router-link>
                  
                </b-card>
              </b-collapse>              
            </div>
            <div v-else>
              <p>No followers yet.</p>
            </div>  
           
<!-- end following: next line-->
            </div>  
            <div class="d-flex align-items-start  flex-column text-left ">
            <p class="lead px-2"><strong>Bio: </strong> {{profile.bio}}Where am ILorem ipsum dolor sit amet consectetur adipisicing elit. Cum itaque nam ipsa, officia fugiat maxime molestiae voluptas explicabo error, expedita autem suscipit, accusamus eligendi obcaecati corrupti culpa veniam eos nesciunt.
            </p>
            <p class="lead px-2" v-if="profile.website"><strong>Website:</strong>{{profile.website}}</p>
            <p class="lead px-2" v-if="profile.image"><strong>Website:</strong>{{profile.website}}</p>
            </div>           
            <router-link :to="{name:'editProfile',params:{unid:profile.unid}}"> 
              <button type="button" class="btn btn-secondary btn-lg">Edit
            </button>
            </router-link>
            <!-- <div class="errMsgs mt-3">
              <div v-if="serErr500" class="warn">{{errMsg500}}</div>
            </div>
            <div class=" mt-2">
              <div v-if="netWorkErr" class="warn">{{netWorkMsgErr}}</div>
            </div> -->
      </div>       
    </div>    
  </section> 
  <!-- not authorized request -->
  <div v-if=!profile class="is-danger not-welcome">You are not allowed to see this page</div>
</div>
</template>
            
<script>

import {mapState} from 'vuex'
import {mapGetters} from 'vuex'
import {getterTypes} from '@/store/modules/profile'
import AppLoader from '@/components/Loader'
export default {
  name:'AccountProfile',
  data(){
    return {      
      netWorkMsgErr:'A network error occured.Sorry about this - we will get it fixed shortly',      
      errMsg500:"A server network error occured.Sorry about this - we will get it fixed shortly",
      errorMsg:"Something went wrong, probably you session has been expired and you need to login again",
      strAmountFollowers:null
    }
  },
  components:{
    AppLoader
  },
  computed:{
    ...mapGetters({
            profile:getterTypes.currentProfile
            
      }),
    ...mapState({            
            // profile:state=>state.profile.data,
            isLoading:state=>state.profile.isLoading,
            error:state=>state.profile.error,
            err500:state=>state.profile.err500,
            netWorkErr:state=>state.profile.netWorkErr  
                      
        }),
    noImgShow(){      
      return this.profile.image===null         
      },
    presentCountFollowers(){
      if(this.profile.count_followers===1){
        return "person"
      }else{
        return "persons"
      }
    },
    presentCountFollowing(){
      if(this.profile.count_following===1){
        return "person"
      }else{
        return "persons"
      }
    }
  },
  methods:{
    showFollowing(){
      console.log("display list of following")
      this.$router.push({name:'followList'})
    },
    showFollowers(){
      console.log('display my followers')
    }
  }
}
</script>
<style scoped>
/* .custom-wrap{
  background-color: blanchedalmond;
}  */
.link-decor{
  color:black;
  text-decoration:none;
}
.link-decor:hover{
  color:rgb(221, 216, 216);
}
/* button edit list of "following" */
.rounded-corner {
  border-radius: 5px;
  cursor: pointer;
}
body {
  height: 100vh;
  margin: 0; padding: 0;
}

  /* display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: row;

  font-family: 'Nunito', sans-serif;
  background-color: blanchedalmond; 

 main {
    height: 100%;
    width: 100%;

    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: row;
}
.card {
      width: 470px;
      min-height: 185px;
      display: flex;

      padding: 10px;
      border-radius: 5px;
      
      background: rgba(255, 255, 255, .8);
}
.avatar {
        width: 100px;
        height: 100px;
        margin-right: 10px;
        border-radius: 50%;
        box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
        border: 4px solid rgba(255, 255, 255, .5);
}

 */  

</style>

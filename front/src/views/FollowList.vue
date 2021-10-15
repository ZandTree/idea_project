<template>  
    <div class="container-fluid">
      <h3 class="mb-4 mt-4 text-center">Manage your list</h3>
        <div class="row py-3" v-if="profile">
          <div class="col col-md-6 py-3">
            <section class="" v-if="profile.following.length>0">
              <h4>You are following <b-badge>New</b-badge></h4>
              <div v-if="profile">
                 <b-card v-for="(person,index) in profile.following" :key="index" class="mb-2">
                   <div class="d-flex flex-wrap justify-content-between col-md-12 col-sm-6">
                  <router-link :to="{ name: 'profile',params:{id:person.id} }" class="link-decor">
                    {{person.username}}
                  </router-link> 
                  <button class="btn btn-outline-danger btn-sm mt-1" 
                    @click="unFollow(person.id,profile.following.splice(index,1))">Unfollow
                  </button>   
                   </div>              
                </b-card>
              </div>
            </section>
            <section class="" v-if="profile.following.length==0">
              <h4>You are not following other members</h4>             
            </section>
          </div>          
          <div class="col col-md-6 py-3">
            <section class="" v-if="profile.followers.length>0">
              <h4>Your ideas are followed by:&nbsp;<b-badge>{{profile.followers.length}}&nbsp;person(s)</b-badge></h4>
              <div v-if="profile">
                <b-card v-for="person in profile.followers" :key="person.id" class="mb-2">                    
                  <div class="mb-4 d-flex justify-content-between">
                    <b-avatar variant="success"></b-avatar>
                    
                    <router-link :to="{ name: 'profile',params:{id:person.user_id} }" class="link-decor">
                      <b-badge variant="dark">{{person.username}}</b-badge> 
                    </router-link>                   
                  </div>             
                </b-card>
              </div>            
            </section>
            <section class="" v-if="profile.followers.length==0">
              <h4>Your ideas are not followed by other members</h4>             
            </section>
          </div>
        </div>      
    </div>  
</template>

<script>
import AppFollow from '@/components/Follow'
import {mapGetters} from 'vuex'
import {getterTypes} from '@/store/modules/profile'
import {actionTypes} from '@/store/modules/follow'
export default {
  name:'followList',
  components:{
    AppFollow
  },
  data(){
      return {
        currentProfile:this.profile
      }
    },
  computed:{
     ...mapGetters({
            profile:getterTypes.currentProfile
            
      })
  },  
  methods:{
    unFollow(userId,id){
      this.$store.dispatch(actionTypes.unFollowUser,{userId})
      .then((resp)=>{
        // if case use keeps page open minwhile token is expired
        if(resp.status ===204){
          console.log("removing item from array via splice")
        }else if(resp.response.status===404){
          this.$router.push({name:'login'})
        }else if(resp.response.status===401){
          this.$router.push({name:'login'})
        }
      })
      .catch(err=>console.log("line 78",err))
    }
  }    
}
</script>

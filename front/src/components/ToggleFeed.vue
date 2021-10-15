<template>
    <div class="row py-2">         
         <!-- <div class="col col-md-8 py-3 mx-auto d-flex justify-content-left"> -->
         <div class="col col-md-8 py-3 mx-auto d-flex justify-content-around">
          <div class="col col-md-4 line-right sm-mod">
              <router-link :to="{ name: 'ideaGeneral' }" 
              class="link-decor px-2 py-2" :class="{'active-item px-3 py-2':routeName==='ideaGeneral'}">
                General Feed
              </router-link>
           </div>
          <div class="col col-md-4 sm-mod" v-if="isLoggedIn">
              <router-link :to="{ name: 'personalFeed' }" 
              class="link-decor px-2 py-2" :class="{'active-item px-3 py-2':routeName==='personalFeed'}">
              Personal Feed
              </router-link>
           </div>
          <div class="col col-md-4 line-left" v-if="tagSlug">
            <router-link :to="{name:'ideasBySlug',params:{slug:tagSlug}}" 
              class="link-decor px-2 py-2"
              :class="{'active-item px-3 py-2':routeName==='ideasBySlug'}"                      
            >
                <b-icon-hash></b-icon-hash>{{tagSlug}}       
            </router-link>
          </div>
        </div>
    </div>
</template>
<script>
import {mapGetters} from 'vuex'
import {getterTypes} from '@/store/modules/auth'

export default {
    name:'AppToggleFeed',
    props:{
      tagSlug:{
        type:String,
        required:false 
      }
    },
    computed:{
         ...mapGetters({
        // currentUser:getterTypes.currentUser,
        isLoggedIn:getterTypes.isLoggedIn,
        // isAnonymous:getterTypes.isAnonymous,        
        }),
        routeName(){
          return this.$route.name
        }
    },

}
</script>
<style scoped>
.line-right{
  border-right-style: solid;
  border-right-width: 1px;
  border-right-color: darkcyan;
}
.line-left{
  border-left-style: solid;
  border-left-width: 1px;
  border-left-color: darkcyan;
}
.link-decor{
  color:black;
  text-decoration:none;
}
.link-decor:hover{
  color:rgb(133, 75, 16);
}
.active-item{
  color:black;
  background-color: #4c3e3e59;
  border-radius: 5px;
  text-decoration: none;

}

@media all and (max-width:700px){
  .sm-mod{
    display: flex;
    /* flex-direction: column; */
    justify-content: center;
  }
}

</style>
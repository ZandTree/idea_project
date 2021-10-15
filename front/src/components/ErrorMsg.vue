<template>
  <div class="container">
    <div class="d-flex justify-content-center">
      <p v-if="errorSingleIdea" class="style-msg">Oops.Sorry.Something went wrong</p>
    </div>
  </div>
</template>

<script>
import {mapState} from 'vuex'
export default {
  name:'AppErrorMsg',
  props:{
        message:{
            type:String,
            required:false
        }
    },
  computed:{            
        ...mapState({            
            errorSingleIdea:state=>state.idea.error
        })
  },
  
}
</script>
<style>

.bg{
  background-color: whitesmoke;
}

</style>
<template>
    <div class="container-fluid">
      <!-- <h3 class="mb-2 text-center mt-2">This is a main idea place</h3> -->
        <app-toggle-feed></app-toggle-feed>
        <div class="row py-3">
          <div class="col col-md-2 py-3 color">
            <section class="categs-space">
              <app-categs></app-categs>
            </section>
          </div>
          <div class="col col-md-8 py-3 px-0">
            <app-idea :api-url="apiUrl"></app-idea>
          </div>
          <div class="col col-md-2 py-3 push-down color">
            <section class="tags-space p-1">             
            <app-tags></app-tags>
            </section>
          </div>
        </div>      
    </div>
</template>
<script>
import AppCategs from '@/components/categs/Categs'
import AppIdea from '@/components/Idea'
import AppTags from '@/components/Tags'
import AppToggleFeed from '@/components/ToggleFeed'

export default {
    name:'AppIdeaGeneral',
    components:{
      AppCategs,
      AppIdea,
      AppTags,
      AppToggleFeed
        
    },
    data(){
      return {
        apiUrl:'/api/v1/ideas-collection/ideas/'
      }
    }, 
    
}
</script>
<style scoped>
.row > div{
  border:1px solid black;
}

.color{
    background-color: #ffebcd;
}

</style>
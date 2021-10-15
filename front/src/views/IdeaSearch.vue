<template>
    <div class="container-fluid">
      <h3 class="mb-3 mt-2 text-center">Search results</h3>
        <div class="row py-3">
          <div class="col col-md-2 py-3">
            <!-- <div><app-loader></app-loader></div> -->
            <section class="categs-space">
              <app-categs></app-categs>
            </section>
          </div>
          <div class="col col-md-8 py-3 px-0">
            <app-idea :api-url="apiUrl"></app-idea>
          </div>
          <div class="col col-md-2 py-3">
            <section class="tags-space">             
            <app-tags></app-tags>
            </section>
          </div>
        </div>      
    </div>
</template>
<script>
import AppIdea from '@/components/Idea'
import AppTags from '@/components/Tags'
import AppCategs from '@/components/categs/Categs'
// import AppLoader from '@/components/Loader'

export default {
    name:'AppIdeaGeneral',
    components:{
        AppIdea,
        AppTags,
        AppCategs, 
        // AppLoader       
    },
    computed:{
        searchTerm() {
          return this.$route.params.term
    },
        apiUrl(){
          return `/api/v1/ideas-collection/ideas/?search=${this.searchTerm}`
    }
  }    
}
</script>
<style scoped>
.row > div{
  border:1px solid black;
}
</style>
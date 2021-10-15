<template>
  <div class="container-fluid">
        <app-toggle-feed :tag-slug="tagSlug"></app-toggle-feed>
        <div class="row">
          <div class="col col-md-2 categ-space color">
            <section class="categs-space">
              <app-categs></app-categs>            
            </section> </div>
          <div class="col col-md-8">
            <app-idea :api-url="apiUrl"></app-idea>
          </div>
          <div class="col col-md-2">
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
import AppToggleFeed from '@/components/ToggleFeed'
export default {
  name:'AppTagIdeas',
  components:{
      AppIdea,
      AppTags,
      AppCategs,
      AppToggleFeed
      
  },
  computed: {
    tagSlug() {
      
      return this.$route.params.slug
    },
    apiUrl() {
      return `/api/v1/tags-name/${this.tagSlug}/`
    }
  },
  
}
</script>
<style scoped>
.categs-space{
  height:100vh;
}
</style>

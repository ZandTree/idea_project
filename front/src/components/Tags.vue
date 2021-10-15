<template>
    <div class="color fill-color pl-1">
        <section >
            <h3>Tags: </h3>
            <div v-if="isLoading"><app-loader></app-loader></div>        
            <div v-if="tags" class="tag-list">
                <router-link v-for="tag in tags" :key="tag.id" :to="{name:'ideasBySlug',params:{slug:tag.slug}}" class="tag">
                    <b-badge variant="secondary" class="tag px-2 mx-1">{{tag.name}}</b-badge>          
                </router-link>            
            </div>
            <!-- <div  v-for="tag in tags" :key="tag.id">
                slug:{{tag.slug}}
            </div> -->
            <div v-if=error>Smth went wrong</div>
        </section>
        
    </div>    
</template>
                
                
<script>
import {actionTypes} from '@/store/modules/tags'
import {mapState} from 'vuex'
import AppLoader from '@/components/Loader'
export default {
    name:'AppTags',
    components:{
        AppLoader,
    },    
    mounted(){
        this.$store.dispatch(actionTypes.getTags)
        
    },
    computed:{
        ...mapState({
            isLoading: state=> state.tags.isLoading,
            error: state=>state.tags.error,
            tags:state=>state.tags.data

        })
    }
}
</script>
<style scoped>
.tag-list{
    display: flex;
    flex-direction: row;
    justify-content: left;
    flex-wrap: wrap;
    
}
.tag{
    color:rgb(238, 236, 232)

}
.tag:hover{
    cursor: pointer;
}
.color{
    background-color: #ffebcd;
}

</style>
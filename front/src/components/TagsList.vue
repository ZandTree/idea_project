<template>
    <div>
        <section>             
            <div v-if="tags" class="tag-list">                
                <router-link v-for="tag in tags" :key="tag.id" :to="{name:'ideasByName',params:{name:tag}}" class="tag">
                    <b-badge variant="secondary" class="tag px-2 mx-1">{{tag}}</b-badge>          
                </router-link>                                         
            </div>            
        </section>       
    </div>    
</template>                
                
<script>
export default {
    name:'AppTagsList',
    props:{
        tags:{
        required:true,
        type:Array
      },
    },
    
   
}
</script>
<style scoped>
.tag-list{
    display: flex;
    flex-direction: row;
    justify-content: right;
    flex-wrap: wrap;
    
}
.tag{
    color:rgb(238, 236, 232)

}
.tag:hover{
    cursor: pointer;
}

</style>
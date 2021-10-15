<template>
    <div class="color vh-100">
        <section class="" >                   
            <div v-if="isLoading"><app-loader></app-loader></div>        
            <div  class="d-flex flex-column">
                <div class="section-categs mb-2 pl-2">Categories:</div>
                <app-categ-tree :treeData="categs"></app-categ-tree>                       
            </div>
            <div v-if="error">Smth went wrong</div>            
        </section>
        <section>
            <app-user-filter></app-user-filter>            
        </section>
    </div>    
</template>
                
                
<script>
import AppCategTree from '@/components/categs/CatTree'

import AppUserFilter from '@/components/UserFilter'
import AppLoader from '@/components/Loader'
import {actionTypes} from '@/store/modules/categs'
import {mapState} from 'vuex'
export default {
    name:'AppCategs',
    components:{
        AppCategTree,
        AppLoader,
        AppUserFilter
    },
    created(){
        this.$store.dispatch(actionTypes.getCategs)

    },    
    computed:{
        ...mapState({
            isLoading: state=> state.categs.isLoading,
            error: state=>state.categs.error,
            categs:state=>state.categs.data

        })
    }
}
</script>
<style scoped>
/* .categ-list{
    display: flex;
    flex-direction: row;
    justify-content: right;
    flex-wrap: wrap;
    
} */
.categ{
    color:rgb(56, 43, 10)

}
.categ:hover{
    cursor: pointer;
}
.li-indent {
  padding-left: 1rem;
  margin-left: 1rem;
  background-color: red;
}
.cat-container {
  background-color: cadetblue;
}
.section-categs {
  text-align: left;
  text-decoration: none;
  list-style: none;
  padding-left: 1rem;
  /* margin-left: 1rem; */
}
.section-categs li {
  cursor: pointer;
  padding: 1rem;
}
.section-categs li:hover {
  background-color: darkcyan;
}
.color{
    background-color: #ffebcd;
}
</style>
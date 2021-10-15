<template>
  <div >
    <nav>
      <div> 
        <ul class="pagination">          
          <li class="page-list" :class="{active: currentPage === 1}">
            <router-link :to="{path: url, query: {page: 1}}" class="page-link">
                  First
            </router-link>
          </li>          
          <li v-if="prev" class="page-list">
            <router-link :to="{path: url, query: {page: currentPage-1}}" class="page-link">
                  Prev
            </router-link>
          </li>          
          <!-- start loop with pages -->
            <li v-for="page in pages"
              :key="page"            
              :class="{active: currentPage === page}"
              class="page-list">          
                <router-link :to="{path: url, query: {page: page}}" class="page-link">
                  {{ page }}
                </router-link>
            </li>
          <!-- end loop with pages -->         
          <li v-if="next" class="page-list">
            <router-link :to="{path: url, query: {page: currentPage+1}}" class="page-link">
                  Next
            </router-link>
          </li>       
          <li class="page-list">
            <router-link :to="{path: url, query: {page: last}}" class="page-link">
                  Last
            </router-link>
          </li>
                 
        </ul> 
      </div>
    </nav>
    <!-- <ul class="pagination">
      <li class="page-item disabled" :class="{active: currentPage === 1}">
            <router-link :to="{path: url, query: {page: 1}}" class="page-link">
                  First
            </router-link>
      </li>   
      <li v-if="prev"  class="page-item">
        <router-link class="page-link" :to="{path: url, query: {page: currentPage-1}}" aria-label="Previous">
            <span aria-hidden="true">&laquo;</span>
            <span class="sr-only">Previous</span>
        </router-link>
      </li>   

      <li v-for="page in pages"
              :key="page"            
              :class="{active: currentPage === page}"
              class="page-item">          
                <router-link :to="{path: url, query: {page: page}}" class="page-link">
                  {{ page }}
                </router-link>
      </li>


      <li v-if="next"  class="page-item">
        <router-link class="page-link" :to="{path: url, query: {page: currentPage+1}}" aria-label="Next">
            <span aria-hidden="true">&raquo;</span>
            <span class="sr-only">Next</span>
        </router-link>
      </li>    
      <li class="page-item">
            <router-link :to="{path: url, query: {page: last}}" class="page-link">
                  Last
            </router-link>
      </li>                  
    </ul> -->
     
  </div>
</template>

<script>
import {range} from '@/helpers/utils'
export default {
  name:'AppPagination',
  data(){
    return {
      last:null
    }
  },
  props:{
    currentPage:{
        required:true,
        type:Number
      },
    limit:{
      type:Number
    },
    total:{
      type:Number
    },
    url:{
      type:String,
      required:true
    },
    prev:{
        type:String||null,
        required:false
      },
    next:{
      type:String||null,
      required:false
    }      
    
  },  
  computed:{    
    pages() {
      const pagesCount = Math.ceil(this.total / this.limit)
      this.last = pagesCount
      return range(1, pagesCount)
    },
    nextPage(){
      return this.currentPage + 1
    }    
  },   
}
</script>

<style scoped>
/* active button */
.active a{
  color:black;
  background-color: #de692e;
  /* outline: none; */
}

/* button not active */
.page-link{
    color:black;
    border-radius:4px;
    background-color: blanchedalmond;
    margin: 3px;
    outline: none;
} 
/* not active button:hover */
.page-link:hover{
    color:black;
    border-radius:4px;
    background-color: #de692e;
    outline: none;
} 


</style>

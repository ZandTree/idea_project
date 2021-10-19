<template>
    <div class="container">        
        <div v-if="isLoading"><app-loader></app-loader></div>
        <div v-if="!ideasToDisplay&&!isLoading" 
        class="not-found h-100 d-flex justify-content-center align-items-center"
        >{{notFoundMsg}}</div>
        

        <!-- <div v-if="!ideasToDisplay">{{notFoundMsg}}</div>         -->
        <div  v-if="ideasToDisplay" class="wrapper">            
            <div class="row main-row" v-for="idea in ideas" :key="idea.id">
                <div   class="col-lg-4 col-md-12 col-sm-12">
                    <div class="idea-img mb-2">
                        <div v-if="idea.thumbnail">                            
                            
                            <img  :src="idea.thumbnail" alt="img idea" class="img-fluid" title="idea.title">
                        </div>
                        <div v-else>
                            <img src="@/assets/photos/ava_cat.jpg" alt="img" class="img-fluid">
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-sm-12 mb-2">
                            <ul class="list-group list-group-horizontal ul-cls" :disabled="isAnonymous">
                                <li class="list-group-item" data-toggle="tooltip" data-placement="top" title="Follow ideas of this author">
                                    <b-icon icon="bookmark-heart-fill"></b-icon>                                   
                                </li>                                
                                <li class="list-group-item" data-toggle="tooltip" data-placement="top" title="Author profile">
                                    <router-link :to="{name:'profile',params:{id:idea.author}}" 
                                    class="link" >
                                        <b-icon icon="person-fill"></b-icon>                                        
                                    </router-link >
                                    <!-- <span class="tooltiptext">See author profile</span> -->
                                </li>
                                <li class="list-group-item" data-toggle="tooltip" data-placement="top" title="Write msg">
                                    <b-icon icon="envelope"></b-icon>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="col-lg-8 col-md-12 col-sm-12">
                <div class="idea-title mb-1 mt-1">
                    <h3>
                       <router-link :to="{ name: 'ideaDetail',params:{slug:idea.slug} }"
                       class="link">{{idea.title}}</router-link>
                    </h3>
                </div>                
                <div class="idea-title mb-2">
                    <router-link :to="{name:'profile',params:{id:idea.author}}" class="link">
                        <p>By <b-icon icon="person-fill"></b-icon> <strong>{{idea.owner_idea}}</strong></p>
                    </router-link>
                </div> 
                <!-- <div>Featured: {{idea.featured}}</div> -->
                <div class="idea-title mb-2 ">
                    <div>
                        <p v-if="idea.avg_rate">
                        <strong>Rating: {{idea.avg_rate}}</strong>
                        </p>
                        <!-- <p v-else>
                            <strong>No rating yet</strong>
                        </p> -->
                    </div>
                </div> 
                <div class="idea-title mb-2">
                    <div>
                       <app-rating-show :rating="idea.avg_rate"></app-rating-show>
                    </div>
                </div> 
                <div class="mb-2">
                    <div class="row">
                        <div class="col-lg-9 col-md-9 col-sm-9">
                           <div class="idea-date mb-2">
                            <span>{{idea.created_at| filterDateTime}}</span>
                            </div>
                        </div>                       
                        <app-like 
                            :idea-id="idea.id"         
                            :idea-likes="idea.an_likes"  
                            :is-anonym="isAnonymous"                         
                            > 
                        </app-like>                        
                    </div>
                </div>                
                <div class="idea-main-text mb-2">
                    <p><strong>Main text: </strong> {{idea.main_text}}</p>
                </div>
                <div class="idea-main-text mb-2">
                    <p><strong>Lead text: </strong> {{idea.lead_text}}</p>
                </div>
                <div>
                <div v-if="idea.users_comments" class="idea-main-text mb-2">
                    <p><strong>Comments</strong> {{idea.users_comments}}</p>
                </div>
                <div v-else class="idea-main-text mb-2 ">
                    <p><strong>No Comments</strong></p>
                </div>
                </div>
                <div class="idea-read-more mb-2">
                    <router-link :to="{ name: 'ideaDetail',params:{slug:idea.slug} }"
                       class="idea-link">
                        <button class="btn btn-outline-dark">
                        Read More
                        </button>                       
                    </router-link>
                </div>
                <div class="idea-read-more mb-2">
                   <div v-if="idea.tags.length>0">                      
                        <div class="d-flex justify-content-left">
                          <div class="px-1">Tags:</div>
                          <app-tags-list :tags="idea.tags"></app-tags-list>                                  
                        </div> 
                      </div>                        
                </div>
              </div>
            </div>
        </div>        
        <div v-if="ideasToDisplay">
            <div >
                <div class="col-lg-8 col-md-12 col-sm-12 pagination">
                    <app-pagination  
                    :currentPage="currentPage" 
                    :total="total"
                    :limit="limit"
                    :url="baseUrl"
                    :next="next"
                    :prev="prev">
                    </app-pagination>           
                </div>
            </div>
        </div>
    </div>    
</template>
<script>

// import {parseUrl} from 'query-string'
import {stringify, parseUrl} from 'query-string'
import {mapState,mapGetters} from 'vuex'
import {actionTypes} from '@/store/modules/ideas'

import {getterTypes as authGetterTypes} from '@/store/modules/auth'
import {limit} from '@/helpers/vars'
import  AppPagination from '@/components/Pagination'
import AppLoader from '@/components/Loader'
import AppTagsList from '@/components/TagsList'
import AppLike from '@/components/Like'
import AppRatingShow from '@/components/RatingShow'

export default {
    name:'AppIdea',
    data(){
        return{
            notFoundMsg:"Sorry. No results at this moment",
            ideaLikes:0 
        }
    },
    components:{
         AppPagination,
         AppLoader,
         AppTagsList,
         AppLike,
         AppRatingShow
    },
    props:{
        apiUrl:{
            type:String,
            required:true
        }
    },
    computed:{                  
        ...mapState({
            ideas:state=>state.ideas.data,
            total:state=>state.ideas.count,
            isLoading:state=>state.ideas.isLoading,
            error:state=>state.ideas.error,
            prev:state=>state.ideas.prev,
            next:state=>state.ideas.next          
        }),
        ...mapGetters({
           isLoggedIn:authGetterTypes.isLoggedIn,
           isAnonymous:authGetterTypes.isAnonymous
        }),
        baseUrl() {
        
         return this.$route.path
        },
        currentPage() {
            // console.log("rout query page",this.$route.query.page)
            return Number(this.$route.query.page || '1')
        },
        limit(){
            return limit
        },
        offset() {
         return this.currentPage * limit - limit
        }, 
        ideasToDisplay(){
            return this.total>0                
        },
              
                  
    },    
    watch: {
        currentPage() {
            this.fetchIdeas()
        },
         baseUrl(){
            // console.log("watcher base url; see changes")
            this.fetchIdeas()
        }
    },     
    created(){
        this.fetchIdeas()   
        // console.log("islogged?",this.isLoggedIn)    
    },
    methods:{
        fetchIdeas(){
            const parsedUrl = parseUrl(this.apiUrl)
            // console.log("step 1 parsed url:",parsedUrl)
            // console.log("parsedUrl",parsedUrl)
            // console.log("parsedUrl.url:   ",parsedUrl.url)
            // console.log("parsedUrl.query:  ",parsedUrl.query)

            const stringifiedParams = stringify({
                limit,
                offset: this.offset,
                ...parsedUrl.query
            })
            const apiUrlWithParams = `${parsedUrl.url}?${stringifiedParams}`
            console.log('apiUrlWith',apiUrlWithParams)
            
            this.$store.dispatch(actionTypes.getIdeas, {apiUrl: apiUrlWithParams})
                  
            },
        
    },    
    
    filters: {
    // Filter full date with (local+) time
    // 2020-07-23 20:41:43.833825
    filterDateTime(item) {
      let initialDate = new Date(item);
    //   initialDate.getMonth() + 1
      const months = ['Jan','Feb','March','April','May','June','July','Aug','Sept','Oct','Nov','Dec']
      const currentMonth = months[initialDate.getMonth()]
      return `
          ${initialDate.getDate()} ${currentMonth} ${initialDate.getFullYear()}-${initialDate.getHours()}:${initialDate.getMinutes()} UTC ${initialDate.getUTCHours()}:${initialDate.getMinutes()}`;
    },
    }    
}
</script>
<style>
/* search without results msg */
.not-found{
    background-color: #e9ecefbf;
    font-size: 2rem;
    


}

.main-row{
    margin:8%;
    background-color: blanchedalmond;
    box-shadow: 0 0 10px 10px rgba(0,0,0,.05);
    border-radius: 0.5rem;
}
.idea-img   >   img{
    width:100%;
    height:100%;
    /* transform: translateY(-30px); */
    object-fit: cover;
    border-radius:0.5rem;
    box-shadow: 0 0 8px 3px rgba(0,0,0,.3);
}
/* @media all and (max-width:700px){
  .idea-img > img{
    
  }
} */

.idea-date span{
    font-weight: 700;
}
.ul-cls{
    justify-content: center;
}
.ul-cls li{
    cursor: pointer;
}
.idea-title >h3{
    font-weight: 400;
    font-style: normal;
}
.idea-main-text{
    font-style: normal;
    line-height: 2;
}
/* tooltip */
.tooltip {
  position: relative;
  display: inline-block;
  border-bottom: 1px dotted black;
}

.tooltip .tooltiptext {
  visibility: hidden;
  width: 120px;
  background-color: black;
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 5px 0;
  
  /* Position the tooltip */
  position: absolute;
  z-index: 1;
  top: -5px;
  left: 105%;
}

.tooltip:hover .tooltiptext {
  visibility: visible;
}
/* .idea-link{
    text-decoration:none;
    cursor: pointer;
    color:rgb(38, 44, 38)

}
.idea-link:hover{
    text-decoration:none;
    cursor: pointer;
    color:rgb(185, 221, 185)

} */
/* likes */
.click-like{
  cursor: pointer;
  padding:6px;
}
.link{
  color:black;
  text-decoration:none;
}
.link:hover{
  color:rgb(33, 98, 84);
  text-decoration: none;
}
@media all and (max-width:700px){
  .pagination{
    display: flex;
    flex-flow: wrap;
  }
}

</style>
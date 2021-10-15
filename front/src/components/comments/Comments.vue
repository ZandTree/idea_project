<template>
    <div>
        <section class="row top">                   
            <div v-if="isLoading" class="col-md-12">
                <app-loader></app-loader>
            </div>
                <!-- <div v-if="activeComment">To delete... active component now is: {{activeComment}}</div>
                <div v-if="!activeComment">To delete... active component now is null</div> -->

            <div class="col-md-12" v-if="isLoggedIn">
                <div class="d-flex justify-content-center">
                <b-button @click="openForm" variant="secondary">Write Comment</b-button>
                </div>
                
                
                <div v-if="goWrite" class="col-md-12">
                    <app-comment-form
                    submitLabel="Write"
                    :active-comment="activeComment" 
                    :hasCancelButtonRoot=true
                    :clean-form = "cleanForm"
                    @handleCancelRootComment="handleCancelRoot"
                    @addRootComment="addRootComment">
                    </app-comment-form>
                 </div>
                
            </div>        
            <div  class="comment-list mt-2 ml-2 col-md-12">
                <div class="section-comments">
                    <!-- <h4>Comments</h4>                 -->
                    <div v-if="warning" class="flesh-msg-error">{{warning}}</div>                         
                </div>                              
                <app-comment 
                v-for="comment in getRootComms"
                :key="comment.id"
                :comment="comment"
                :parent-id="comment.id"
                :reply-to-id="comment.reply_to_id"
                :active-comment="activeComment"                
                :comments="comments"
                :depth=1
                @replyComment="replyComment"
                @updateComment="updateComment"
                @commEdit="handleEdit"
                @commReply="handleReply"
                @commDelete="handleDelete"
                @handleCancel="handleCancel"                
                ></app-comment>                               
            </div>
            <div v-if="error" >Msg from store: smth went wrong</div>                 
        </section>
    </div>    
</template>

<script>
import AppCommentForm from '@/components/comments/CommentForm.vue'
import AppComment  from '@/components/comments/Comment'
import AppLoader from '@/components/Loader'
import {actionTypes} from '@/store/modules/comments'
import {mapState} from 'vuex'
import {mapGetters} from 'vuex'
import {getterTypes} from '@/store/modules/auth'

export default {
    name:'AppCommentList',
    components:{       
        AppLoader, 
        AppComment,
        AppCommentForm,
               
    },
    data(){
        return {
            activeComment:null,
            cleanForm:false,
            warning:'',
            // hasCancelButton:false 
            goWrite:false,
            hasCancelButtonRoot:false           
        }
    },
    props:{        
        ideaId:{
            type:Number,
            required:true
        },
        ideaSlug:{
            type:String,
            required:true
        },
        currentUser:{
            type:Object,
            required:false
        }        
    },
    created(){       
      this.$store.dispatch(actionTypes.fetchCommentList,this.ideaSlug)
        
    },
    methods:{
        // methods to set active comment 
        handleReply(commId){           
            this.activeComment={id:commId,type:'replying'}
            //console.log("parent sets type",this.activeComment.type)
        },
        handleEdit(commId){            
            this.activeComment={id:commId,type:'editing'}
            //console.log("parent sets type",this.activeComment.type)
        },
        handleDelete(commId){
            this.activeComment={id:commId,type:'deleting'}
            //console.log("parent delete comm ",commId)
            this.deleteComment(commId)
        },
        openForm(){            
            this.goWrite = true
            this.activeComment={id:null,type:'writing'}             
        },        
        
        handleCancel(){            
            this.activeComment = null            
        }, 
        handleCancelRoot(){
            console.log("root cancel")
            this.activeComment = null
            this.cleanForm=true
            this.goWrite=false
        }, 
        replyComment(replyComment){
                     
            let commentData = {
                body: replyComment.body,
                idea:this.ideaId,
                parent:replyComment.parent,
                }
                
                this.$store.dispatch(actionTypes.sendRootComm,commentData)
                .then((resp)=>{
                
                this.activeComment = null
                
                })
                .catch(err=>console.log(err))    
        },       
        addRootComment(data){
            console.log("adding root comment...")        
            // let user = this.currentUser
            let commentData = {
                body: data.body,
                // user: user,
                idea:this.ideaId,
                parent:null,
                }
                console.log("data",commentData)
                this.$store.dispatch(actionTypes.sendRootComm,commentData)
                .then((resp)=>{                
                    if(resp.status===201){                        
                        this.activeComment=null
                        this.cleanForm = true
                        this.goWrite = false                        
                    }
                    if(resp.status===400&&resp.body===undefined){
                        // from store custom msg(status:400,body:undefined)
                        this.warning = 'comment can not be empty'                        
                        setTimeout(()=>{
                            this.warning = ''                    
                        },2000) 
                    }                    
                 })
                .catch((err) =>{
                    console.log(err)
                    
                })        
        },        
        updateComment(data){            
            this.$store.dispatch(actionTypes.editComm,data)
                .then((resp)=>{                
                if(resp.status===403){                    
                    this.warning = "Permission denied"                }
                    this.activeComment=null                    
                })
                .catch(err=>console.log(err))        
        }, 
        deleteComment(commId){
            this.$store.dispatch(actionTypes.deleteComm,commId)
            .then((resp)=>{
                console.log(resp)               
            })
            .catch(err=>console.log(err))
        },
             
    },    
    computed:{
        ...mapState({
            isLoading: state=> state.comments.isLoading,
            error: state=>state.comments.error,
            comments:state=>state.comments.data,
            fladToRednder:state=>state.comments.flagRerender
        }),
         ...mapGetters({        
            isLoggedIn:getterTypes.isLoggedIn,       
        
        }),
        getRootComms(){
            // console.log(this.comments.filter(comm=> comm.parent === null))
            // console.log("length root:",this.comments.length)
            if(this.comments){
                return  this.comments.filter(comm=> comm.parent === null)

            }else{
                return []
            }        
        },
        
    },
    
}

</script>
<style scoped>
.section-comments {
  text-align: left;
  text-decoration: none;
  list-style: none;
  /* to display error msg better */
  /* padding-left: 1rem;
  margin-left: 1rem; */
}
.warning{
    background-color: rgb(240, 228, 230);
    max-height: 150px;
    max-width: 100%;
    border-bottom-color: red;  

}
@media only screen and (max-width: 768px) {
  /* For mobile phones: */  
  .row{
    margin-right: 0rem;
  }
  .top{
      width: 100%;
  }
  
}

</style>
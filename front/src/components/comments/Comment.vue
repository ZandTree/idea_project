<template>
<!-- user can see a comment -->
<!-- auth user&&author comment can edit comment /cancel editing-->
<!-- auth user&&author comment can delete comment -->
<!-- auth user can reply on a comment-->
  <div class="mr-1 pr-1 no-right">
 <!-- start render if comment not deleted     -->
     <div v-if="!comment.deleted" class="label-wrapper ">
        <div class="row">                    
         <div class="comment-wrap mw-100">
<!-- comment-menu(top)            -->
        <div div class="">
          <div class="row pt-2">
            <div class=" col-md-6 author-space-creds col-sm-12">   
                <div class="px-2"><b-icon-person></b-icon-person></div>             
                <p class="pl-1 mr-2 px-2">Written by: <strong>{{comment.author_comment}}</strong></p>
                <p v-if="comment.name_recepient" class="pl-1 mr-2 px-2">Reply to: <strong>{{comment.name_recepient}}</strong></p>

            </div>
            <div class="col-md-6 col-sm-12 author-space-action">   
                <template v-if="currentUser&&currentUser.id==comment.user_id">
                  <div class="pl-1 ml-4 edit" @click="commEdit(comment.id)"><b-icon-pencil></b-icon-pencil></div>
                  <div class="pl-1 ml-4 trash"  @click="showModal"><b-icon-trash></b-icon-trash></div>
                </template>
            </div>
          </div> 
          <div class="row mb-2">  
            <div class="col-md-12">    
              <div class="comment-date">
                Posted on: <strong>{{comment.created_at|filterDateTime}}</strong>
              </div>
              
            </div>      
          </div>
        </div>   
<!-- if comment not deleted you may:             -->
  <!-- if just show comment body  -->
        <div v-if="!comment.deleted">
          <div v-if="!isEditing" class="col-sm-12 ">
            <p class="">{{comment.body}} </p>  
            <!-- <p>Temp comm iD <strong>{{comment.id}}</strong></p>
            
            <p v-if="!parentId===null">Temp parent id {{parentId}}</p>
            <p v-if="parentId===null">Temp parent id is null</p> -->
          </div>           
            
  <!-- if editing -->
            <div v-if="isEditing" class="col-md-12">
              <app-comment-form
              submitLabel="Edit"          
              :hasCancelButton=true
              :initial-body="comment.body"
              @updateComment="updateComment"
              @handleCancel="handleCancel"              
              >
              </app-comment-form>  
            </div>
  <!-- if reply(ing) -->
            <div v-if="isReplying">
               <app-comment-form
              submitLabel="Reply"
              :hasCancelButton=true
              :parent-id="comment.id"
              :reply-to-id="comment.reply_to_id"              
              @reply="replyComment"
              @handleCancel="handleCancel"              
              >
              </app-comment-form> 
            </div>
            <div v-if="isLoggedIn" class="d-flex justify-content-left col-md-12 mb-2">                
                <button class="btn btn-outline-success mb-2" 
                        @click="commReply(comment.id)"
                        :class='makeButtonInvisible?"hideButton":""'>
                    Reply
                </button>               
            </div>
          </div> 
<!--end if comm not deleted-->          
        </div>
      </div> 
     </div> 
<!--end if comment not deleted-->

<!-- start render section if comment deleted -->
      <div v-if="comment.deleted" class="comment-wrap-deleted mt-1 mb-1 mr-4">
      <div>Comment deleted</div>
      </div>
<!-- end section render deleted comment     -->
<!-- start render if comment has replies: Instagram stile == "onle one indentation defined by var indent
see computed -->
    <div v-if="replies&&replies.length>0" class="mt-2" :style="indent">
        <app-comment 
          v-for="comment in replies"
          :key="comment.id"
          :comment="comment"
          :parent-id="comment.id"
          :reply-to-id="comment.reply_to_id"
          :active-comment="activeComment" 
          :comments="comments"
          :depth=0               
          @replyComment="replyComment"
          @updateComment="updateComment"
          @commEdit="commEdit"
          @commReply="commReply"
          @commDelete="commDelete"
          @handleCancel="handleCancel"                
          >
        </app-comment>          
    </div>
      
<!-- The Modal -->
    <div class="modal-bg" v-if="showConfirmDelete">
        <div class="confirm-modal">         
          <button type="button" class="btn-close" @click="close"></button>
          <header class="modal-header">
            <!-- <h5>Warning</h5> -->
          </header>
          <section class="modal-body">
            <h6>Do you really want to delete this comment?</h6>          
          </section>
          <section class="modal-footer"> 
            <button class="btn btn-sm btn-danger" @click="commDelete(comment.id)">
              Yes,I want to delete this comment
            </button>        
            <button type="button" class="btn-green rounded" @click="close">Cancel</button>
          </section>
      </div>
    </div>
  </div>        
</template>

<script>
import {mapGetters} from 'vuex'
import {getterTypes} from '@/store/modules/auth'
import AppCommentForm from '@/components/comments/CommentForm.vue'


export default {
  components: { 
    AppCommentForm,      
    AppComment: () => import('@/components/comments/Comment')
    },
    data(){
      return {
        showConfirmDelete:false, 
        makeButtonInvisible:false       
      }
    },
    props: {
        comment:{          
          type:Object,          
          },
        activeComment:{
          type:Object||null
        },
        parentId:{
          type:Number
        },
        replyToId:{
          type:Number||null
        },
        comments:{
          type:Array
        },
        depth:{
          type:Number
        }         
    }, 
    methods:{  
      // methods to pass id to the parent about current(active) comment    
        commReply(commId){
            
            this.makeButtonInvisible = true
            this.$emit('commReply',commId)
        },
        commEdit(commId){
            
            this.makeButtonInvisible = true
            this.$emit('commEdit',commId)
        },
        commDelete(commId){            
            this.makeButtonInvisible = true
            this.showConfirmDelete = false
            this.$emit('commDelete',commId)
        },
        updateComment(commentBody){
          // attr 'body' edited in form
          //here attr 'id' added
            // check if commentBody does not have id ( otherwise perm denied)=> goes to recurs level 
            // and will change id for parent id
            if(!commentBody.id){
              commentBody.id=this.comment.id

            }
            
            this.$emit('updateComment',commentBody)
        },
        replyComment(commentData){          
            
          this.$emit('replyComment',commentData)
        },
        onSubmit(commentData){
            this.$emit('onSubmit',commentData)
        },
        handleCancel(){
            console.log("comment handling cancel")
            this.$emit('handleCancel')
        },
        close() {
          
          this.showConfirmDelete = false;
        }, 
        showModal(){
          this.showConfirmDelete = !this.showConfirmDelete
        }      

  },
  computed:{
     ...mapGetters({
          currentUser:getterTypes.currentUser,
          isLoggedIn:getterTypes.isLoggedIn,
          
        }),  
    isReplying(){
        console.log()
        return this.activeComment&&this.activeComment.id===this.comment.id&&this.activeComment.type==='replying'
    },
    isEditing(){
        return this.activeComment&&this.activeComment.id===this.comment.id&&this.activeComment.type==='editing'
    },
    isDeleting(){
      return this.activeComment&&this.activeComment.id===this.comment.id&&this.activeComment.type==='deleting'
    },
    getReplyId(){
      return this.parentId?this.parentId:this.comment.id
    },
    replies(){
      // console.log(this.comments.filter(comm=>comm.parent===this.parentId))
          return this.comments.filter(comm=>comm.parent===this.parentId).sort(
            (a,b)=>new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
          )           
        },
    indent() {
      return { transform: `translate(${this.depth * 50}px)` };
    },    
  },
  filters: {
    // Filter full date with (local+) time
    // 2020-07-23 20:41:43.833825
    filterDateTime(item) {
      let initialDate = new Date(item);
      const months = ['Jan','Feb','March','April','May','June','July','Aug','Sept','Oct','Nov','Dec']
      const currentMonth = months[initialDate.getMonth()]
      return `
          ${initialDate.getDate()} ${
        currentMonth
      } ${initialDate.getFullYear()} at ${initialDate.getHours()} H : ${initialDate.getMinutes()} min
      (UTC: ${initialDate.getUTCHours()} h ${initialDate.getMinutes()} min)`;
    },
    }    
};
</script>
<style scoped>
.label-wrapper {
  padding-bottom: 10px;
  margin-bottom: 10px;
  border-radius: 10px;
  /* border-bottom: 1px solid #ccc; */
  
}
.comment-form-invisible{
  display: none;
}
.hideButton{
  display: none;
}
.show-comment-form{
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  min-height: 100px;
  max-width: 100%;
  padding: 0.5rem 1rem;
  border:1px solid black;
}
/* comment button */
input[type=submit] {
  background-color: #e2cca8;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
input[type=submit]:hover {
  background-color: #d1860c;
}
input[type=text],  textarea {
  width: 100%; 
  padding: 12px; 
  border: 1px solid #ccc;
  border-radius: 4px; 
  box-sizing: border-box;
  margin-top: 6px; 
  margin-bottom: 16px; 
  resize: vertical;
  outline:none;
  /* for scroll-bar in IE */
  overflow: auto;  
}
/* textarea focus {background-color:#000;color:#FFF;} */
/* main div for all comments */
.comment-wrap{
  background-color: #4c524c22;
  border-radius: 10px; 
}
.comment-wrap-deleted{
  background-color: #4c524c22;
  border-radius: 10px; 
  padding:1rem;
}
.comment-date{
  font-size: 0.8rem;
  font-weight: 400;
}
/* div user name */
.author-space-creds{
  display: flex; 
}
.author-space-action{
  display: flex;
  justify-content: space-evenly;
}
@media only screen and (max-width: 768px) {
  /* For mobile phones: */
  .author-space-action{
    display: flex;
    justify-content: flex-start;
    margin-bottom: 1rem;
  }
  .edit{
    margin-left: 0.5rem;
  }
  .row{
    margin-right: 1rem;
  }
  .no-right{
    margin-right: 0;
    padding-right: 5px;
    width:100%;
  }
  
  
}

/* edit and trash action */
.edit,.trash {
  cursor: pointer;
}

.replies {
  background-color: rgb(240, 228, 224);
}
/* modal styles */
.modal-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 99;
  /* normal css flow  to hide element*/
  /* visibility: hidden;
  opacity: 0; */
}
.confirm-modal {
  background-color: rgb(245, 231, 218);
  width: 50%;
  /* otherwise pop-up with too long body */
  /* height: 50%; */
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-direction: column;
  position: relative;
}
.modal-header,
.modal-footer {
  padding: 15px;
  display: flex;
}
.modal-header {
  /* position: relative; */
  border-bottom: 1px solid #eeeeee;
  color: rgb(224, 55, 55);
  /* color: #4aae9b; */
  justify-content: space-between;
}
.modal-footer {
  border-top: 1px solid #eeeeee;
  display: flex;
  align-items: center;
  justify-content: space-around;
}
.modal-body {
  position: relative;
  padding: 20px 10px;
  z-index: 1;
}
.btn-close {
  position: absolute;
  top: 10px;
  right: 10px;
  /* background-color: burlywood; */
  /* border: none;
  font-size: 20px;
  padding: 10px;
  cursor: pointer;
  font-weight: bold;
  color: #4aae9b;
  background: transparent; */
}
.btn-green {
  color: white;
  background: #4aae9b;
  border: 1px solid #4aae9b;
  border-radius: 2px;
}
</style>

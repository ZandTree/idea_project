<template>    
 <div>  
    <button type="button" 
                id="like-button"
                @click="doLike"
                :class="{'disabled':isAnonym, 
                        'btn-outline-secondary':likeToToggle,
                        'btn-outline-success':!likeToToggle
                }"
                data-toggle="tooltip" data-placement="right" title="Please login to Like"
                > 
            <div class="d-flex jsustify-content-between">               
            <b-icon-heart-fill></b-icon-heart-fill>            
            <div class="px-2">
                <span class="px-0" v-if="likeStatus===null">{{ideaLikes}}</span>
                <span class="px-0" v-else>{{newLikeVal}}</span>            
            </div>  
            </div>
     </button>     
    <p v-if="needAuthMsg" class="warning">{{needAuthMsg}}</p>         
 </div>
</template> 

<script>
import {actionTypes} from '@/store/modules/singleIdea'
export default {
    name:'Like',
    props:{
        ideaId:{
            type:Number,
            required:true
        },
        ideaLikes:{
            type:null||Number,
            // required:true
        },
        isAnonym:{
            type:Boolean,
            required:false
        }
        
    },
    data(){
        return{        
            likeToToggle:null, 
            initialLikeState:null,        
            newLikeVal:this.ideaLikes,
            likeStatus:null,
            needAuthMsg:null,
            localNewLike:{count:null,initialAction:null}       
        }
    },
    methods:{
        async doLike(){
            if(this.isAnonym){
                console.log('hi, anonym')                
                return
            }
            // console.log("initial like",this.likeToToggle)
            this.likeToToggle = !this.likeToToggle
            // console.log("dus i send != state of like",this.likeToToggle)
            const likeInfo = {
                        like:{"like":this.likeToToggle},
                        id:this.ideaId
            };
            this.$store.dispatch(actionTypes.handleLike,likeInfo)
            .then((servResp)=>{
                if(servResp.status===200){
                    this.likeStatus = servResp.data.like
                    console.log("dj server confirms data in db",this.likeStatus)
                    if(this.likeStatus===true){
                        // console.log("like plus: +=")   
                        this.newLikeVal ++                   
                    }else{
                        // console.log("minus like:-=")
                        this.newLikeVal -= this.newLikeVal                                            
                    }  
                    // this.likeStatus = !this.likeStatus             
                    
                    
                }else if(servResp.status === 401){
                    console.log("you are not auth-ed????")
                    this.needAuthMsg = 'Please, login'                 
                    setTimeout(()=>{
                        this.needAuthMsg = null
                },4000)
                }        
            }).catch(err=>console.log("err in like",err))        
        
            },
        async getInitialLikeState(){
            // console.log("requesting initial like state",this.ideaId)
            this.$store.dispatch(actionTypes.getLikeState,this.ideaId)
            .then((servResp)=>{
                if(servResp.status===200){
                    this.likeToToggle = servResp.data.like
                }
            })
            .catch(err=>console.log(err))
        } 

    },
    created(){
        if(!this.isAnonym){
        this.getInitialLikeState()
        }
    }
}
         

</script>
<style scoped>

#like-button {
  color: rgb(236, 34, 34);
  font-size: 1.0em;
  font-family: 'Heebo', sans-serif;
  background-color: transparent;
  border: 0.1em solid;
  border-radius: 1em;
  padding: 0.333em 1em 0.25em;
  line-height: 1.2em;
  /* box-shadow: 0 0.25em 1em -0.25em; */
  cursor: pointer;
  transition: color 150ms ease-in-out, background-color 150ms ease-in-out, transform 150ms ease-in-out;
  outline: 0;
  margin: 1em 0;
}  
#like-button:hover {
    color: rgb(240, 170, 170);
  }

/* like button on mob */
 @media (max-width: 575.98px){
  #like-button{
        
        font-size: 1.0em;
        font-family: 'Heebo', sans-serif;
        background-color: transparent;
        border: 0.1em solid;
        border-radius: 1em;
        padding: 0.333em 0.9em 0.25em;
        line-height: 0.8em;
        /* box-shadow: 0 0.25em 1em -0.25em; */
        cursor: pointer;
        transition: color 150ms ease-in-out, background-color 150ms ease-in-out, transform 150ms ease-in-out;
        outline: 0;
        margin: 0.5em 0;
    }
  
}
#like-button:active {
    transform: scale(0.95);
  }
  
#like-button .selected {
    color: white;
    background-color: rgb(243, 236, 236);
    border-color: red;
}
  
.heart-icon {
    display: inline-block;
    fill: currentColor;
    width: 0.8em;
    height: 0.8em;
    margin-right: 0.2em;
}

.click-like{
  cursor: pointer;
  padding:3px;
  
}
.zoo{
    display: flex;
    flex-direction: column;
    justify-content: center;

}
.warning{
    background-color: rgb(236, 215, 207);
    border-radius: 5px;
    padding: 3px 10px;
}

</style>
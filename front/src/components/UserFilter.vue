<template>
    <div id="checkboxes"> 
        <form @submit.prevent="sortIt">
            <p>Sort</p>
            <div class="form-check">
                <input class="form-check-input" type="radio" v-model="userChoice" value="rateOnTop"
                id="zTop" active-class="active">
                <label class="form-check-label" for="zTop">
                    Highest Rating  to top
                </label>
            </div>
             <div class="form-check">
                <input class="form-check-input" type="radio" v-model="userChoice" value="oldOnTop"
                id="oldTop" active-class="active">
                <label class="form-check-label" for="oldTop">
                    Oldest on top
                </label>
            </div>      
            <div class="form-check">
                <input class="form-check-input" type="radio" v-model="userChoice" value="newOnTop" 
                id="newTop" active-class="active">
                <label class="form-check-label" for="newTop">
                    Newest op top 
                </label>
            </div>             
            <div class="form-check">
                <input class="form-check-input" type="radio" v-model="userChoice" value="aOnTop" 
                id="aTop" active-class="active">
                <label class="form-check-label" for="aTop">
                    A to top 
                </label>
            </div>
            <div class="form-check">
                <input class="form-check-input" type="radio" v-model="userChoice" value="zOnTop"
                id="zTop" active-class="active">
                <label class="form-check-label" for="zTop">
                    Z to top
                </label>
            </div>
            
            <p>Filter</p>
                <div class="input-group mb-3">
                    <div class="input-group-prepend">
                        <div class="input-group-text">
                        <input v-model="featurePlus" value="True" type="checkbox" aria-label="Featured">
                        </div>
                    </div>
                    <input type="text" class="form-control" aria-label="Text input with checkbox"
                    placeholder="Featured">
                </div>
            <div class="">
            <b-button  size="sm" class="my-2  mx-2 mt-2" type="submit">Search</b-button>       
            <b-button  size="sm" class="my-2  mx-2 mt-2 btn-success" @click="reset">Reset filter </b-button>       

            </div>
        </form>
    </div>
</template>
<script>
export default {
    name:'AppUserFilter',
    data(){
        return {
            userChoice:null,
            featurePlus:false                     
        }
    },
    computed:{
        passUserChoice(){
            if(this.userChoice==='oldOnTop'){
                return "created_at"
            }else if(this.userChoice ==='newOnTop') {
                return "-created_at"
            }        
            else if(this.userChoice==='aOnTop'){
                return "title"
            }else if(this.userChoice==='rateOnTop'){
                return "max_rating"
            }else if(this.userChoice ==='zOnTop') {
                return "-title"            }
            else{
                return '-created_at'
            }
        },
        showFeatured(){
            return this.featurePlus
                                  
        }
    },
    methods:{
        sortIt(){          
            // console.log("param to url for ordering:",this.passUserChoice)
            this.$router.push({name:'filter',params:{sort:this.passUserChoice,featured:this.showFeatured}}) 
        },
        reset(){
            this.userChoice=null,
            this.featurePlus=false,
            this.onFront=null
        }
    }
}
</script>
<style scoped>
.buts{
    display: flex;
    flex-wrap: wrap;
}
</style>
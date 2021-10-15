<template>
    <div>               
        <div class="stars-container"> 
            <div v-if="!rating" class="stars-container">
                <p class="px-1"><b-icon-star></b-icon-star></p>
                <p class="px-1"><b-icon-star></b-icon-star></p>
                <p class="px-1"><b-icon-star></b-icon-star></p>
                <p class="px-1 "><b-icon-star></b-icon-star></p>
                <p class="px-1"><b-icon-star></b-icon-star></p>
                
            </div> 
            <div v-if="rating>0"   class="stars-container">
                <div class="px-1" v-for="star in roundedRating" :key="star.id">
                    <div>
                        <b-icon-star-fill></b-icon-star-fill>
                    </div>
                </div>
                <div v-if="floatFlag">
                    <div>
                        <b-icon-star-half></b-icon-star-half>
                    </div>
                </div>
                <div v-if="addEmptyStars" class="stars-container">
                    <div class="px-1" v-for="star in addEmptyStars" :key="star.id">
                        <p>
                            <b-icon-star></b-icon-star>
                        </p>
                    </div>
                </div>
            <!-- <p>Rating (based on ...ratings) </p>                   -->
            </div> 
        </div>              
    </div>
</template>

<script>
export default {
    name:"AppRating", 
    // rating == string
    props:['rating'],   
    computed:{
        
        parseRating(){
            return  Number(this.rating)
        },
        roundedRating(){
            // console.log("to the floor",Math.floor(this.parseRating))
            return Math.floor(Number(this.parseRating))
        },
        addEmptyStars(){
            if(this.floatFlag){
                return 5-this.roundedRating-1
            }else{
                return 5-this.roundedRating
            }
        },
        floatFlag(){
            
            return !Number.isInteger(Number(this.rating))
        }
        
        
        
    },
    methods:{
        
    }
    
}
</script>
<style scoped>
.stars-container{
    display: flex;
    justify-content: flex-start;
    
}
.point{
    cursor: pointer;
}
</style>
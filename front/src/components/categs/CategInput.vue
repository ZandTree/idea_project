<template>
    <div>        
        <b-form-group
            id="input-group-11"            
             class="text-left">
            <label for="input-11" class="control-label">Category</label>                    
            <b-form-select
            id="input-11"
            v-model="category"
            :options="setCategNames"                
            @change="catVal">                       
            
            </b-form-select>
        </b-form-group> 
        
        
      </div>
</template>         
          

<script>
    export default {
        name:"AppCategInput",
        props:{
            placeholder: { type: String },
            setCategNames: { type: Array },
            categ:{
                type:Number,
                required:true
            },
            
        },
        data(){
            return {
                category:this.categ
            }
        },         
        
        methods:{
            catVal(){
                this.$emit('getCateg', this.getCateg);
            }
        },
        computed:{
            getCateg(){
                return this.category
            }
        }
        
    }
</script>
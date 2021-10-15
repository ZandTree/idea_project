<template>
  <div class="error-section">    
    <ul class="error-messages">
      <li v-for="errorMessage in errorMessages" :key="errorMessage" class="warning">
        {{ errorMessage }}
      </li>
    </ul>
  </div>
</template>

<script>
/*
{ "title": [ "This field may not be blank." ], "mainTextErr": [ "This field may not be blank." ], "nonFieldErrs": { "title": [ "This field may not be blank." ], "main_text": [ "This field may not be blank." ] } }



*/

export default {
  name:'AppErrorMsg',
  props:{
        validationErrors:{
            type:Object,
            required:true
        }
    },
    computed: {
    errorMessages() {
      console.log("this val errs",this.validationErrors)
      return Object.keys(this.validationErrors).map(item => {
        const messages = this.validationErrors[item].join(', ')

        return `${item} ${messages}`
      })
    }
  }
  
}
</script>
<style scoped>
.warning{
  color:brown
}
</style>

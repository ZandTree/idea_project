<template>
    <div class="container">
        <div class="row mt-4 main-box">            
            <div class="col col-md-10" >
                <div class='container'>
                    <div class="wrapper">
                        <h5>Please check your 
                            email address: <strong>{{showEmailCheck}}</strong> to see the link to confirm
                            this email
                            <!-- extra {{store.state.autj.showEmailCheck}} -->
                        </h5>  
                                          
                    </div>                    
                </div>                
            </div>
        </div>
    </div>           
</template>
<script>
export default {
    name:'AppConfirmEmail',
    computed:{
        showEmailCheck(){
            return this.$store.state.auth.showEmail.email;
        }
    }    
}
</script>
<style scoped>
.main-box {

  padding:2rem;
  background-color: blanchedalmond;
  box-shadow: 0 0 10px 10px rgba(0,0,0,.05);
  border-radius: 0.5rem;
} 
</style>
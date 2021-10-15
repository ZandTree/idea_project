<template>
    <div class="container">
        <div class="row mt-4">            
            <div class="col col-md-10 col-sm-10" >
                <div class='container'>
                    <div class="wrapper">
                        <!-- will be displayed when django server is down -->
                        <h5 v-if="netWorkErr">
                            Our server is enduring some problems.Sorry about this - we will get it fixed shortly. </h5>
                        <h5 v-if="incorrectEmail">Sorry, something went wrong during password reset proccess.
                            Check whether your email address correct.
                            <!-- Check whether your email address {{showEmail}} correct. -->
                            If you need help, please contact us : support@mail.com
                        </h5> 
                        <p class="mt-3">
                            Home <router-link :to="{name:'home'}">back to home</router-link>
                        </p>  
                                          
                    </div>                    
                </div>                
            </div>
        </div>
    </div>           
</template>
<script>
import {mapState} from 'vuex'
export default {
    name:'AppPswRestFailure',    
    computed:{
        computed:{
        ...mapState({
            isLoading:state=>state.auth.isLoading,
            netWorkErr:state=>state.auth.netWorkErr,
            incorrectEmail:state=>state.auth.incorrectEmail
        }),                   
        // showEmail(){
        //     return this.$store.state.auth.showEmailCheck;
        // }
    }
    }   
    
}
</script>
<style scoped>
.wrapper{
    background-color: blanchedalmond;
}
</style>
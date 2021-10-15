<template>  
    <div class="container-fluid">
       <div class="bg">
          <h2>Sorry. You have no permissions to do this.</h2>
        </div>  
    </div>  
</template>
<script>
export default {
  name: "noPerm",
  mounted() {
    setTimeout(this.goHome, 3500);
  },
  methods: {
    goHome() {
      this.$router.push("/")    
    },
  }
}
</script>
<style  scoped>
body, html {
  height: 100%;
  margin: 0;
}


.bg {
  /* The image used */
  background-image: url("../assets/photos/lift.jpg");

  /* Full height */
  height: 100vh; 

  /* Center and scale the image nicely */
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.bg > h2 {
  font-size: 100px;
  margin-bottom: 20px;
  color: #fff;
}
@media all and (max-width:700px){
  .bg h2{
    font-size:calc(2vh + 2vw + 1rem ) ;
  }
}

</style>
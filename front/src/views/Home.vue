<template>
  <div :class="ready?'loaded':''">
    <header>
      <h1>Ideas Rule The World</h1>
    </header>
    <main>
      <h2>Pet project based on django and vue.js</h2>    
    </main>
  </div>
</template>

<script>

import AppBanner from '@/components/Banner'
export default {
  name: 'AppHome',
  data(){
    return {
      ready:false
    }
  },
  components:{
    AppBanner
  },
  mounted(){
    this.ready = true
  } 
}
</script>
<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Merriweather&family=Montserrat:wght@300&display=swap");
:root {
  --base: 10;
  --len: 10; /* length of title */
}
*,
*::before,
*::after {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}
html {
  background-color: #333;
  color: #fff;
  font-size: 20px;
  font-family: "Monserrat", sans-serif;
  line-height: 1.5;
  font-weight: 400;
}
header {
  height: 100vh;
  font-family: "Merriweather", serif;
  display: flex;
  flex-direction: column;
  place-content: center;
}  
header::before {
  position: absolute;
  content: '';
  width:100vw;
  height: 100vh;
  z-index: -1;
  background-image: url(../assets/photos/bridge_final.jpg);
  background-position: center;
  background-size: cover;
  transform: scale(1.2);
  /* transform: scale(1.4); */
  transition: transform 0.5s ease-in 0.5s;
  /* transition: transform 0.5s ease-in 0.5s; */
}

.loaded header::before{
  transform: scale(1);
}

/* make middle 1/third almost transparent 
and middle 1/3 is devided into 2 parts with raion 38.2:62.8
*/
header h1{
  font-size: calc(2vh + 2vw + 2rem );
  color:rgb(38, 36, 36);
  background-color: hsla(0, 0%, 100%, 0.8);
  line-height: 1.5;
  padding-left: 2rem;
  height:33vh;
  display: flex;
  flex-direction: column;
  justify-content: center; 
  /* box-sizing:border-box */
  border-left:38.2vw solid hsla(0, 0%, 0%, 0.8);

}
main {
  padding: 2rem 2rem 2rem 2rem;
}
@media all and (min-width:700px){
  main{
    padding:2rem 2rem 2rem 0rem;
    margin-left: 38.2vw;
  }
}
@media all and (max-width:700px){
  header h1{
    font-size:calc(2vh + 2vw + 1rem ) ;
  }
}
</style>

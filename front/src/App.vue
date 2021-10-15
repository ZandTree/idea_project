<template>
  <div id="app">    
    <Menu></Menu>  
    <router-view/>    
  </div>
</template>

<script>
import Menu from '@/components/Menu'
export default {
  name:'App',
  components:{
    Menu
  }
}
</script>

<style>
html, body { 
  height: 100%;
  
}
.full-page{ 
  height: 100vh;
  width: 100vw;
  
}
.container-fluid{
    height:100vh;
    
  }

.container, .row.justify-content-center.align-items-center {
  height: 100%;
  min-height: 100%;
} 
/* user UI msg */
.warn {
  background-color: rgb(240, 194, 194);
  border-radius: 3px;
  padding:5px 10px;
}
/* success flash message */
.flesh-msg{  
    display: flex;
    justify-content: center;
    background-color: rgb(192, 219, 164);
   
    padding: 2rem;
    border-radius: 10px;


}
.flesh-msg-error{  
    background-color: rgb(240, 194, 194);;
    
    display: flex;
    justify-content: center;
    padding: 2rem;
    border-radius: 10px;
    margin-left: -0.5rem;


}
.is-danger {
  background-color: #c72534c9;
  padding-left:1rem;
  border-radius: 5px;
  color:white;
}
.is-success {
  background-color: cadetblue;
  padding-left:1rem;
  border-radius: 5px;
  color:white;
}
.not-welcome{
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: row;
}   
/* field form is required */
.control-label::after {
  content: " *";
  color: red;
}
/* for side bars */
.color{
    background-color: #ffebcd;
}
.fill-color{
   height: 100vh;
   margin: 0; 
   border-radius: 5px;
}

/* comment form  */
.comment-form-invisible{
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

/* comments to display */

.comment-body{
  border:1px solid black;
  border-radius: 3px; 
}


</style>

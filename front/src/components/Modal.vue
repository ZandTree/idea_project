<template>
  <div class="modal-bg">
    <div class="confirm-modal">
      <button type="button" class="btn-close" @click="close"></button>
      <header class="modal-header">
        <slot name="header">Default Title </slot>
      </header>
      <section class="modal-body">
        <slot name="body">Default body </slot>
      </section>
      <section class="modal-footer">
        <slot name="modal-footer">Default Footer </slot>
        <!-- <button type="button" class="btn-green" @click="close">Close</button> -->
      </section>
    </div>
  </div>
  <!--  outer div class modal-backdrop -->
</template>
<script>
export default {
  name: "AppModal",
  data() {
    return {};
  },
  methods: {
    close() {
      console.log("close X clicked");
      this.$emit("close");
    },
  },
};
</script>

<style scoped>
.modal-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 99;
  /* normal css flow  to hide element*/
  /* visibility: hidden;
  opacity: 0; */
}
.confirm-modal {
  background-color: rgb(245, 231, 218);
  width: 50%;
  /* otherwise pop-up with too long body */
  /* height: 50%; */
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-direction: column;
  position: relative;
}
.modal-header,
.modal-footer {
  padding: 15px;
  display: flex;
}
.modal-header {
  /* position: relative; */
  border-bottom: 1px solid #eeeeee;
  color: rgb(224, 55, 55);
  /* color: #4aae9b; */
  justify-content: space-between;
}
.modal-footer {
  border-top: 1px solid #eeeeee;
  display: flex;
  align-items: center;
  justify-content: space-around;
}
.modal-body {
  position: relative;
  padding: 20px 10px;
  z-index: 1;
}
.btn-close {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: lightcoral;
  /* border: none;
  font-size: 20px;
  padding: 10px;
  cursor: pointer;
  font-weight: bold;
  color: #4aae9b;
  background: transparent; */
}
.btn-green {
  color: white;
  background: #4aae9b;
  border: 1px solid #4aae9b;
  border-radius: 2px;
}
</style>
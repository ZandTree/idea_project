<template>
  <div class="tree-menu">
    <div :style="indent" @click="toggleChildren(slug)" class="label-wrapper">
     
       <router-link  :to="{name:'categ',params:{slug:slug}}" class="categ">
                <b-badge variant="secondary" class="categ px-2 mx-1">{{name}}</b-badge>          
       </router-link> 
    </div>
    <div v-if="showChildren">
      <tree-menu
        v-for="node in children"
        :key="node.id"
        :children="node.children"
        :name="node.name"
        :depth="depth + 1"
        :slug="node.slug"        
      >
      </tree-menu>
      <!-- depth for css styling -->
      
    </div>
  </div>
</template>
<script>


export default {
  props: ["name", "children", "depth", "slug"],
  name: "tree-menu",
  computed: {
    indent() {
      return { transform: `translate(${this.depth * 25}px)` };
    },
  },
  data() {
    return {
      showChildren: false,
       
    };
  },
  methods: {    
    async toggleChildren(catSlug) {
      this.showChildren = !this.showChildren;      
      
    },
      
  },
  // created(){
  //   console.log("Node tree comp is created")
  // }
};
</script>

<style scoped>
.tree-menu .label-wrapper {
  padding-bottom: 10px;
  margin-bottom: 10px;
  /* border-bottom: 1px solid #ccc; */
  cursor: pointer;
}
</style>>

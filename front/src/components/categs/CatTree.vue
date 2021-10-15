<template>
  <div>
    <div>
      <div v-for="node in treeData" :key="node.id">
 <!-- render categs children if present        -->
        <div v-if="node.children && node.children.length" class="left-shift">
          <!-- <div v-if="tree.children.length > 0" class="left-shift"> -->
            <!-- <div v-if="node.name">{{node.name}}</div>            -->
          <app-node-tree
            :name="node.name"
            :children="node.children"
            :depth="0"
            :slug="node.slug"            
          ></app-node-tree>
          <!-- :depth otherwise a string will be passed to a child component -->
        </div>
<!-- render root categs (parent null) -->
        <div v-else class="left-shift">
          <!-- <div @click="getCatIdeas(node.slug)">{{ node.name }}</div> -->
           <router-link :to="{name:'categ',params:{slug:node.slug}}" class="categ">
                <b-badge variant="secondary" class="categ px-2 mx-1">{{node.name}}</b-badge>          
            </router-link> 
        </div>
        
      </div>
    </div>
  </div>
</template>
<script>
import AppNodeTree from "@/components/categs/NodeTree.vue";

export default {
  components: { AppNodeTree },
  props: ["treeData"], 
  created(){
    // console.log("Cat Tree component is created")
  }
};
</script>

<style scoped>
.left-shift {
  text-align: left;
  padding: 0.2rem 0 0.5rem 0.5rem;
  margin-left: 0.5rem;
  cursor: pointer;
}
/* .zoo{
  transform: translate(25px);
  eq: translate(25px, 0) = only in horizontal direction
} */
</style>>
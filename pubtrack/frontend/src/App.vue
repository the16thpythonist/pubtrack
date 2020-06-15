<template>
  <div id="app">
    <NavBar class="nav"></NavBar>
    <div class="content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
  import NavBar from "@/components/NavBar";

  export default {
    name: "App",
    components: {
      NavBar
    }
  }
</script>

<style>
  body {
    margin: 0;
    padding: 0;
  }

  .content {
    padding: 10px;
    height: auto;
    margin: 30px 20% 0 20%;
  }
</style>

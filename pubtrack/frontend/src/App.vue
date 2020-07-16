<template>
  <div id="app">
    <NavBar class="nav"></NavBar>
    <div class="content">
      <router-view></router-view>
    </div>
    <Footer/>
  </div>
</template>

<script>
  import NavBar from "@/components/NavBar";
  import Footer from "./components/Footer";

  export default {
    name: "App",
    components: {
      Footer,
      NavBar
    }
  }
</script>

<style>
  html {
    font-family: Helvetica, Arial, sans-serif;
    height: 100%;
  }

  body {
    margin: 0;
    padding: 0;

    min-height: 100%;
    height: 100%
  }

  #app{
    height: 100%;
    min-height: 100%;

    display: flex;
    flex-direction: column;
  }

  .content {
    padding: 10px;
    margin: 30px 20% 0 20%;
    flex-grow: 2;
  }

  hr {
    color: #e1e4e8;
    background-color: #e1e4e8;
    height: 1px;
    border-style: none;
  }

  img[alt=full] {
    width: 100%;
  }
</style>

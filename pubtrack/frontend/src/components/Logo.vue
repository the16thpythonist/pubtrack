<template>
    <div class="container">
        <router-link :to="{name: 'home'}" class="logo">
            PubTrack
        </router-link>
    </div>
</template>

<script>
    export default {
        name: "Logo"
    }
</script>

<style scoped>
    .logo {
        text-decoration: none;
        color: white;
        font-family: Roboto, sans-serif;
            font-size: 1.7em;
            font-weight: bold;
    }

    .logo:hover {
        text-shadow: 3px 3px 7px rgba(255, 255, 255, 0.3);
    }

</style>
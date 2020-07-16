<template>
    <nav>
        <div class="container">
            <Logo/>

            <div class="nav-items">
                <router-link class="item" :to="{name: 'home'}">
                    Home
                </router-link>

                <router-link class="item" :to="{name: 'kitopen-coverage'}">
                    KITOpen Analytics
                </router-link>

                <router-link class="item" :to="{name: 'authors-list'}">
                    Authors
                </router-link>

                <router-link class="item" :to="{name: 'publications-list'}">
                    Publications
                </router-link>
            </div>

        </div>
    </nav>
</template>

<script>
    import Logo from "./Logo";

    export default {
        name: "NavBar",
        components: {
            Logo
        }
    }
</script>

<style scoped>
    nav {
        padding: 15px;

        background-color: #24292e;
        color: white;

        border-style: none;
    }

    .container {
        height: 40px;

        display: flex;
            flex-direction: row;
            align-items: center;

        font-size: 1em;
    }

    .logo {
        margin-left: 30px;

        font-family: Roboto, sans-serif;
            font-size: 1.7em;
            font-weight: bold;
    }

    .nav-items {
        margin-right: 10px;
        flex-grow: 2;

        display: flex;
            flex-direction: row;
            justify-content: flex-end;
            align-items: center;

        font-family: sans-serif;
            font-size: 1.1em;
    }

    .item, .item:visited {
        margin-right: 25px;

        font-weight: bold;
        text-decoration: none;
        color: white;

        border-style: solid;
            border-width: 0;
            border-bottom-width: 2px;
            border-color: #232323;
    }
    .item:hover {
        border-color: white;
    }
</style>
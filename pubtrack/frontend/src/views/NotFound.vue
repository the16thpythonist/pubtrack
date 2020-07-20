<template>
    <div class="container">
        <div class="not-found">
            <div class="code">404</div>
            <div class="title">Page Not Found</div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "NotFound"
    }
</script>

<style scoped>
    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .not-found {
        align-self: center;
        display: flex;
        flex-direction: column;
    }

    .code {
        font-size: 15em;
        font-weight: bold;
        width: 100%;
    }

    .title {
        align-self: center;
        font-size: 3em;
        font-weight: bold;
        margin-top: -40px;
    }

</style>
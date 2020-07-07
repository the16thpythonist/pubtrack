<template>
    <span class="container" @click="emitClick">
        <span class="inner">
        </span>
    </span>
</template>

<script>
    export default {
        name: "ClipboardIcon",
        methods: {
            emitClick() {
                this.$emit('click', true);
            }
        }
    }
</script>

<style scoped>

    .container:hover{
        opacity: 0.6;
    }

    .inner {
        position: relative;
        width: 10px;
        height: 10px;
    }

    .inner:after {
        content: "";
        position: absolute;

        height: 10px;
        width: 10px;
        background-color: white;

        transform: translate(2px, 5px);

        border-style: solid;
        border-color: black;
        border-radius: 1px;
        border-width: 1px;
    }
    .inner:before {
        background-color: white;
        content: "";
        position: absolute;

        height: 10px;
        width: 10px;

        transform: translate(-2px, 1px);

        border-style: solid;
        border-color: black;
        border-radius: 1px;
        border-width: 1px;
    }
</style>
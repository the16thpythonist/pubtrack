<template>
    <div class="container">
        <div
                class="true"
                v-show="value === true">
            YES
        </div>
        <div
                class="false"
                v-show="value !== true">
            NO
        </div>
    </div>
</template>

<script>
    /**
     * This component represents an indicator for a boolean variable.
     *
     * The whole point of this component is literally just to indicate the state of a boolean value. And that's it.
     * A boolean value can be bound to it and on the web page it will render into a display of yes or no according
     * to the variable.
     */
    export default {
        name: "BooleanIcon",
        props: {
            /**
             * The boolean state of the indicator.
             */
            value: {
                type:       Boolean,
                required:   true
            }
        },
        data: function () {
            return {}
        },
    }
</script>

<style scoped>
    .container>div {
        font-family: sans-serif;
            font-size: 0.9em;
            font-weight: bold;
    }

    .true {
        color: green;
    }

    .checkmark {
        height: 30px;
        width: 30px;
        border-radius: 15px;
        background-color: green;
    }

    .cross {
        height: 30px;
        width: 30px;
        border-radius: 15px;
        background-color: red;
    }

    .false {
        color: red;
    }
</style>
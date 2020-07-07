<template>
    <div class="container">
        <div
                class="true"
                v-show="value === true">
            <div class="tick-icon">
            </div>
        </div>
        <div
                class="false"
                v-show="value !== true">
            <div class="cross-icon">
            </div>
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

    .false {
        color: #ff4853;
    }


    .tick-icon {
        position: relative;

        width: 30px;
        height: 30px;

        border-radius: 15px;

        background-color: #5ad75a;
    }

    .tick-icon:before {
        content: "";
        position: absolute;

        background-color: white;

        height: 14px;
        width: 4px;

        transform: translate(15px, 9px) rotate(45deg);
    }

    .tick-icon:after {
        content: "";
        position: absolute;

        background-color: white;

        height: 8px;
        width: 4px;

        transform: translate(9px, 13px) rotate(-45deg);
    }

    .cross-icon {
        position: relative;

        width: 30px;
        height: 30px;

        border-radius: 15px;

        background-color: #ff4853;
    }

    .cross-icon:before {
        content: "";
        position: absolute;

        background-color: white;

        width: 4px;
        height: 17px;

        transform: translate(13px, 7px) rotate(45deg);
    }

    .cross-icon:after {
        content: "";
        position: absolute;

        background-color: white;

        width: 4px;
        height: 17px;

        transform: translate(13px, 7px) rotate(-45deg);
    }
</style>
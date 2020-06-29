<template>
    <div
            :class="classes"
            @click="onClick">
    </div>
</template>

<script>
    export default {
        name: "Checkbox",
        props: {
            value: {
                type:       Boolean,
                required:   true,
            }
        },
        data() {
            return {
                active: this.value
            }
        },
        methods: {
            onClick() {
                this.toggle();
                this.emit();
            },
            toggle() {
                this.active = !this.active;
            },
            emit() {
                this.$emit('input', this.active);
            }
        },
        computed: {
            classes() {
                return {
                    'checkbox':     true,
                    'active':       this.active
                }
            }
        },
        watch: {
            value(newVal) {
                this.active = newVal;
            }
        }
    }
</script>

<style scoped>
    .checkbox {
        height: 25px;
        width: 25px;

        background-color: rgba(0,0,0,0.30);
        /*border-style: solid;*/
        /*border-width: 2px;*/
        /*border-color: white;*/
        border-radius: 1px;
    }

    .checkbox:hover {
        background-color: rgba(0,0,0,0.20);;
    }

    .checkbox.active {
        background-color: #40af54;
    }

    .checkbox.active:hover {
        background-color: #42c357;
    }

    .checkbox.active:after {
        content: "";
        position: absolute;
        width: 4px;
        height: 8px;
        background-color: white;
        transform: translate(6px, 12px) rotate(-45deg);
    }

    .checkbox.active:before {
        content: "";
        position: absolute;
        width: 4px;
        height: 16px;
        background-color: white;
        transform: translate(12px, 5px) rotate(45deg);
    }
</style>
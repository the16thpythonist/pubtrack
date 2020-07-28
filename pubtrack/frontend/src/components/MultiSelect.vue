<template>
    <div class="container">
        <div class="title" v-if="title">
            {{ title }}
        </div>
        <div class="head row">
            <div class="column1">
                <em class="select-all" @click="selectAll">All</em>
            </div>
            <div class="column2">
                {{ header }}
            </div>
        </div>
        <div class="selection" v-for="(choice, value) of choices">
            <div class="choice row">
                <div class="column1">
                    <Checkbox
                        class="checkbox"
                        :value="!!selected[choice]"
                        @input="onInput(choice)"/>
                </div>
                <div class="name column2">
                    {{ choice }}
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Checkbox from "./Checkbox";
    export default {
        name: "MultiSelect",
        components: {Checkbox},
        props: {
            choices: {
                type:           Array,
                required:       true
            },
            value: {
                type:           Array,
                required:       true
            },
            title: {
                type:           String,
                required:       false,
                default:        ''
            },
            header: {
                type:           String,
                required:       false,
                default:        ''
            }
        },
        data() {
            return {
                selected: {},
                allSelected: false
            }
        },
        methods: {
            onInput(choice) {
                this.select(choice, !!!this.selected[choice]);
                this.emitInput();
            },
            select(choice, value) {
                if (value) {
                    this.$set(this.selected, choice, true);
                } else {
                    this.$delete(this.selected, choice);
                }
            },
            selectAll() {
                this.allSelected = !this.allSelected;
                console.log(this.allSelected);
                for (let choice of this.choices) {
                    this.select(choice, this.allSelected);
                }
                this.emitInput();
            },
            emitInput() {
                let result = Array.from(Object.keys(this.selected));
                this.$emit('input', result);
            }
        }
    }
</script>

<style scoped>
    .row {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: row;
        margin-bottom: 3px;
    }

    .checkbox {
        margin-right: 10px;
        transform: scale(0.8);
    }

    .column1 {
        min-width: 40px;
        max-width: 40px;
    }

    .column2 {
        min-width: 90%;
        max-width: 90%;
        padding-top: 5px;
    }

    .select-all {
        cursor: pointer;
        margin-left: 5px;
    }
</style>
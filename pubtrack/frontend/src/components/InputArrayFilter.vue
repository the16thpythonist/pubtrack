<template>
    <div class="container">
        <label
                v-show="title">
            {{ title }}
        </label>
        <div class="input">
            <input
                    type="text"
                    v-model="input"
                    @input="onInput"
                    :placeholder="filter['placeholder']">
        </div>
    </div>
</template>

<script>
    export default {
        name: "InputArrayFilter",
        props: {
            title: {
                type:       String,
                required:   false,
                default:    'Input Filter:'
            },
            base: {
                type:       Array,
                required:   true,
            },
            value: {
                type:       Array,
                required:   true
            },
            filter: {
                type:       Object,
                required:   false,
                default(){
                    return {
                        placeholder:        'Type something',
                        func(array, input) {
                            console.log(input);
                            return array;
                        }
                    }
                }
            }
        },
        data() {
            return {
                input: ''
            }
        },
        methods: {
            onInput() {
                let filtered = this.applyFilter();
                this.emit(filtered);
            },
            applyFilter() {
                return this._applyFilter(this.base);
            },
            _applyFilter(array) {
                return this.filter['func'](array, this.input);
            },
            emit(value) {
                this.$emit('input', value);
            }
        },
        watch: {
            base(newValue) {
                let filtered = this._applyFilter(newValue);
                this.emit(filtered);
            }
        }
    }
</script>

<style scoped>

</style>
<template>
    <div class="container">
        <h2>{{ title }}</h2>
        <textarea class="text" v-model="content">

        </textarea>
    </div>
</template>

<script>
    export default {
        name: "ArrayMapDisplay",
        props: {
            title: {
                type:       String,
                required:   false,
                default:    'My JSON data'
            },
            value: {
                required:   true
            },
            mapFunc: {
                type:       Function,
                required:   false,
                default:    function (element) {
                    return element;
                }
            }
        },
        data: function() {
            return {
                content:  ''
            }
        },
        methods: {
            getString: function (value) {
                let base = (typeof value === 'object' ? this.objectToArray(value) : value);
                let result = base.map(this.mapFunc);
                return JSON.stringify(result, null, 2);
            },
            objectToArray(obj) {
                let array = [];
                for(let key in obj) {
                    if (!Object.prototype.hasOwnProperty.call(obj, key)) continue;
                    let value = obj[key];

                    array.push(value);
                }
                return array;
            }
        },
        watch: {
            value: function (newValue) {
                this.content = this.getString(newValue);
            }
        }
    }
</script>

<style scoped>
    .text {
        width: 100%;
        height: 200px;
    }
</style>
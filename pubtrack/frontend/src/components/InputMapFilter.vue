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
    // TODO: Update this doc so it says, that this is about Map's
    // TODO: Add a checkbox to the front, so the filter can also be toggled.
    /**
     * A free text filter to be dynamically applied to an array
     *
     * First and foremost, the basic functionality of this component is the functionality of a filter for an array.
     * An array gets passed in and based on some defined rules some elements of this array will be removed for the
     * resulting array, which is returned.
     * The array on which to be operated gets passed in as the "base" prop and the resulting array will be updated
     * in the "value" prop.
     *
     * The component will render as a text input field. Whatever text will be entered into the input field will also
     * be passed to the filter function.
     * How the filter works specifically is not implemented within this component. This filter functionality can also
     * be passed dynamically to the component using the "filter" prop.
     * The filter defined there will be reapplied to the array every time the content of the input field changes
     *
     * EXAMPLE
     *
     * ```js
     * export default {
     *     name: "SomeComponent",
     *     data: {
     *         baseArray: ["Hello", "World"],
     *         resultArray: [],
     *         inputFilter: {
     *             name:        "Contains Text",
     *             placeholder: "Enter text to check for inclusion",
     *             func(array, input) {
     *                 return array.filter(function(element){
     *                     return element.includes(input);
     *                 });
     *             }
     *         }
     *     }
     * }
     * ```
     *
     * ```html
     * <InputArrayFilter
     *          :base="baseArray"
     *          v-model="resultArray"
     *          :filter="inputFilter"/>
     * ```
     */
    export default {
        name: "InputMapFilter",
        props: {

            title: {
                type:       String,
                required:   false,
                default:    'Input Filter:'
            },
            /**
             * The base array on which the filters will be applied
             */
            base: {
                type:       Map,
                required:   true,
            },
            /**
             * The array which results after the filter has been applied to the base
             */
            value: {
                type:       Map,
                required:   true
            },
            /**
             * And object defining the filter, which is applied to the array
             */
            filter: {
                type:       Object,
                required:   false,
                default(){
                    return {
                        placeholder:        'Type something',
                        func(map, input) {
                            console.log(input);
                            return map;
                        }
                    }
                }
            }
        },
        data() {
            return {
                // Contains the user input from the input field. Bound to the element via v-model
                input: ''
            }
        },
        methods: {
            /**
             * Callback for the input even on the text input field. Will reapply the filter on the base array and
             * emit the result as the parameter to an input event of this component
             */
            onInput() {
                let filtered = this.applyFilter();
                this.emit(filtered);
            },
            /**
             * Applies the filter to the base array and returns the result.
             *
             * @returns {*}
             */
            applyFilter() {
                return this._applyFilter(this.base);
            },
            /**
             * Applies the filter on the given array.
             *
             * Defining helper methods with as many parameters as possible helps the testability.
             *
             * @param map
             * @returns {*}
             * @private
             */
            _applyFilter(map) {
                return this.filter['func'](map, this.input);
            },
            /**
             * Emits an "input" event with the given value.
             *
             * @param value
             */
            emit(value) {
                this.$emit('input', value);
            }
        },
        watch: {
            /**
             * Whenever the "base" prop is changed the filter will be applied to this new array.
             * @param newValue
             */
            base(newValue) {
                let filtered = this._applyFilter(newValue);
                this.emit(filtered);
            }
        }
    }
</script>

<style scoped>

</style>
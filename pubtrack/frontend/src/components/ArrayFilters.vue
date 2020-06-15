<template>
    <div class="container">
        <span class="title">
            Filters:
        </span>
        <div
                class="element"
                v-for="(filter, key) in filters"
                :key="key">
            <input
                    type="checkbox"
                    :id="key"
                    @input="onInput($event, filter)">
            <label
                    :for="key">
                {{ filter['name'] }}
            </label>
        </div>
    </div>
</template>

<script>
    /**
     * A set of custom filters to be dynamically applied to an array.
     *
     * First and foremost, the basic functionality of this component is the functionality of a filter for an array.
     * An array gets passed in and based on some defined rules some elements of this array will be removed for the
     * resulting array, which is returned.
     * The array on which to be operated gets passed in as the "base" prop and the resulting array will be updated
     * in the "value" prop.
     *
     * But this component does not implement some specific filter. This filter can also be passed in as a prop. Even
     * multiple filters can be passed in using the "filters" prop. Each possible filter will have to be a object,
     * which is a property to the "filters" object. An example of how these have to be defined will be given later.
     *
     * Ultimately the decision to apply a filter on the array or not is with the user of the application. This
     * component will render as a set of checkboxes, one for every possible filter. As soon as a box is checked the
     * filters will be reapplied and the outcome will then be updated to the "value" prop.
     *
     * EXAMPLE
     *
     * ```js
     * export default {
     *      name: "SomeComponent",
     *      components: {ArrayFilters},
     *      data() {
     *          return {
     *              baseArray: [1, 2, 3, 4, 5, 7, 8],
     *              resultArray: [],
     *              customFilters: {
     *                  iseven: {
     *                     name:        "Is even?",
     *                     active:      false,
     *                     func(array) {
     *                         return array.filter(function(element) {
     *                             return element % 2 === 0
     *                         });
     *                     }
     *                  }
     *              }
     *          }
     *      }
     * }
     * ```
     *
     * ```html
     * <ArrayFilters
     *          :base="baseArray"
     *          v-model="resultArray"
     *          :filters="customFilters"/>
     * ```
     *
     */
    export default {
        name: "ArrayFilters",
        props: {
            /**
             * The base array on which all the filters will be applied
             */
            base: {
                type:       Array,
                required:   true
            },
            /**
             * The array, which results, after all the active filters have been applied
             */
            value: {
                type:       Array,
                required:   true
            },
            /**
             * An object defining all the filters, which are available for the user to be chosen
             */
            filters: {
                type:       Object,
                required:   true
            }
        },
        // data: function () {
        //     return {
        //
        //     }
        // },
        methods: {
            /**
             * The callback for an input event on the checkboxes.
             *
             * If the checkbox has been checked the corresponding filter becomes active, it it has been unchecked it
             * becomes inactive. In any given case all the filters will be recomputed using the "base" array and the
             * new resulting array will be emitted as an input event of this method.
             *
             * @param event
             * @param filter
             */
            onInput(event, filter) {
                // This is the callback exclusively for the checkboxes, which means that event.target will be a
                // checkbox element and event.target.checked will the boolean state of the checkbox which fired the e
                // event.
                filter['active'] = event.target.checked;
                let result = this.applyAllFilters(this.base);
                this.emit(result);
            },
            /**
             * Applies all active filters on the given base array and returns the resulting array.
             *
             * @param base
             * @returns {*}
             */
            applyAllFilters(base) {
                let result = base;
                for (let key in this.filters) {
                    if (!Object.prototype.hasOwnProperty.call(this.filters, key)) continue;
                    let filter = this.filters[key];

                    if (filter['active']) {
                        // It is important to note here that the "func" defined for a filter object does take the
                        // whole array as an argument and not just an element (like filter functions usually do).
                        result = filter['func'](result);
                    }
                }
                return result;
            },
            /**
             * Emits the given value as an input event
             *
             * @param value
             */
            emit: function (value) {
                this.$emit('input', value);
            }
        },
        watch: {
            /**
             * If the base array is modified all the filters are being reapplied to the new base array.
             *
             * @param newValue
             */
            base(newValue) {
                let result = this.applyAllFilters(newValue);
                this.emit(result);
            }
        }
    }
</script>

<style scoped>

</style>
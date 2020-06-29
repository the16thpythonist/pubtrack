<template>
    <div class="container">
        <span class="title">
            {{ title }}:
        </span>
        <div
                class="element"
                v-for="(filter, key) in filters"
                :key="key">
            <Checkbox
                    class="checkbox"
                    :id="key"
                    @input="onSelect($event, filter)"/>
            <label
                    :for="key">
                {{ filter['name'] }}
            </label>
        </div>
    </div>
</template>

<script>

    import Checkbox from "./Checkbox";

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
     *      components: {MapFilters},
     *      data() {
     *          return {
     *              baseMap: new Map([["ar", 1], ["es", 2], ["oe", 3], ["tk", 4]]),
     *              resultMap: new Map(),
     *              customFilters: {
     *                  // Example for filtering the values of the map
     *                  // This will filter all the elements, where the value is an even integer
     *                  iseven: {
     *                     name:        "Is value even?",
     *                     active:      false,
     *                     func(map) {
     *                          let result = new Map();
     *                          map.forEach(function(key, value)) {
     *                              if (value % 2 == 0) {result.set(key, value); }
     *                          }
     *                          return result;
     *                     }
     *                  },
     *                  // Example for filtering the key of the map
     *                  // This will filter for all the key strings, which have the letter "e" in them
     *                  contains_e: {
     *                      name:       "Does key contain 'e'?",
     *                      active:     false,
     *                      func(map) {
     *                          let result = new Map();
     *                          map.forEach(function(key, value)) {
     *                              if (key.included("e")) {result.set(key, value); }
     *                          }
     *                          return result;
     *                      }
     *                  }
     *              }
     *          }
     *      }
     * }
     * ```
     *
     * ```html
     * <MapFilters
     *          :base="baseMap"
     *          v-model="resultMap"
     *          :filters="customFilters"/>
     * ```
     *
     */
    export default {
        name: "MapFilters",
        components: {Checkbox},
        props: {
            /**
             * The base map on which all the filters will be applied
             */
            base: {
                type:       Map,
                required:   true
            },
            /**
             * The map, which results, after all the active filters have been applied
             */
            value: {
                type:       Map,
                required:   true
            },
            /**
             * An object defining all the filters, which are available for the user to be chosen
             */
            filters: {
                type:       Object,
                required:   true
            },
            title: {
                type:       String,
                required:   false,
                default:    'Filters'
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
             * becomes inactive. In any given case all the filters will be recomputed using the "base" map and the
             * new resulting map will be emitted as an input event of this method.
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
            onSelect(value, filter) {
                filter['active'] = value;
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
                for (let [key, value] of Object.entries(this.filters)) {
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
    .title {
        margin-bottom: 5px;

    }

    .checkbox {
        transform: scale(0.7);
        margin-right: 10px;
    }

    .element {
        display: flex;
        flex-direction: row;
        align-content: center;
        align-items: center;
    }
</style>
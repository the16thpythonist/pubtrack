<template>
    <div class="container" @click="emitClick($event)">
        <div
                :class="classes"
                :style="styles">
        </div>
    </div>
</template>

<script>
    /**
     * Displays an arrow, whose direction can be controlled and which also acts as a button.
     *
     * This is more of a design element than actual functionality.
     * One prominent use for this kind of clickable arrow is for drop down items. Usually the arrow points downwards to
     * indicate that it is possible to drop down some content. If it is clicked the hidden content will be revealed and
     * the arrow will point upwards to indicate that it is possible to click it to hide the content again.
     *
     * This component is more or less just a generalized implementation of that requirement.
     * Additional to the core functionality of controlling the arrow direction, the component offers some properties to
     * customize the style of the arrow.
     *
     * EXAMPLE
     *
     * ```js
     * export default {
     *     name: "SomeComponent",
     *     components: { PointingArrow },
     *     data() {
     *         return {
     *             direction: "right"
     *         }
     *     }
     * }
     * ```
     *
     * ```html
     * <PointingArrow
     *          :value="direction"
     *          size="6px"
     *          thickness="2px"
     *          radius="1px"
     *          color="red"/>
     * ```
     *
     */
    export default {
        name: "PointingArrow",
        props: {
            /**
             * The direction of the arrow.
             *
             * This property may only accept the following string identifiers:
             * "up", "down", "left", "right"
             * If anything else is used the component will turn to the default direction.
             */
            value:  {
                type:       String,
                required:   true
            },
            /**
             * The default direction of the arrow, which is set when the string for value is an invalid identifier
             */
            default: {
                type:       String,
                required:   false,
                default:    'down'
            },
            /**
             * The size of the arrow. (CSS size)
             *
             * The actual arrow is contained within a quadratic container. The CSS size value set for this will be used
             * as both the width and the height for this container.
             */
            size: {
                type:       String,
                required:   false,
                default:    "8px"
            },
            /**
             * The thickness of the arrow line. (CSS size)
             */
            thickness: {
                type:       String,
                required:   false,
                default:    "2px"
            },
            /**
             * The radius of the edges of the line, which forms the arrow (CSS size)
             */
            radius: {
                type:       String,
                required:   false,
                default:    "0px"
            },
            /**
             * The color of the arrow itself (CSS color)
             */
            color: {
                type:       String,
                required:   false,
                default:    "#181818"
            }
        },
        data() {
            return {
                // Check if the direction string is valid
                options: ["up", "down", "right", "left"],
            }
        },
        computed: {
            /**
             * Returns an object with the style rules for the arrow
             *
             * This is done with a computed property since the style rules depend on the props of the component and
             * those could be changed dynamically
             *
             * @returns {{borderColor: *, borderRadius: *, borderLeftWidth: *, width: *, borderBottomWidth: *, height: *}}
             */
            styles() {
                return this.createStyles(this.size, this.color, this.thickness, this.radius);
            },
            /**
             * Returns an object with the CSS classes of the arrow
             *
             * The base functionality of the arrow direction is implemented using different CSS classes, so these have
             * to dynamically be changed depending on the value prop of the component
             *
             * @returns {{arrow: boolean, left: boolean, up: boolean, right: boolean, down: boolean}}
             */
            classes() {
                let value = this.normalizeValue(this.value);
                return this.createClasses(value);
            }
        },
        methods: {
            /**
             * Emits a "click" event.
             *
             * This is the callback for whenever the container box of the arrow is clicked
             *
             * @param event
             */
            emitClick(event) {
                this.$emit('click', event);
            },
            /**
             * Given the direction string value, this will check if it is a valid option. If the value is a valid
             * option it is returned as it is and if not the default direction value is returned.
             *
             * @param value
             * @returns {string|*}
             */
            normalizeValue(value) {
                if (this.options.includes(value)) {
                    return value;
                } else {
                    let message = `Arrow value is not supported! "${value}"`;
                    console.log(message);
                    return this.default;
                }
            },
            /**
             * Creates the classes object from the direction string value.
             *
             * @param value
             * @returns {{arrow: boolean, left: boolean, up: boolean, right: boolean, down: boolean}}
             */
            createClasses(value) {
                value = this.normalizeValue(value);
                return {
                    arrow:                  true,
                    up:                     value === "up",
                    down:                   value === "down",
                    right:                  value === "right",
                    left:                   value === "left"
                }
            },
            /**
             * Creates the styles object from the given individual values.
             *
             * @param size
             * @param color
             * @param thickness
             * @param radius
             * @returns {{borderColor: *, borderRadius: *, borderLeftWidth: *, width: *, borderBottomWidth: *, height: *}}
             */
            createStyles(size, color, thickness, radius) {
                return {
                    width:                  size,
                    height:                 size,
                    borderColor:            color,
                    borderBottomWidth:      thickness,
                    borderLeftWidth:        thickness,
                    borderRadius:           radius
                }
            }
        }
    }
</script>

<style scoped>
    .container {
        padding: 5px;
    }

    .arrow {
        display: block;
        padding: 0px;
        background-color: inherit;
        border-style: solid;
        border-width: 0px;
    }

    .up {
        transform: rotate(-225deg);
    }

    .down {
        transform: rotate(-45deg);
    }

    .right {
        transform: rotate(-135deg);
    }

    .left {
        transform: rotate(45deg);
    }
</style>
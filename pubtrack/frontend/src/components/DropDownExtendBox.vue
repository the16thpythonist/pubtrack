<template>
    <div class="container">
        <div
                class="head"
                :style="headStyle">
            <PointingArrow
                    class="toggle"
                    :value="arrowDirection"
                    @click="toggle">
            </PointingArrow>
            <div class="title">
                <slot name="title"></slot>
            </div>
        </div>
        <div
                class="extend"
                v-show="active"
                :style="extendStyle">
            <slot name="content"></slot>
        </div>
    </div>
</template>

<script>

    // COMPONENTS
    import PointingArrow from "./PointingArrow";

    /**
     * A box, which consists of two containers. The one being always visible and the display of the other can be
     * toggled by the press of a button.
     *
     * This component is more of a design element than an actual functionality unit. The display function using the
     * button is the only functionality, which it offers.
     * It is an element which can be used for example, when the details of a list element would clutter the page, but
     * they should still be accessible. In such a case the button can be used to show just the details of the current
     * element of interest and afterwards it can be hidden again...
     *
     * The content of the two containers can be assigned using the two names slots "title" for the visible part and
     * "content" for the optional part.
     *
     * EXAMPLE
     *
     * ```js
     * export default {
     *      name: "SomeComponent",
     *      components: {DropDownExtendBox}
     * }
     * ```
     *
     * ```html
     * <DropDownExtendBox>
     *     <template v-slot:title>
     *          This is the title of the box
     *     </template>
     *
     *     <template v-slot:content>
     *         This content is hidden until the button is pressed!
     *     </template>
     * </DropDownExtendBox>
     * ```
     */
    export default {
        name: "DropDownExtendBox",
        components: {
            /**
             * EXPLANATION OF "PointingArrow"
             *
             * This is a component, which simply displays an arrow. The direction of this arrow can be controlled using
             * it's "value" prop. If it is clicked it will emit an input event.
             * In this component the arrow will be used as a button, which will toggle the visibility state of the
             * hidden container. The direction of the arrow will also serve as an indicator for the current state
             * of the container
             */
            PointingArrow
        },
        props: {
            /**
             * The padding of the entire box.
             */
            padding: {
                type:       String,
                required:   false,
                default:    "10px"
            }
        },
        data() {
            return {
                // Boolean indicator, which is true when the content is visible and false if it is hidden
                active: false,
                // This is a helper variable, which controls the state of the arrow element, which acts as the button,
                // which can be used to toggle the state of the second container.
                arrowDirection: "down"
            }
        },
        computed: {
            /**
             * Returns an object with the styling rules for the "title" slot container
             *
             * The styles of this container have to be passed in dynamically using a computed property, because 1) some
             * style rules are directly dependent on the numeric value of the "padding" prop and 2) some style rules
             * are also dependent on the visibility state of the box.
             */
            headStyle() {
                return {
                    paddingTop: this.padding,
                    paddingLeft: this.padding,
                    paddingRight: this.padding,
                    paddingBottom: !this.active ? this.padding : (this.padding / 2)
                }
            },
            /**
             * Returns the object with the styling rules for the "content" slot container
             *
             * The styles of this container have to be passed in dynamically using a computed property, because 1) some
             * style rules are directly dependent on the numeric value of the "padding" prop and 2) some style rules
             * are also dependent on the visibility state of the box.
             */
            extendStyle() {
                return {
                    paddingTop: !this.active ? this.padding : (this.padding / 2),
                    paddingBottom: this.padding,
                    paddingLeft: this.padding,
                    paddingRight: this.padding,
                }
            }
        },
        methods: {
            /**
             * Inverts the current state of the box. With the two possible states being hidden and visible
             */
            toggle() {
                if (this.active) {
                    this.active = false;
                    this.setArrowDown();
                } else {
                    this.active = true;
                    this.setArrowUp();
                }
            },
            /**
             * Sets the direction of the arrow button downwards
             */
            setArrowDown() {
                this.arrowDirection = "down";
            },
            /**
             * Sets the direction of the arrow button upwards
             */
            setArrowUp() {
                this.arrowDirection = "up";
            }
        }
    }
</script>

<style scoped>
    .container {
        display: flex;
        flex-direction: column;
    }

    .toggle {
        margin-right: 5px;
    }

    .head {
        display: flex;
            flex-direction: row;
    }

    .title {
        width: 100%;
    }

    .extend {
        background-color: rgba(255,255,255,0.30);
    }

    .title>*, .extend>*{
        width: 100%;
    }
</style>
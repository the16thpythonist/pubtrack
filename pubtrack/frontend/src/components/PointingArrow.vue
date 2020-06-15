<template>
    <div class="container" @click="emitClick($event)">
        <div
                :class="classes"
                :style="styles">
        </div>
    </div>
</template>

<script>
    export default {
        name: "PointingArrow",
        props: {
            value:  {
                type:       String,
                required:   true
            },
            size: {
                type:       String,
                required:   false,
                default:    "8px"
            },
            thickness: {
                type:       String,
                required:   false,
                default:    "2px"
            },
            radius: {
                type:       String,
                required:   false,
                default:    "0px"
            },
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
                default: "down",
                classes: {},
                styles: {}
            }
        },
        methods: {
            emitClick(event) {
                this.$emit('click', event);
            },
            normalizeValue(value) {
                if (this.options.includes(value)) {
                    return value;
                } else {
                    let message = `Arrow value is not supported! "${value}"`;
                    console.log(message);
                    return this.default;
                }
            },
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
            updateClasses() {
                this.classes = this.createClasses(this.value);
            },
            createStyles(size, color, thickness, radius) {
                return {
                    width:                  size,
                    height:                 size,
                    borderColor:            color,
                    borderBottomWidth:      thickness,
                    borderLeftWidth:        thickness,
                    borderRadius:           radius
                }
            },
            updateStyles() {
                this.styles = this.createStyles(
                    this.size,
                    this.color,
                    this.thickness,
                    this.radius
                )
            }
        },
        watch: {
            value() {
                this.updateClasses();
            },
            color() {
                this.updateStyles();
            },
            size() {
                this.updateClasses();
            }
        },
        created() {
            this.updateClasses();
            this.updateStyles();
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
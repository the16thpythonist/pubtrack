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

    export default {
        name: "DropDownExtendBox",
        components: {
            PointingArrow
        },
        props: {
            padding: {
                type:       String,
                required:   false,
                default:    "10px"
            }
        },
        data() {
            return {
                active: false,
                arrowDirection: "down"
            }
        },
        computed: {
            headStyle() {
                return {
                    paddingTop: this.padding,
                    paddingLeft: this.padding,
                    paddingRight: this.padding,
                    paddingBottom: !this.active ? this.padding : "4px"
                }
            },
            extendStyle() {
                return {
                    paddingBottom: this.padding,
                    paddingLeft: this.padding,
                    paddingRight: this.padding,
                }
            }
        },
        methods: {
            toggle() {
                if (this.active) {
                    this.active = false;
                    this.setArrowDown();
                } else {
                    this.active = true;
                    this.setArrowUp();
                }
            },
            setArrowDown() {
                this.arrowDirection = "down";
            },
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
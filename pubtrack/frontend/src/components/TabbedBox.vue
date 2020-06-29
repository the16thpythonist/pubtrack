<template>
    <div class="Container">
        <div class="header-container">
            <div
                    :class="headerClasses(key)"
                    v-for="(header, key) in headers"
                    :key="key"
                    @click="changeTab(key)">
                {{ header }}
            </div>
        </div>

        <div
                class="content-container">
            <div
                    class="content"
                    v-for="(header, key) in headers"
                    :key="header"
                    :style="contentStyle"
                    v-show="key === activeTab">
                <slot :name="key">
                    {{ header }} has not content...
                </slot>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "TabbedBox",
        props: {
            headers: {
                type:       Object,
                required:   true
            },
            default: {
                type:       String,
                required:   true
            },
            height: {
                type:       String,
                required:   false,
                default:    '200px'
            }
        },
        data() {
            return {
                activeTab:  this.default
            }
        },
        methods: {
            headerClasses(key) {
                return {
                    'header':       true,
                    'active':       key === this.activeTab
                }
            },
            changeTab(key) {
                this.activeTab = key;
            }
        },
        computed: {
            contentStyle() {
                return {
                    'height':       this.height
                }
            }
        }
    }
</script>

<style scoped>
    .header-container {
        display: flex;
            flex-direction: row;

        border-width: 0;
            border-color: #9B9B9B;
            border-style: solid;
            border-bottom-width: 1px;
    }

    .header {
        color: #9B9B9B;
        padding: 10px;
        margin-right: 20px;
    }

    .header:hover {
        cursor: pointer;
    }

    .header.active {
        color: black;

        border-style: solid;
            border-color: #9B9B9B;
            border-width: 1px;
            border-bottom-width: 0;
    }

    .content {
        margin: 0;
        overflow-y: auto;
        overflow-x: hidden;
    }
</style>
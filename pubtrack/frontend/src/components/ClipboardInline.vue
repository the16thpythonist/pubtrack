<template>
    <span class="container">
        <span ref="content" :class="contentClasses"><slot></slot></span>
        <ClipboardIcon @click="copyToClipboard"/>
    </span>
</template>

<script>
    import { copyClipboard } from "../common/clipboard.js";
    import ClipboardIcon from "./ClipboardIcon";

    export default {
        name: "ClipboardInline",
        components: {ClipboardIcon},
        props: {
            strikeThrough: {
                type:       Boolean,
                required:   false,
                default:    true
            }
        },
        data() {
            return {
                copied:     false
            }
        },
        methods: {
            emitCopy() {
                this.$emit('copy', this.value);
            },
            copyToClipboard() {
                copyClipboard(this.$refs.content);
                this.copied = true;
                this.emitCopy();
            }
        },
        computed: {
            contentClasses() {
                return {
                    'copy-content':     true,
                    'copied':           this.copied && this.strikeThrough
                }
            }
        }
    }
</script>

<style scoped>

    .container {
        display: flex;
        flex-direction: row;

        display: inline-flex;
    }

    .copy-content {
        display: inline-block;
        margin-right: 15px;
        font-family: monospace, sans-serif
    }

    .copied {
        color: gray;
        text-decoration: line-through;
    }

</style>
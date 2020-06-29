<template>
    <div class="container">
        <div class="input-container">
            <div class="input" v-for="(data, key) in inputs">
                <label>
                    {{ data['label'] }}:
                </label>
                <input
                        type="text"
                        v-model="parameters[key]"
                        :placeholder="data['placeholder'] ? data['placeholder'] : 'Enter Text...'"
                        @input="onInput">
            </div>
        </div>

        <label class="label">Generated Content:</label>
        <textarea v-model="content">
        </textarea>

        <button
                class="generate"
                type="button"
                @click.prevent="generateContent()"
                v-show="!reactive">
            Generate!
        </button>
    </div>
</template>

<script>
    export default {
        name: "InputTextGenerator",
        props: {
            value: {
                type:       Object,
                required:   true
            },
            generate: {
                type:       Function,
                required:   true
            },
            inputs: {
                type:       Object,
                required:   true
            },
            reactive: {
                type:       Boolean,
                required:   false,
                default:    false,
            }
        },
        data() {
            return {
                parameters: {},
                content: ''
            }
        },
        methods: {
            onInput() {
                if (this.reactive) {
                    this.generateContent();
                }
            },
            generateContent() {
                this.content = this.generate(this.parameters, this.value);
            }
        },
        created() {
            this.generateContent();
        }
    }
</script>

<style scoped>
    .container {
        display: flex;
            flex-direction: column;
    }

    .input {
        display: flex;
            flex-direction: row;
            align-items: center;

        margin-bottom: 10px;
    }

    /* THE INPUT FIELDS */
    input {
        flex-grow: 2;

        background-color: inherit;

        font-size: 0.95em;

        border-style: none;
            border-color: #b9b9b9;
            border-bottom-style: solid;
            border-bottom-width: 1px;

        padding-bottom: 3px;
        margin-left: 10px;
    }

    input:focus {
        border-color: black;
    }

    .label {
        margin-top: 10px;

        font-size: 0.9em;
    }

    /* THE GENERATE BUTTON */

    button {
        align-self: center;

        font-size: 1.1em;
            color: #00D52F;

        margin-top: 15px;

        height: 35px;
        width: 110px;
        background-color: inherit;

        border-style: solid;
            border-radius: 2px;
            border-width: 2px;
            border-color: #00D52F;
    }

    button:hover {
        cursor: pointer;

        background-color: #00D52F;
        color: white;
    }

    textarea {
        padding: 5px;
        min-height: 150px;
        min-width: 98%;
        max-width: 98%;
    }
</style>
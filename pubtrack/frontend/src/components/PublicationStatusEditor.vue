<template>
    <div class="container">
        <div class="row header">
            <div class="status-type">
                Status: <em>{{ status['name'] }}</em>
            </div>
            <span class="spacer"></span>
            <div class="changed">
                Changed: 12-12-2017
            </div>
        </div>
        <div class="row">
            <label>Description: </label>
            <input
                    type="text"
                    placeholder="Enter Description..."
                    v-model="status['description']"
                    @input="onInput">
        </div>
        <div class="row">
            <label>Solution: </label>
            <input
                    type="text"
                    placeholder="Enter Solution..."
                    v-model="status['solution']"
                    @input="onInput">
        </div>
        <div class="row actions">
            <span class="spacer"></span>
            <button
                    v-for="(action, key) in actions"
                    :key="key"
                    :class="action['classes']"
                    @click.prevent="action['callback']">
                {{ action['symbol'] }}
            </button>
        </div>
    </div>
</template>

<script>

    import api from "../common/api.service.js";

    export default {
        name: "PublicationStatusEditor",
        props: {
            value:    {
                type:       Object,
                required:   true
            }
        },
        data() {
            return {
                api: new api.Api()
            }
        },
        computed: {
            status() {
                return this.value['status'];
            },
            actions() {
                return {
                    warn: {
                        symbol:             'x',
                        classes: {
                            'warn-button':  true,
                            'active':       this.status['type'] === 'warn'
                        },
                        callback:           this.setPublicationWarned
                    },
                    pend: {
                        symbol:             '?',
                        classes: {
                            'pend-button':  true,
                            'active':       this.status['type'] === 'pend'
                        },
                        callback:           this.setPublicationPending
                    },
                    perm: {
                        symbol:             '-',
                        classes: {
                            'perm-button':  true,
                            'active':       this.status['type'] === 'perm'
                        },
                        callback:           this.setPublicationPermitted
                    },
                    solv: {
                        symbol:             'o',
                        classes: {
                            'solv-button':  true,
                            'active':       this.status['type'] === 'solv'
                        },
                        callback:           this.setPublicationSolved
                    }
                }
            }
        },
        methods: {
            onInput() {
                this.emit(this.value);
            },
            emit(publication) {
                this.$emit('input', publication);
            },
            setPublicationWarned() {
                this.setPublicationStatus('warn');
            },
            setPublicationPermitted() {
                this.setPublicationStatus('perm');
            },
            setPublicationPending() {
                this.setPublicationStatus('pend');
            },
            setPublicationSolved() {
                this.setPublicationStatus('solv');
            },
            setPublicationStatus(type) {
                let patch = {
                    description:        this.status['description'],
                    solution:           this.status['solution'],
                    type:               type
                };
                let self = this;
                this.api.patchPublicationStatus(this.value['uuid'], patch)
                    .then(function (status) {
                        self.value['status'] = status;
                    })
                    .catch(function (error) {
                        console.log(error)
                    })

            }
        }
    }
</script>

<style scoped>
    .container {
        display: flex;
            flex-direction: column;
    }

    .row {
        display: flex;
            flex-direction: row;
            align-content: center;
            align-items: center;

        margin-bottom: 5px;
    }

    .changed {
        color: #5f5f5f;
        font-size: 0.8em;
    }

    .spacer {
        flex-grow: 2;
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

    /* THE SELECTION BUTTONS */

    button {
        height: 23px;
        width: 28px;

        padding: 0;
        background-color: rgba(159,159,159, 1);

        text-align: center;
            color: white;
            font-weight: bold;
            font-size: 0.9em;
            line-height: 15px;
            box-sizing: border-box;

        border-style: solid;
            border-radius: 1px;
            border-width: 0;
            border-color: white;

        margin-left: 15px;
    }

    .actions {
        height: 36px;
    }

    button:hover {
        height: 28px;
        width: 33px;
        margin-left: 10px;
        /*box-shadow: 0px -1px 7px 3px rgba(0,0,0,0.71);*/
    }

    .active{
        height: 28px;
        width: 31px;
        margin-left: 15px;
    }
    .active:hover {
        height: 30px;
        width: 35px;
        margin-left: 11px;
    }

    .warn-button {
        background-color: #D8000C;
    }

    .perm-button {
        background-color: #004beb;
    }

    .solv-button {
        background-color: #00d52f;
    }

    .pend-button {
        background-color: #f5b700;
    }

</style>
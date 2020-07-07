<template>
    <div class="publication-select">
        <div class="headers">
            <span class="column0 header-offset"></span>
            <div class="column1">Publication Info</div>
            <div class="column2">Watched Authors</div>
            <div class="column3">KIT Open?</div>
            <div class="column4">POF Struct.</div>
            <div class="column5">
                <em
                        class="select-all"
                        @click.prevent="selectAll">
                    {{ allSelected ? 'Unselect' : 'Select' }}
                </em>
            </div>
        </div>
        <div class="selection">
            <div
                    class="publication"
                    v-for="(publication, uuid) of publications"
                    :key="uuid"
                    :class="rowClasses(uuid)">
                <div class="base-information">
                    <div class="column1">
                        <router-link
                                class="publication-name"
                                :to="{name: 'publication-detail', params: {'uuid': publication['uuid']}}">
                            <em>{{ getPublicationFirstAuthor(publication) }} et al. </em> {{ publication['title'] }}
                        </router-link>
                    </div>
                    <div class="column2 publication-authors">
                        <router-link
                                class="publication-author"
                                v-for="metaAuthor in publication['meta_authors']"
                                :key="metaAuthor['slug']"
                                :to="{name: 'author-detail', params: {slug: metaAuthor['slug']}}">
                            {{ metaAuthor['full_name'] }}
                        </router-link>
                    </div>
                    <BooleanIcon
                            class="column3"
                            :value="publication['on_kitopen']">
                    </BooleanIcon>
                    <div class="column4 publication-pof">
                        {{  publication['pof_structure'] ? publication['pof_structure'] : "-" }}
                    </div>
                    <div class="column5 publication-select-wrapper">
                        <Checkbox
                                class="select"
                                :value="!!selected[uuid]"
                                @input="onSelect($event, uuid)"/>
                    </div>
                </div>
                <DropDownExtendBox
                        class="dropdown">
                    <template v-slot:title>
                        <div class="status">
                            Status: <em>{{ publication['status']['name'] }}</em>
                        </div>
                    </template>
                    <template v-slot:content>
                        <div class="additional-information">
                            <h4>Additional information</h4>
                            <span class="scopus-id">
                                Scopus ID:
                                <a :href="publication['scopus_url']">
                                    {{ publication['scopus_id'] }}
                                </a>
                            </span>
                            <span class="kitopen-id">
                                KITOpen ID:
                                <a :href="publication['kitopen_url']">
                                    {{ publication['kitopen_id'] }}
                                </a>
                            </span>
                            <span class="doi">
                                DOI:
                                <a :href="publication['doi_url']">
                                    {{ publication['doi'] }}
                                </a>
                            </span>
                            <h4>Publication Status:</h4>
                            <PublicationStatusEditor v-model="publications[uuid]">
                            </PublicationStatusEditor>
                        </div>
                    </template>
                </DropDownExtendBox>
            </div>
        </div>
    </div>
</template>

<script>

    import api from "../common/api.service.js";
    // COMPONENTS
    import BooleanIcon from "./BooleanIcon";
    import DropDownExtendBox from "./DropDownExtendBox";
    import PublicationStatusEditor from "./PublicationStatusEditor";
    import Checkbox from "./Checkbox";

    export default {
        name: "PublicationSelect",
        components: {
            PublicationStatusEditor,
            BooleanIcon,
            DropDownExtendBox,
            Checkbox
        },
        props: {
            value: {
                type:       Object,
                required:   true
            },
            publicationsMap: {
                type:       Map,
                required:   true
            }
        },
        data: function () {
            return {
                publications: {},
                selected: {},
                api: new api.Api(),
                allSelected: false
            }
        },
        methods: {
            selectAll() {
                for (let [uuid, publication] of Object.entries(this.publications)) {
                    this.selectPublication(!this.allSelected, uuid, publication);
                }
                this.allSelected = !this.allSelected;
                this.emitInput();
            },
            getPublicationFirstAuthor(publication) {
                return publication['authors'][0] ? publication['authors'][0]['last_name'] : 'None';
            },
            onInput(event, publication) {
                this.emitInput();
            },
            onSelect(value, uuid) {
                this.selectPublication(value, uuid, this.publications[uuid]);
                this.emitInput();
            },
            selectPublication(select, uuid, publication) {
                if (select) {
                    this.$set(this.selected, uuid, this.publications[uuid]);
                } else {
                    this.$delete(this.selected, uuid);
                }
            },
            emitInput() {
                this.$emit('input', this.selected);
            },
            rowClasses(uuid) {
                let publication = this.publications[uuid];
                let status = publication['status']['type'];
                return {
                    publication:        true,
                    warning:            status === 'warn',
                    resolved:           status === 'solv',
                    permitted:          status === 'perm',
                    pending:            status === 'pend'
                }
            }
        },
        watch: {
            publicationsMap(newVal) {
                this.publications = Object.fromEntries(newVal);
                this.selected = {}
            }
        }
    }
</script>

<style scoped>

    .publication {

    }

    .base-information {
        display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: space-between;
        padding: 10px;
    }

    .headers {
        display: flex;
            flex-direction: row;
        padding: 10px;

        margin-bottom: 10px;
        background-color: #e6e6e6;
    }

    /* STYLE OF THE ROWS */

    h4 {
        margin-top: 10px;
        margin-bottom: 5px;
    }

    .publication {
        margin-bottom: 10px;

        border-style: solid;
            border-width: 1px;
            border-radius: 2px;
            border-color: #9b9b9b;
    }

    .publication-name {
        font-size: 1.1em;
        text-decoration: none;
        color: black;
    }

    .warning {
        background-color: #FFD6D8;
        border-color: #FF5C64;
    }

    .resolved {
        background-color: #D6FFDF;
        border-color: #5CFF7F;
    }

    .permitted {
        background-color: #D6E2FF;
        border-color: #85A9FF;;
    }

    .pending {
        background-color: #FFFAEB;
        border-color: #FFE085;
    }

    /* LAYOUT OF THE TABLE */

    .column0 {
        min-width: 0.1%;
    }

    .column1 {
        flex-grow: 2;
        width: auto;
        margin-right: 15px;
    }

    .column2 {
        min-width: 20%;
        max-width: 20%;
    }

    .column3 {
        min-width: 10%;
        max-width: 10%;
    }

    .column4 {
        min-width: 15%;
        max-width: 15%;
    }

    .column5 {
        min-width: 7%;
        max-width: 7%;
    }

    .publication-authors>*{
        margin-right: 5px;
    }

    .additional-information {
        display: flex;
            flex-direction: column;


        font-size: 0.85em;
        color: #373737;
    }

    .additional-information>span {
        margin-bottom: 5px;
    }

    /* BUTTONS */

    .warning-button, .pending-button, .permitted-button, .solved-button {
        border-style: solid;
            border-width: 1px;
            border-radius: 0px;
        margin-left: 10px;
        width: 30px;
        height: 20px;
        background-color: #42b983;
    }

    /* SELECTING THE PUBLICATIONS */

    .select-all {
        cursor: pointer;
    }

    .publication-select-wrapper{
        height: auto;
        align-self: center;
    }

    .select {
        margin-left: 13px;
    }

    .publication-author {
        display: inline-flex;
        position: relative;

        height: 22px;
        padding-right: 5px;
        padding-left: 5px;

        text-align: center;
        text-decoration: none;
        vertical-align: middle;
        line-height: 22px;
        font-size: 0.9em;
        font-family: sans-serif;

        color: #373737;
        background-color: rgba(0,0,0,0.25);

        border-radius: 0px 2px 2px 0px;
    }

    .publication-author:before {
        content: "";
        position: absolute;

        width: 0;
        height: 0;
        border-top: 11px solid transparent;
        border-right: 8px solid rgba(0,0,0,0.25);
        border-bottom: 11px solid transparent;

        transform: translate(-13px, 0px);
    }

</style>
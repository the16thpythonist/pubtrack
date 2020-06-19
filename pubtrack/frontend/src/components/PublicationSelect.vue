<template>
    <div class="publication-select">
        <div class="headers">
            <span class="column0 header-offset"></span>
            <div class="column1">Publication Info</div>
            <div class="column2">Watched Authors</div>
            <div class="column3">KITOpen?</div>
            <div class="column4">POF Structure</div>
            <div class="column5">Select</div>
        </div>
        <div class="selection">
            <div
                    class="publication"
                    v-for="(publication, i) in publications"
                    :key="i"
                    :class="rowClasses(i)">
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
                        <input
                            type="checkbox"
                            class="select"
                            :label="publication['slug']"
                            @input="onInput($event, publication)">
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
                            <PublicationStatusEditor v-model="publications[i]">
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

    export default {
        name: "PublicationSelect",
        components: {
            PublicationStatusEditor,
            BooleanIcon,
            DropDownExtendBox
        },
        props: {
            value: {
                type:       Object,
                required:   true
            },
            publications: {
                type:       Array,
                required:   true
            }
        },
        data: function () {
            return {
                selected: {},
                api: new api.Api()
            }
        },
        methods: {
            getPublicationName(publication) {
                let title = publication['title'];
                let author = publication['authors'][0] ? publication['authors'][0]['last_name'] : 'None';
                return `${author} et al. ${title}`;
            },
            getPublicationFirstAuthor(publication) {
                return publication['authors'][0] ? publication['authors'][0]['last_name'] : 'None';
            },
            onInput(event, publication) {
                let checked = event.target.checked;
                console.log(checked);
                if (checked) {
                    this.$set(this.selected, publication['uuid'], publication);
                } else {
                    this.$delete(this.selected, publication['uuid']);
                }
                this.emitInput();
            },
            emitInput() {
                this.$emit('input', this.selected);
            },
            rowClasses(index) {
                let publication = this.publications[index];
                let status = publication['status']['type'];
                return {
                    publication:        true,
                    warning:            status === 'warn',
                    resolved:           status === 'solv',
                    permitted:          status === 'perm'
                }
            },
            setPermitted(index) {
                console.log(index);
                let publication = this.publications[index];
                let uuid = publication['uuid'];
                let solution = publication['status']['_input'];
                // In case of success updating the info, else logging
                this.api.setPublicationStatusPermitted(uuid, solution)
                    .then(function (data) {
                        console.log(data);
                        publication['status']['solution'] = solution;
                        publication['status']['type'] = 'perm';
                    })
                    .catch(function (error) {
                        console.log("Could not set publication status to premitted");
                        console.log(error);
                    });
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

    .select {
        width: 40px;
        margin: 0;
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

    /* LAYOUT OF THE TABLE */

    .column0 {
        min-width: 0.1%;
    }

    .column1 {
        flex-grow: 2;
        width: auto;
    }

    .column2 {
        min-width: 20%;
    }

    .column3 {
        min-width: 10%;
    }

    .column4 {
        min-width: 15%;
    }

    .column5 {
        min-width: 5%;
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

</style>
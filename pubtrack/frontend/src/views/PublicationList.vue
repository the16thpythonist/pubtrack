<template>
    <div class="container">
        <h1>Known Publications</h1>
        <InputArrayFilter
                title=""
                :base="publications"
                :filter="titlesearch"
                v-model="filteredPublications"/>
        <div class="separator"></div>
        <div class="item" v-for="publication in filteredPublications" :key="publication['uuid']">
            <router-link
                        class="link"
                        :to="{name: 'publication-detail', params: {'uuid': publication['uuid']}}">
                <div class="inner">
                    <div class="column1">
                        <div class="title">
                            <em>{{ getFirstAuthor(publication) }}</em>{{ publication['title'] }}
                        </div>
                        <div class="secondary-info uuid">
                            uuid: {{ publication['uuid'] }}
                        </div>
                    </div>
                    <div class="column2">
                        {{ getMetaAuthors(publication) }}
                    </div>
                    <div class="column3">
                        <div
                                class="kitopen-badge"
                                v-if="publication['on_kitopen']">
                            KITOpen
                        </div>
                    </div>
                </div>
            </router-link>
        </div>
    </div>
</template>

<script>
    import api from "../common/api.service.js";

    import InputArrayFilter from "../components/InputArrayFilter";

    export default {
        name: "PublicationList",
        components: {InputArrayFilter},
        data() {
            return {
                api: new api.Api(),
                publications: [],
                filteredPublications: [],
                titlesearch: {
                    placeholder:        'Search title...',
                    func(publications, input) {
                        let result = [];
                        for (let publication of publications) {
                            let case_sensitive = publication['title'].includes(input);
                            let case_insensitive = publication['title'].toLowerCase().includes(input);
                            if (case_insensitive || case_sensitive) {
                                result.push(publication);
                            }
                        }
                        return result;
                    }
                }
            }
        },
        methods: {
            getPublications() {
                let self = this;
                this.api.getPublicationList()
                    .then(function (publications) {
                        self.publications = publications;
                    })
            },
            getFirstAuthor(publication) {
                let author = publication['authors'][0];
                return `${author['last_name']} et al. `;
            },
            getMetaAuthors(publication) {
                return publication['meta_authors'].map(function (meta_author) {
                    return meta_author['full_name'];
                }).join(', ')
            }
        },
        created() {
            this.getPublications()
        }
    }
</script>

<style scoped>
    .separator {
        height: 1px;
        width: 100%;

        margin-top: 10px;
        margin-bottom: 20px;

        background-color: rgba(0,0,0,0.30);
    }

    .item {
        background-color: #ebebeb;

        padding: 10px;
        margin-bottom: 10px;

        border-style: solid;
            border-width: 1px;
            border-radius: 1px;
            border-color: #B9B9B9;
    }

    .link {
        text-decoration: none;
        cursor: pointer;
        color: black;
    }

    .inner {
        display: flex;
        flex-direction: row;
    }

    .title {
        text-decoration: none;
        color: black;
        font-size: 1.1em;
    }

    .secondary-info {
        margin-top: 3px;
        color: #737373;
        font-size: 0.9em;
    }

    .column1 {
        flex-grow: 2;
        margin-right: 20px;
    }

    .column2 {
        min-width: 25%;
        margin-right: 10px;
    }

    .column3 {
        min-width: 10%;
    }

    .kitopen-badge {
        float: right;

        padding: 2px;
            padding-left: 6px;
            padding-right: 6px;
        margin-left: auto;

        display: inline-block;
        color: white;

        font-family: sans-serif, Arial, Verdana, "Trebuchet MS";
            font-size: 0.7em;
            font-weight: bold;

        background-color: #33af96;

        border-style: solid;
        border-width: 1px;
        border-radius: 2px;
        border-color: #329179;
    }

</style>
<template>
    <div class="container">
        <h1>KITOpen Metrics</h1>
        <p>
            This page can be used to display metrics of the <em>Publication Count</em> for the publications currently
            known to the pubtrack application. <br>
            To display the metrics, at least one item of both the displayed years and authors has to be selected within
            the option boxes below. Each of the options displayed are represented in at least one publication, which
            is currently in the database (which does mean, that every combination of year and author necessarily has
            to be represented).
        </p>
        <div class="selection">
            <MultiSelect
                    class="select year"
                    header="Year of Publication"
                    :choices="years"
                    v-model="selectedYears"
                    @input="onInput"/>
            <MultiSelect
                    class="select author"
                    header="Author"
                    :choices="authors"
                    v-model="selectedAuthors"
                    @input="onInput"/>
        </div>

        <h2>Metrics</h2>
        <div class="author-metrics">
            <div class="total">
                Total: <ClipboardInline :strike-through="false">{{ total }}</ClipboardInline>
            </div>
            <h4>Publications by Year:</h4>
            <div class="metric" v-for="(amount, year) in metricsYear">
                {{ year }}: {{ amount }}
            </div>
            <h4>Publications by Author:</h4>
            <div class="metric" v-for="(amount, author) in metricsAuthor">
                {{ author }}: {{ amount }}
            </div>
        </div>

        <h2>Publication Details</h2>
        <div class="results">
            <div class="header row">
                <div class="column1">
                    Title
                </div>
                <div class="column2">
                    Observed Authors
                </div>
                <div class="column3">
                    Year
                </div>
            </div>
            <div
                    class="publication"
                    v-for="publication of filteredPublications.values()">
                <div class="publication-content row">
                    <div class="column1">
                        <router-link
                                class="publication-name"
                                :to="{name: 'publication-detail', params: {'uuid': publication['uuid']}}">
                            <em>{{ publication['first_author'] }} et al. </em> {{ publication['title'] }}
                        </router-link>
                    </div>
                    <div class="column2">
                        <AuthorTagList :authors="publication['meta_authors']"/>
                    </div>
                    <div class="column3">
                        {{ publication['published'].slice(0,4) }}
                    </div>
                </div>
                <DropDownExtendBox>
                    <template v-slot:title>
                        <div>
                            Additional Information
                        </div>
                    </template>
                    <template v-slot:content>
                        <div class="additional-information">
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
                            <span class="date">
                                Published: {{ publication['published'].slice(0, 10) }}
                            </span>
                        </div>
                    </template>
                </DropDownExtendBox>
            </div>
        </div>
    </div>
</template>

<script>
    import api from '../common/api.service.js';
    import MapFilters from "../components/MapFilters";
    import MultiSelect from "../components/MultiSelect";
    import ClipboardInline from "../components/ClipboardInline";
    import DropDownExtendBox from "../components/DropDownExtendBox";
    import AuthorTagList from "../components/AuthorTagList";

    export default {
        name: "KitOpenMetrics",
        components: {AuthorTagList, DropDownExtendBox, ClipboardInline, MultiSelect, MapFilters},
        data() {
            return {
                api: new api.Api(),
                publications: new Map(),
                years: [],
                authors: [],
                selectedYears: [],
                selectedAuthors: [],
                filteredPublications: new Map(),
                metricsYear: {},
                metricsAuthor: {},
                total: 0,
            }
        },
        methods: {
            getPublications() {
                let self = this;
                return this.api.getPublicationList()
                    .then(function (publications) {
                        let result = new Map();
                        let years = new Set();
                        let authors = new Set();
                        for (let publication of publications) {
                            let uuid = publication['uuid'];
                            result.set(uuid, publication);

                            // Adding the publication year to the set
                            let year = publication['published'].slice(0, 4);
                            years.add(year);

                            // Adding all the meta authors to the set
                            for (let metaAuthor of publication['meta_authors']) {
                                authors.add(metaAuthor['full_name']);
                            }
                        }
                        self.publications = result;
                        self.years = Array.from(years);
                        self.authors = Array.from(authors);
                    })
            },
            onInput() {
                let result = new Map();

                this.resetMetrics();

                for (let [uuid, publication] of this.publications) {
                    let year = publication['published'].slice(0, 4);
                    if (this.selectedYears.includes(year)) {
                        for (let metaAuthor of publication['meta_authors']) {
                            let fullName = metaAuthor['full_name'];
                            if (this.selectedAuthors.includes(fullName)) {
                                result.set(uuid, publication);

                                this.increaseMetrics(this.metricsYear, year);
                                this.increaseMetrics(this.metricsAuthor, fullName);
                                this.total += 1;
                            }
                        }
                    }
                }
                this.filteredPublications = result;
            },
            increaseMetrics(metrics, key) {
                if (!!metrics[key]) {
                    metrics[key] += 1;
                } else {
                    metrics[key] = 1;
                }
            },
            resetMetrics() {
                this.metricsYear = {};
                this.metricsAuthor = {};
                this.total = 0;
            }
        },
        created() {
            this.getPublications();
        }
    }
</script>

<style scoped>
    .selection {
        display: flex;
        flex-direction: row;
    }

    .select.year {
        margin-right: 10px;
    }
    .select {
        padding: 5px;
        background-color: #e6e6e6;
        flex-grow: 1;
        border-radius: 2px;
    }

    .total {
        font-size: 1.2em;
    }

    .row {
        display: flex;
        flex-direction: row;
    }

    .header {
        padding: 10px;
        margin-bottom: 10px;
        background-color: #e6e6e6;
    }

    .publication {
        padding: 10px;

        margin-bottom: 10px;

        border-style: solid;
        border-width: 1px;
        border-color: #B9B9B9;
        border-radius: 2px;
    }

    .publication-name {
        font-size: 1.1em;
        color: black;
        text-decoration: none;
    }

    .column1 {
        flex-grow: 2;
        margin-right: 10px;
    }

    .column2 {
        min-width: 35%;
        max-width: 35%;
    }

    .column3 {
        min-width: 10%;
        max-width: 10%;
    }

    .additional-information {
        font-size: 0.9em;
        display: flex;
        flex-direction: column;
    }

    .additional-information>span {
        margin-bottom: 2px;
        color: gray;
    }
</style>
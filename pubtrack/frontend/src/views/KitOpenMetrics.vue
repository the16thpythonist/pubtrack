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
            <MultiSelect
                    class="select pof"
                    header="POF Structure"
                    :choices="pofs"
                    v-model="selectedPofs"
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
            <h4>Publications by POF:</h4>
            <div class="metric" v-for="(amount, pof) in metricsPof">
                {{ pof }}: {{ amount }}
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
                <div class="column4">
                    POF Structure
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
                    <div class="column4">
                        {{ publication['pof_structure'] }}
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
                pofs: [],
                years: [],
                authors: [],
                selectedPofs: [],
                selectedYears: [],
                selectedAuthors: [],
                filteredPublications: new Map(),
                metricsYear: {},
                metricsAuthor: {},
                metricsPof: {},
                total: 0,
            }
        },
        methods: {
            comparePublications(firstPublication, secondPublication) {
                let comparisonKey = 'first_author';
                if (firstPublication[comparisonKey] > secondPublication[comparisonKey]) {
                    return 1;
                } else if (firstPublication[comparisonKey] < secondPublication[comparisonKey]) {
                    return -1;
                } else {
                    return 0;
                }
            },
            getPublications() {
                let self = this;
                return this.api.getPublicationList()
                    .then(function (publications) {
                        publications.sort(self.comparePublications);

                        let result = new Map();

                        let years = new Set();
                        let authors = new Set();
                        let pofs = new Set()

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

                            // Adding the POF structure to the set
                            if (publication['pof_structure']) {
                                pofs.add(publication['pof_structure'])
                            } else {
                                pofs.add('NONE');
                            }

                        }
                        self.publications = result;

                        self.years = Array.from(years);
                        self.authors = Array.from(authors);
                        self.pofs = Array.from(pofs);
                    })
            },
            onInput() {
                let result = new Map();

                this.resetMetrics();

                for (let [uuid, publication] of this.publications) {
                    let year = publication['published'].slice(0, 4);
                    if (this.selectedYears.includes(year)) {
                        let pofStructure = publication['pof_structure'] ? publication['pof_structure'] : 'NONE';
                        for (let metaAuthor of publication['meta_authors']) {
                            let fullName = metaAuthor['full_name'];
                            if (this.selectedAuthors.includes(fullName) && this.selectedPofs.includes(pofStructure)) {
                                this.increaseMetrics(this.metricsAuthor, fullName);

                                if (!result.get(uuid)) {
                                    this.increaseMetrics(this.metricsPof, pofStructure);
                                    this.increaseMetrics(this.metricsYear, year);
                                    this.total += 1;
                                }

                                result.set(uuid, publication);
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
                this.metricsPof = {};
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

    .select.author {
        margin-left: 10px;
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
        min-width: 25%;
        max-width: 25%;
    }

    .column3 {
        min-width: 10%;
        max-width: 10%;
    }

    .column4 {
        min-width: 20%;
        max-width: 20%;
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
<template>
    <div class="kitopen-coverage-analytics">
        <h1 class="title">KITOpen Analytics</h1>

        <!-- Add the filters -->
        <ArrayFilters
                :base="publications"
                v-model="filteredPublications"
                :filters="filters">
        </ArrayFilters>

        <InputArrayFilter
                :base="filteredPublications"
                v-model="filteredPublications2"
                :filter="pofFilter">
        </InputArrayFilter>

        <!-- Make this its own widget -->
        <PublicationSelect
                v-model="selectedPublications"
                :publications="filteredPublications2">
        </PublicationSelect>

        <!-- Button for export to pdf or smth. else -->
        <ArrayMapDisplay
                title="Selected Publications:"
                :value="selectedPublications"
                :mapFunc="exportPublication">
        </ArrayMapDisplay>
    </div>
</template>

<script>
    import api from '../common/api.service.js';

    // Vue Components
    import PublicationSelect from "../components/PublicationSelect";
    import ArrayFilters from "../components/ArrayFilters";
    import ArrayMapDisplay from "../components/ArrayMapDisplay";
    import InputArrayFilter from "../components/InputArrayFilter";

    export default {
        name: "KITOpenCoverage",
        components: {
            ArrayMapDisplay,
            PublicationSelect,
            ArrayFilters,
            InputArrayFilter
        },
        data: function () {
            return {
                api: new api.Api(),
                publications: [],
                filteredPublications: [],
                filteredPublications2: [],
                selectedPublications: {},
                filters: {
                    kitopen:  {
                        name:       'On KITOpen',
                        active:     false,
                        func:       function (publications) {
                            return publications.filter(function (publication) {
                                return publication['on_kitopen'];
                            })
                        }
                    },
                    notkitopen:  {
                        name:       'Not On KITOpen',
                        active:     false,
                        func:       function (publications) {
                            return publications.filter(function (publication) {
                                return !publication['on_kitopen'];
                            })
                        }
                    },
                    warning: {
                        name:       'Unresolved Warnings',
                        active:     false,
                        func:       function (publications) {
                            return publications.filter(function (publication) {
                                return publication['status']['type'] === 'warn';
                            })
                        }
                    },
                    permitted: {
                        name:       'Permitted Warnings',
                        active:     false,
                        func:       function (publications) {
                            return publications.filter(function (publication) {
                                return publication['status']['type'] === 'perm';
                            })
                        }
                    }
                },
                pofFilter: {
                    placeholder: 'POF Structure must include:',
                    func(publications, input) {
                        return publications.filter(function (publication) {
                            if (input === '') return true;
                            return (publication['pof_structure'] !== null) &&
                                   (publication['pof_structure'].includes(input));
                        })
                    }
                },
                selectedPublicationsJSON: ''
            }
        },
        methods: {
            getAuthors: function() {
                let self = this;
                this.api.getAuthorList()
                    .then(function (data) {
                        self.authors = data.results;
                    })
                    .catch(function (error) {
                        console.log(error);
                    });
            },
            getPublications: function () {
                let self = this;
                this.api.getPublicationList()
                    .then(function (publications) {
                        self.publications = publications;
                    })
            },
            exportPublication: function (publication) {
                return {
                    'title':        publication['title'],
                    'on_kitopen':   publication['on_kitopen'],
                    'meta_authors': publication['meta_authors'].map(function (metaAuthor) {
                        return {
                            'slug':         metaAuthor['slug'],
                            'full_name':    metaAuthor['first_name'] + ' ' + metaAuthor['last_name']
                        }
                    })
                }
            }
        },
        created() {
            this.getPublications();
        }
    }
</script>

<style scoped>
    .kitopen-coverage-analytics {
        display: flex;
        flex-direction: column;
    }

    .kitopen-coverage-analytics>* {
        margin-bottom: 25px;
    }

    h1.title {
        margin-bottom: 40px;
    }
</style>
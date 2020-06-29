<template>
    <div class="kitopen-coverage-analytics">
        <h1 class="title">KITOpen Analytics</h1>

        <!-- Add the filters -->
        <MapFilters
                :base="publications"
                v-model="filteredPublications"
                :filters="filters">
        </MapFilters>

        <InputMapFilter
                title="Search in POF and title:"
                :base="filteredPublications"
                v-model="filteredPublications2"
                :filter="pofFilter">
        </InputMapFilter>

        <!-- Make this its own widget -->
        <PublicationSelect
                v-model="selectedPublications"
                :publications-map="filteredPublications2">
        </PublicationSelect>

        <h1>Actions</h1>

        <TabbedBox
                height="400px"
                default="email"
                :headers="{email: 'Generate Change Request', search: 'KITOpen Search Parameters', import: 'KITOpen Import'}">
            <template v-slot:email>
                <InputTextGenerator
                        :value="selectedPublications"
                        :inputs="parametersEmail"
                        :generate="generateEmail"/>
            </template>
        </TabbedBox>


    </div>
</template>

<script>
    import api from '../common/api.service.js';

    // Vue Components
    import PublicationSelect from "../components/PublicationSelect";
    import MapFilters from "../components/MapFilters";
    import InputMapFilter from "../components/InputMapFilter";
    import TabbedBox from "../components/TabbedBox";
    import InputTextGenerator from "../components/InputTextGenerator";

    export default {
        name: "KITOpenCoverage",
        components: {
            InputTextGenerator,
            MapFilters,
            InputMapFilter,
            PublicationSelect,
            TabbedBox
        },
        data: function () {
            return {
                api: new api.Api(),
                publications: new Map(),
                filteredPublications: new Map(),
                filteredPublications2: new Map(),
                selectedPublications: {},
                // FILTERING THE PUBLICATIONS
                filters: {
                    notkitopen:  {
                        name:       'Not On KITOpen',
                        active:     false,
                        func:       function (publications) {
                            let result = new Map();
                            for (let [uuid, publication] of publications) {
                                if (!publication['on_kitopen']) {result.set(uuid, publication); }
                            }
                            return result;
                        }
                    },
                    warning: {
                        name:       'Unresolved Warning',
                        active:     false,
                        func:       function(publications) {
                            let result = new Map();
                            for (let [uuid, publication] of publications) {
                                if (publication['status']['type'] === 'warn') {result.set(uuid, publication); }
                            }
                            return result;
                        }
                    }
                },
                pofFilter: {
                    placeholder: 'Must include...',
                    func(publications, input) {
                        let result = new Map();
                        for (let [uuid, publication] of publications) {
                            let in_title = publication['title'].toLowerCase().includes(input);
                            let in_pof = publication['pof_structure'] !== null &&
                                         publication['pof_structure'].includes(input);

                            if (in_title || in_pof) {
                                result.set(uuid, publication);
                            }
                        }
                        return result;
                    }
                },
                // ACTIONS TO PROCESS SELECTED PUBLICATIONS
                // ****************************************
                // EMAIL GENERATION
                parametersEmail: {
                    fullname: {
                        label:          'Full Name',
                        description:    'The full name will be inserted as the sender in the footer of the mail body',
                        placeholder:    'Enter Full Name...'
                    },
                    newpof: {
                        label:          'New POF Structure',
                        description:    'This will the pof structure to which all the publications are to be changed to',
                        placeholder:    'Enter Valid POF Structure...'
                    }
                },
                generateEmail(parameters, value) {
                    // value in this case is the object of selected publications
                    let parts = [
                        'Dear KITOpen Team,S\n',
                        'Would you be so kind to change the POF structures on the following publications:\n'
                    ];
                    for (let [uuid, publication] of Object.entries(value)) {
                        let item = ` - KITOpen ID: ${publication['kitopen_id']}\n` +
                                   `   New POF Structure: ${parameters['newpof']}\n`;
                        parts.push(item)
                    }
                    parts.push('Thank you!\n');
                    parts.push('Best regards,');
                    parts.push(parameters['fullname']);
                    return parts.join('\n');
                }
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
                        let result = new Map();
                        // 27.06.2020 Changed it so that it now assigns the porperties of an object, because
                        // I essentially want to store them in an assoc array (=object)
                        for (let publication of publications) {
                            let uuid = publication['uuid'];
                            result.set(uuid, publication);
                        }
                        self.publications = result;
                    })
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
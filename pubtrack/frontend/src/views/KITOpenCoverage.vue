<template>
    <div class="kitopen-coverage-analytics">
        <h1 class="title">KITOpen Analytics</h1>

        <!-- Explanation -->
        <p>
            This page can be used to monitor the status of all the publications within the pubtrack database.
            On default, the list view below contains every publication currently known to this pubtrack instance. Each
            row represents one publication. To further narrow down the selection of displayed publications, the
            "Filters" section below can be used. Simply check the boxes to apply the corresponding filters.
            Additionally, the search field can be used to further filter by the inclusion of an arbitrary sub string
            within the title or the POF structure of a publication.
        </p>

        <p>
            The list view of the publications contains five columns, which represent the following information (in that
            order): The first author and title of the publication, a list of all the observed authors, which are also
            authors of that specific publication, a boolean indication of whether or not the publication is on
            KITOpen or not, the POF structure of the publication (if one exists) and finally a checkbox to select the
            publication to apply group actions. <br>
            Additionally the arrow in the lower left-hand corner of a row can be used to open a dropdown view for each
            publication which contains additional information about it, as well as the <em>Status Editor</em>
        </p>

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
                :headers="{email: 'POF Change Request', search: 'KITOpen Search Parameters'}">
            <template v-slot:email>
                <h3>Instructions</h3>
                <p>
                    The widget below will automatically generate an email body to form a request to the KITOpen
                    Support team. This email will request a change of the POF structure of all the selected
                    publications to a different POF structure.
                </p>
                <p>
                    To generate the email content please enter your full name (which will be used in the footer section
                    of the email to identify yourself) and the string name of the new POF structure to which all the
                    publications are supposed to be changed to.<br>
                    After entering the details hit the <em>Generate!</em> button and the email content will appear
                    within the text area below.
                </p>
                <InputTextGenerator
                        :value="selectedPublications"
                        :inputs="parametersEmail"
                        :generate="generateEmail"/>
            </template>
            <template v-slot:search>
                <h3>Instructions</h3>
                <p>
                    Visit the <a href="https://dbkit.bibliothek.kit.edu/start.php" target="_blank">KITOpen Depositing and Publishing</a>
                    web application.
                </p>
                <p>
                    Navigate to the <em>Search Form</em>, which is typically displayed on the left-hand side of the
                    screen. Once in the search use the list of KITOpen ID's below to open the individual publications.
                    Do so by copying the ID's below and inserting them into the search box <em>KITOpen ID</em> before
                    hitting the enter key.<br>
                    The ID's in the list below can be copied to the clipboard automatically by pressing the icon beside
                    them. After pressing this icon the ID will also turn gray to visually indicate, that it has already
                    been copied.
                </p>
                <p>
                    Once a new page opens click the green <em>Show search result</em> button in the upper right hand
                    corner of the screen to view the publication details. You can now proceed to edit the publication...
                </p>
                <p>
                    ID's of the selected publications:
                </p>
                <div
                        style="margin-bottom: 10px;"
                        v-for="publication of selectedPublications">
                    <div style="margin-bottom: 5px; font-size: 0.9em; color: gray;">
                        {{ publication['title'] }}
                    </div>
                    <ClipboardInline >
                        {{publication['kitopen_id']}}
                    </ClipboardInline>
                </div>

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
    import ClipboardInline from "../components/ClipboardInline";

    export default {
        name: "KITOpenCoverage",
        components: {
            ClipboardInline,
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
                    },
                    selected: {
                        name:       'Only Selected',
                        active:     false,
                        func:       function(publications) {
                            let result = new Map();
                            for (let [uuid, publication] of publications) {
                                if (publication['selected']) {result.set(uuid, publication); }
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
            getPublications: function () {
                let self = this;
                this.api.getPublicationList()
                    .then(function (publications) {
                        publications.sort(self.comparePublications)
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

    p {
        margin-top: 5px;
    }

    h1.title {
        margin-bottom: 20px;
    }
</style>
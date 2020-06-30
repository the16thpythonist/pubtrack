<template>
    <div class="container">
        <div class="success">
            <h1>{{ publication['title'] }}</h1>
            <div class="authors">
                {{ authorsString() }}
            </div>

            <div class="main">
                <div class="info doi">
                    DOI: <a :href="publication['doi_url']">{{ publication['doi'] }}</a>
                </div>
                <div class="info published">
                    Published: {{ publication['published'] }}
                </div>
            </div>

            <h2>Additional Information</h2>

            <div class="pubtrack">
                <div class="info uuid">
                    UUID: {{ publication['uuid'] }}
                </div>
                <div class="info modified">
                    Modified: {{ publication['modified'] }}
                </div>
                <div class="meta-authors">

                </div>
            </div>

            <div class="kitopen">
                <div class="info kitopen-id">
                    KITOpen ID:
                    <span v-if="publication['on_kitopen']">
                        <a :href="publication['kitopen_url']">{{ publication['kitopen_id'] }}</a>
                    </span>
                    <span v-else>
                        -
                    </span>
                </div>
                <div class="info kitopen-pof">
                    POF Structure: {{ publication['on_kitopen'] ? publication['pof_structure'] : '-' }}
                </div>
            </div>

            <div class="scopus">

            </div>
                <div class="info scopus-id">
                    Scopus ID:
                    <span v-if="publication['scopus_id']">
                        <a :href="publication['scopus_url']">{{ publication['scopus_id'] }}</a>
                    </span>
                    <span v-else>
                        -
                    </span>
                </div>
            <h2>

            </h2>

            <PublicationStatusEditor v-model="publication"/>
        </div>
    </div>
</template>

<script>
    import api from "../common/api.service.js";

    import PublicationStatusEditor from "../components/PublicationStatusEditor";
    import DropDownExtendBox from "../components/DropDownExtendBox";

    export default {
        name: "PublicationDetail",
        components: {
            DropDownExtendBox,
            PublicationStatusEditor
        },
        props: {
            uuid: {
                type:       String,
                required:   true
            }
        },
        data() {
            return {
                api: new api.Api(),
                publication: {}
            }
        },
        methods: {
            getPublication() {
                let self = this;
                this.api.getPublicationDetail(this.uuid)
                    .then(function (publication) {
                        console.log(publication);
                        self.publication = publication;
                    })
            },
            authorsString() {
                let author_strings = [];
                for (let author of this.publication['authors']) {
                    author_strings.push(`${author['first_name'][0]}. ${author['last_name']}`);
                }
                return author_strings.join(', ')
            }
        },
        created() {
            this.getPublication();
        }
    }
</script>

<style scoped>
    .info-container {
        display: flex;
        flex-direction: column;
    }

    .info-container>span {
        margin-bottom: 10px;
    }

    .info {
        margin-bottom: 10px;
    }

    .success>* {
        margin-bottom: 20px;
    }

    .success h2 {
        margin-top: 30px;
        font-size: 1.2em;
    }

</style>
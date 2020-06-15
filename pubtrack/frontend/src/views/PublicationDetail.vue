<template>
    <div class="container">
        <div class="success">
            <h2>Publishing Information</h2>
            <div class="info-container">
                <span>Title: {{ publication['title'] }}</span>
                <span>Published: {{ publication['published'] }}</span>
            </div>

            <h2>KITOpen Information</h2>
            <div class="info-container">
                <span>On KITOpen: {{ publication['on_kitopen'] }}</span>
                <span>KITOpen ID: {{ publication['kitopen_id'] }} </span>
            </div>

            <h2>Publication Status</h2>
            <PublicationStatusEditor v-model="publication">
            </PublicationStatusEditor>
        </div>
    </div>
</template>

<script>
    import api from "../common/api.service.js";

    import PublicationStatusEditor from "../components/PublicationStatusEditor";

    export default {
        name: "PublicationDetail",
        components: {
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

    .success>* {
        margin-bottom: 20px;
    }

    .success>h2 {
        margin-top: 30px;
    }


</style>
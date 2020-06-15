<template>
    <div class="container">
        <h1>Known Publications</h1>
        <div class="item" v-for="publication in publications" :key="publication['uuid']">
            <router-link :to="{name: 'publication-detail', params: {'uuid': publication['uuid']}}">
                {{ publication['title'] }}
            </router-link>
        </div>
    </div>
</template>

<script>
    import api from "../common/api.service.js";

    export default {
        name: "PublicationList",
        data() {
            return {
                api: new api.Api(),
                publications: []
            }
        },
        methods: {
            getPublications() {
                let self = this;
                this.api.getPublicationList()
                    .then(function (publications) {
                        self.publications = publications;
                    })
            }
        },
        created() {
            this.getPublications()
        }
    }
</script>

<style scoped>

</style>
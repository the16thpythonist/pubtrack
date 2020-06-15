<template>
    <div class="container">
        <h1>Observed Authors</h1>
        <div class="item" v-for="author in authors" :key="author['slug']">
            <router-link :to="{name: 'author-detail', params: {'slug': author['slug']}}">
                {{ author['first_name'] }} {{ author['last_name'] }}
            </router-link>
        </div>
    </div>
</template>

<script>

    import api from "../common/api.service.js";

    export default {
        name: "AuthorList",
        data: function () {
            return {
                api: new api.Api(),
                authors: []
            }
        },
        methods: {
            getAuthors: function () {
                let self = this;
                this.api.getMetaAuthorList()
                    .then(function (meta_authors) {
                        self.authors = meta_authors;
                    })
            }
        },
        created() {
            this.getAuthors();
        }
    }
</script>

<style scoped>

</style>
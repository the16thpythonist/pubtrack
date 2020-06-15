<template>
    <div class="container">
        <div class="error" v-if="hasError">
            An author with this slug does not exists
        </div>
        <div class="success" v-else>
            <h2>Personal Information</h2>
            <div class="personal-info">
                <span>First Name: {{ metaAuthor['first_name'] }}</span>
                <span>Last Name: {{ metaAuthor['last_name'] }}</span>
                <span>Profile Created: {{ metaAuthor['created'] }}</span>
            </div>
            <h2>Affiliated Institutions</h2>
            <div class="institutions">
                <div
                        class="institution-element"
                        v-for="institution in metaAuthor['institutions']"
                        :key="institution['slug']">
                    {{ institution['name'] }} ({{ institution['city'] }})
                </div>
            </div>
            <h2>Publications</h2>
            <div class="publications">
                <div
                        class="author-profile"
                        v-for="author in metaAuthor['authors']"
                        :key="author['slug']">
                    <h4>Profile: {{ author['first_name'] }} {{ author['last_name'] }}</h4>
                    <div
                            class="publication-element"
                            v-for="publication in author['publications']"
                            :key="publication['uuid']">
                        {{ publication['title'] }} (ID: {{ publication['uuid'] }})
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import api from "../common/api.service.js";

    export default {
        name: "AuthorDetail",
        props: {
            slug: {
                type:       String,
                required:   true
            }
        },
        data: function() {
            return {
                api: new api.Api(),
                hasError: false,
                metaAuthor: {}
            }
        },
        methods: {
            getMetaAuthor: function () {
                let self = this;
                this.api.getMetaAuthor(this.slug)
                    .then(function (metaAuthor) {
                        self.metaAuthor = metaAuthor;
                    })
                    .catch(function (error) {
                        console.log(error);
                        self.hasError = true;
                    });
            }
        },
        created() {
            this.getMetaAuthor();
        }
    }
</script>

<style scoped>
    .personal-info {
        display: flex;
        flex-direction: column;
    }

    .success>* {
        margin-bottom: 20px;
    }

    .success>h2 {
        margin-top: 30px;
    }

    .personal-info>span {
        margin-bottom: 10px;
    }
</style>
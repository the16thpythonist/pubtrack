<template>
    <div class="container">
        <router-link
                class="publication-author"
                v-for="author in authors"
                :key="author['slug']"
                :to="{name: 'author-detail', params: {slug: author['slug']}}">
            {{ author['full_name'] }}
        </router-link>
    </div>
</template>

<script>
    export default {
        name: "AuthorTagList",
        props: {
            authors: {
                type:       Array,
                required:   true
            }
        }
    }
</script>

<style scoped>
    .publication-author {
        display: inline-flex;
        position: relative;

        height: 22px;
        padding-right: 5px;
        padding-left: 5px;
        margin-bottom: 5px;

        text-align: center;
        text-decoration: none;
        vertical-align: middle;
        line-height: 22px;
        font-size: 0.9em;
        font-family: sans-serif;

        color: #373737;
        background-color: rgba(0,0,0,0.25);

        border-radius: 0px 2px 2px 0px;
    }

    .publication-author:before {
        content: "";
        position: absolute;

        width: 0;
        height: 0;
        border-top: 11px solid transparent;
        border-right: 8px solid rgba(0,0,0,0.25);
        border-bottom: 11px solid transparent;

        transform: translate(-13px, 0px);
    }
</style>
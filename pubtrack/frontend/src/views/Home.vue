<template>
    <div class="container">
        <div class="header">README.md</div>
        <VueShowdown
                class="readme"
                flavor="github"
                :options="{ emoji: true, simpleLineBreaks: false }"
                :markdown="content"/>
    </div>
</template>

<script>

    import api from '../common/api.service.js';
    import { VueShowdown } from 'vue-showdown';

    export default {
        name: "Home",
        components: {
            VueShowdown
        },
        data() {
            return {
                api: new api.Api(),
                content: ''
            }
        },
        methods: {
            getReadme() {
                let self = this;
                this.api.get('readme/')
                    .then(function (data) {
                       self.content = data['content'];
                    });
            }
        },
        created() {
            this.getReadme();
        }
    }
</script>

<style scoped>
    .container {
        font-family: Helvetica, Arial, sans-serif;

        padding: 20px;
        border: 1px solid #e1e4e8;
        border-radius: 6px;
    }

    .header {
        font-weight: bold;
    }

    .readme {
        padding: 20px;
    }
</style>
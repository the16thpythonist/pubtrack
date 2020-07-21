<template>
    <div class="footer">
        <div class="left">
            &copy; Jonas Teufel
        </div>
        <div class="right">
            <h3>Contact</h3>
            <div class="contact">
                <div class="contact-element">
                    <div class="label">Name:</div>
                    <div class="value">{{ contact['full_name'] }}</div>
                </div>
                <div class="contact-element">
                    <div class="label">Location:</div>
                    <div class="value">{{ contact['location'] }}</div>
                </div>
                <div class="contact-element">
                    <div class="label">Email:</div>
                    <a
                            class="value"
                            style="color: white;"
                            :href="`mailto:${contact['email']}`"
                            type="">
                        {{ contact['email'] }}
                    </a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import api from "../common/api.service.js";

    export default {
        name: "Footer",
        data() {
            return {
                api: new api.Api(),
                contact: {}
            }
        },
        created() {
            let self = this;
            this.api.get('contact/', {})
                .then(function (contact) {
                    console.log(contact);
                    self.contact = contact;
                });
        }
    }
</script>

<style scoped>

    .footer {
        display: flex;
        flex-direction: row;

        margin-top: 50px;
        padding: 20px;

        background-color: #24292e;
        color: white;
      }

    h3 {
        margin-top: 0;
        margin-bottom: 2px;
    }

    .left, .right {
        min-width: 50%;
        clear: both;
    }

    .contact {
        display: flex;
        flex-direction: column;
    }

    .contact-element {
        display: flex;
        margin-bottom: 2px;

        min-width: 100%;

        flex-direction: row;
    }

    .contact .label {
        min-width: 30%;
        max-width: 30%;
    }

    .contact .value {
        min-width: 65%;
        max-width: 70%;
    }
</style>
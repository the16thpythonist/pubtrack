import { CSRF_TOKEN } from "./csrf_token.js"
import axios from 'axios'

function Api() {

    // I ll have to pass this in via the template
    const BASE_URL = process.env.VUE_APP_API_URL;

    // PRIVATE METHODS
    this.axios = axios.create({
        baseURL: BASE_URL,
        timeout: 1000,
        responseType: 'json',
        withCredentials: true,
        headers: {
            'content-type':         'application/json',
            'Accept':               'application/json',
            'X-CSRFToken':          CSRF_TOKEN
        }
    });

    // PUBLIC METHODS

    this.get = function(endpoint, params) {
        let config = {
            params: params
        };
        return this.axios.get(endpoint, config)
            .then(function (response) {
                return response.data;
            })
    };

    this.post = function (endpoint, data) {
        let config = {
            data: data
        };
        return this.axios.post(endpoint, config);
    };

    this.patch = function (endpoint, data) {
        let config = {
            data: data
        };
        return this.axios.patch(endpoint, data, config);
    };


    this.getAuthorList = function() {
        let endpoint = '/authors/';
        return this.get(endpoint, {});
    };

    this.getMetaAuthorList = function () {
        let endpoint = '/meta-authors/';
        return this.get(endpoint, {})
            .then(function (data) {
                return data.results;
            });
    };

    this.getMetaAuthorDetail = function (slug) {
        let endpoint = `/meta-authors/${slug}/`;
        return this.get(endpoint, {});
    };

    this.getMetaAuthor = function (slug) {
        return this.getMetaAuthorDetail(slug)
            .then(function (metAuthor) {
                let institutions = [];
                for (let author of metAuthor['authors']) {
                    institutions = [...author['institutions'], ...institutions]
                }
                metAuthor['institutions'] = institutions;
                return metAuthor;
            });
    };

    this.setPublicationStatusPermitted = function (uuid, solution) {
        let patch = {
            'type':         'perm',
            'solution':     solution,
        };
        return this.patchPublicationStatus(uuid, patch)
            .then(function (response) {
                return response.data;
            });
    };

    this.patchPublicationStatus = function (uuid, patch) {
        let endpoint = `/publication-statuses/${uuid}/`;
        return this.patch(endpoint, patch)
            .then(function (response) {
                return response.data;
            });
    };

    this.getPublicationList = function () {
        let endpoint = '/publications/';
        return this.get(endpoint, {})
            .then(function (data) {
                return data.results;
            });
    };

    this.getPublicationDetail = function (uuid) {
        let endpoint = `/publications/${uuid}/`;
        return this.get(endpoint, {});
    };

    this.getAuthorDetail = function(slug) {
        let endpoint = `/authors/${slug}/`;
        return this.get(endpoint, {});
    };
}


export default {
    Api: Api
}
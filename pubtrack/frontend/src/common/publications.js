

function getPublicationMetaAuthors(publication) {
    let metaAuthors = [];
    for (let key in publication['authors']) {
        let author = publication['authors'][key];
        if (author['meta_author'] !== null) {
            console.log(author);
            metaAuthors.push(author['meta_author']);
        }
    }
    console.log(metaAuthors);
    return metaAuthors;
}

export default {
    getPublicationMetaAuthors: getPublicationMetaAuthors
}
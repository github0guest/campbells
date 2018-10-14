new Vue({
    el: '#character',
    data: {
        info: null,
        loading: true,
        errored: false,
        newCharacter: 'Eileen',
    },
    methods: {
        enterCharacter(character) {
            this.newCharacter = character;
            axios
                .get('http://127.0.0.1:5000/json/dates/?character=' + this.newCharacter )
                .then(response => (this.info = response.data))
                .catch(error => {
                    console.log(error);
                    this.errored = true
                })
                .finally(() => this.loading = false)
        },
        renderComic(date) {
            return date + `<img src="http://127.0.0.1:5000/static/images/` + date + `.gif">`
        }
    },
});


new Vue({
    el: '#date',
    data: {
        info: null,
        loading: true,
        errored: false,
        dateSearch: '1988-04-11',
    },
    methods: {
        enterDate(date) {
            this.dateSearch = date;
            axios
                .get('http://127.0.0.1:5000/json/characters/?date=' + this.dateSearch )
                .then(response => (this.info = response.data))
                .catch(error => {
                    console.log(error);
                    this.errored = true
                })
                .finally(() => this.loading = false)
        },
        renderComic(date) {
            return `<img src="http://127.0.0.1:5000/static/images/` + this.dateSearch + `.gif">`
        }
    },
});


new Vue({
    el: '#search',
    data: {
        info: null,
        loading: true,
        errored: false,
        searchTerm: 'Skeeter Falls',
    },
    methods: {
        search(term) {
            this.newSearchTerm = term;
            axios.post('http://127.0.0.1:5000/json/search/', JSON.stringify({text: this.searchTerm}))
                .then(response => (this.info = response.data))
                .catch(error => {
                    console.log(error);
                    this.errored = true
                })
                .finally(() => this.loading = false)
        },
        renderComic(date) {
            return date + `<img src="http://127.0.0.1:5000/static/images/` + date + `.gif">`
        }
    },
});

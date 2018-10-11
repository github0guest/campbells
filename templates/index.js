new Vue({
    el: '#root',
    data: {
        info: null,
        searchTerm: 'test',
        postBody: JSON.stringify({text: this.searchTerm}),
        errors: [],
        axiosConfig: '{"Content-Type": "application/json"}',
    },
    methods: {
        postPost() {
            axios.post('http://127.0.0.1:5000/json/searchTest/', JSON.stringify({text: "test"}))
                .then(response => (this.info = response.data))
                .catch(e => {
                    this.errors.push(e)
                })
        }
    }
});
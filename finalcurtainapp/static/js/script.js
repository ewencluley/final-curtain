$(document).ready(function() {
    $('#searchForm').on('submit', event => {
        $.ajax( {
            data: {
                q: $('#search').val(),
            },
            type: 'GET',
            url: '/search'
        }).done(response => {
            $('#results').empty()
            response.forEach(i => {
                $('#results').append(`<a class="list-group-item" id="${i.id}" href="/cast/${i.id}">${i.id}</a>`)
            })
        })
        event.preventDefault()
    });
})
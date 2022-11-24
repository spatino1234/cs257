/*
 * types.js
 * Jeff Ondich, 27 April 2016
 * Updated, 5 November 2020
 * 
 * Modified by Ruben Boero and Serafin Patino
 */

window.onload = initialize;

var alternatingLineColor = '#E2FCFF'

function initialize() {
    loadTypesSelector();

    // get the go button, call the on click function when the button is pressed
    let go_button = document.getElementById('go_button');
    if (go_button){
        go_button.onclick = onGoButtonClicked;
    }

    // wait for the enter button to be pressed, search when it is clicked
    let search_bar = document.getElementById('search_bar');
    if (search_bar) {
        search_bar.addEventListener('keyup', function(event){
            event.preventDefault();
            if (event.keyCode === 13) {
                go_button.click();
            }
        })
    }
}

// Returns the HTML for the table to display search results
function createTableHTML(search_results, alternatingLineColor) {
    let tableBody = '';

    // Create the header of the table
    tableBody += '<tr id = "table_header"><td>Dex Number</td><td>Pokémon</td><td>Ability 1</td><td>Ability 2</td><td>Hidden Ability</td><td>Type 1</td><td>Type 2</td><td>Generation</td></tr>'
    // Create the body of the table
    for (let k = 0; k < search_results.length; k++) {
        let pokemon = search_results[k];

        let url = '/specific/' + pokemon['id']
        
        // everyother line will be a different color
        if (k % 2 == 0) {
            tableBody += '<tr><td>'+ pokemon['dex_num'] + '<td><a href = "' + url + '">'+ pokemon['name'] + '</a></td>' + 
            '<td>' + pokemon['ability1'] + '</td>' + '<td>' + pokemon['ability2'] + '</td>' + 
            '<td>' + pokemon['ability3'] + '</td>' + '<td>' + pokemon['type1'] + '</td>' + 
            '<td>' + pokemon['type2']+ '</td>' + '<td>' + pokemon['generation'].replace('generation', 'Generation') +
            '</td>' + '</td></tr>\n';
        } 
        else {
            tableBody += '<tr bgcolor="' + alternatingLineColor + '"><td>'+ pokemon['dex_num'] + '<td><a href = "' + 
            url + '">'+ pokemon['name'] + '</a>' + '<td>' + pokemon['ability1'] + '</td>' + '<td>' + 
            pokemon['ability2'] + '</td>' + '<td>' + pokemon['ability3'] + '</td>' + '<td>' + pokemon['type1'] + 
            '</td>' + '<td>' + pokemon['type2']+ '</td>' + '<td>' + 
            pokemon['generation'].replace('generation', 'Generation') + '</td>' + '</td></tr>\n';
        }        
    }
    return tableBody
}

// Returns the base URL of the API, onto which endpoint
// components can be appended.
function getAPIBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port
                    + '/api';
    return baseURL;
}

function onGoButtonClicked() { 
    var search_text = document.getElementById('search_bar').value
    var search_dropdown = document.getElementById('search_dropdown');
    var search_category = search_dropdown.value;

    if (search_text == '') {
        search_text = 'default'
    }
    let url = '/search_results/' + search_category + '/' + search_text;
    window.location.href = url
}

function loadTypesSelector() {
    let url = getAPIBaseURL() + '/types';

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(types) {
        let selectorBody = '';

        // start at k = 1 bc the first egg group is a null value
        for (let k = 1; k < types.length; k++) {
            let type = types[k];
            // using type radio to only allow one button to be selected at once
            // every 6th type ends a row
            if (k % 6 == 0) {
                selectorBody += '<td><input type="radio" onchange="onTypeSelectionChanged(event)" id="' + type + '" name="type_box"/>' + type + '</td></tr>'
            }
            else {
                selectorBody += '<td><input type="radio" onchange="onTypeSelectionChanged(event)" id="' + type + '" name="type_box"/>' + type + '</td>';
            }
            // onchange calls a function when the radio button is clicked
        }

        let selector = document.getElementById('type_selector');
        if (selector) {
            selector.innerHTML = selectorBody;
        }
    })

    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}

function onTypeSelectionChanged(event) {
    // event is the context around clicking the box
    // target is the check box, target.id is the text
    type = event.target.id

    let url = getAPIBaseURL() + '/type/' + type;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(pokemon_results) {
        let tableBody = createTableHTML(pokemon_results, alternatingLineColor)

        let typeResults = document.getElementById('type_results');
        if (typeResults) {
            typeResults.innerHTML = tableBody;
        }
        })

    .catch(function(error) {
    console.log(error);
    });
}
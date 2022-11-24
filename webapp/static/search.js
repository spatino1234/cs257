/*
 * search.js
 * Jeff Ondich, 27 April 2016
 * Updated, 5 November 2020
 * 
 * Modified by Ruben Boero and Serafin Patino
 */

window.onload = initialize;

function initialize() {
    let legendary_dropdown = document.getElementById('legendary_selector');
    if (legendary_dropdown){
        legendary_dropdown.onchange = onLegendaryCategorySelectionChanged;
    }
    
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
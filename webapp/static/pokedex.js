/*
 * pokedex.js
 * Jeff Ondich, 12 November 2020
 *
 * Adapted from the Chartist library samples.
 *   https://gionkunz.github.io/chartist-js/examples.html
 * 
 * Modified by Ruben Boero and Serafin Patino
 */
window.onload = initialize;

function initialize() {
    createBarChart();

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

function onGoButtonClicked() { 
    var search_text = document.getElementById('search_bar').value
    var search_dropdown = document.getElementById('search_dropdown');
    var search_category = search_dropdown.value;

    if (search_text == '') {
        search_text = 'default'
    }
    let url = '/search_results/' + search_category + '/' + search_text;
    window.location.href = url

    console.log('go button clicked')
}

function createBarChart() {
    let hp = parseInt(document.getElementById('hp').innerText);
    let atk = parseInt(document.getElementById('atk').innerText);
    let def = parseInt(document.getElementById('def').innerText);
    let spatk = parseInt(document.getElementById('spatk').innerText);
    let spdef = parseInt(document.getElementById('spdef').innerText);
    let spd = parseInt(document.getElementById('spd').innerText);

    var data = {
        labels: ['HP', 'ATK ', 'DEF','SP. ATK','SP. DEF', 'SPD'],
        series: [[hp, atk, def, spatk, spdef, spd]]

    };

    var options = {horizontalBars: true, reverseData: true,   axisY: {offset: 80}, high: 255, low: 0}

    new Chartist.Bar('#stats_chart', data, options);
}



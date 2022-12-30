
// Game variables
let loop_time = 10
let score = 0
let gradient_1;
let gradient_2;

let scroll_count;
let scroll_loop;
let scroll_t= 100
var gr = document.querySelector(':root')   

let time_color;
 // ----------------------- Button -----------------------
 let sound_off  = document.getElementById('sound_off')
 let sound_on   = document.getElementById('sound_on')
 const submit_btn = document.getElementById('submit')
 const quit       = document.getElementById('quit')

// HTML Game design attributs
const text_promt = document.getElementById('text_promt')
const  score_tag = document.getElementById('score_tag')


// Color time bar
function init_countdown_bar() {
    color_countdow_reset()
    if (!time_color) {time_color = setInterval(color_countdown, 10)}
} 
function color_countdow_reset() {
    gradient_1 = 1
    gradient_2 = 1
    gr.style.setProperty('--gradient_1', `${gradient_1}%`)
    gr.style.setProperty('--gradient_2', `${gradient_2}%`)
}
function color_countdown() {
    gradient_1 = gradient_1 + scroll_count
    gradient_2 = gradient_2 + scroll_count
    gr.style.setProperty('--gradient_1', `${gradient_1}%`)
    gr.style.setProperty('--gradient_2', `${gradient_2}%`)
}
function stop_color_bar(){clearInterval(time_color); time_color = null;}


// --------------------- text promt (Hard game) ---------------------
function init_text_promt(text) {
    scroll_count = 1 / loop_time; scroll_t= 100
    text_promt.innerHTML = text
    voice(text)
    if (!scroll_loop) {scroll_loop = setInterval(text_scroll, 10)}
}
function text_scroll() {
    scroll_t = scroll_t - 0.4
    gr.style.setProperty('--text_scroll', `${scroll_t}%`)
    if (scroll_t < -200) {
        stop_text()
    }}
function stop_text(){clearInterval(scroll_loop); scroll_loop = null}



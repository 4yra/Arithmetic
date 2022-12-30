// HTML Game design attributs
let volume = 0
const speach = window.speechSynthesis;
var msg = new SpeechSynthesisUtterance();
// --------------------- Sound ---------------------
// Text to speach
function voice(text) {
    console.log(text);
    msg.rate = 0.9; // From 0.1 to 10
    msg.pitch = 2; // From 0 to 2
    msg.volume = volume;
    msg.text = text;
    speach.speak(msg);
}
function point_score_sound() {
    var sound = new Audio('./static/sound/score_sound.mp3')
    sound.volume = 0.2; sound.play()
}

function sound(bool) {
    sound_on.classList.toggle('hide')
    sound_off.classList.toggle('hide')
    if (bool == 0) {
        volume = 0.5
        msg.volume = volume;
        voice(exp_string)
        console.log(`Sound On ${volume}`);
    }else {
        speach.cancel()
        volume = 0
        msg.volume = volume;
        console.log(`Sound Off ${volume}`);
    }
}
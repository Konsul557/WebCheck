console.log("=== Script start ===");
/**
 * Выбор режима входа
 */

var currentMode = 'sign-in';

var buttonSignIn = document.getElementById('button-sign-in');
var buttonSignUp = document.getElementById('button-sign-up');

buttonSignIn.addEventListener('click', function() {
    currentMode = 'sign-in';
    changeForm();
});

buttonSignUp.addEventListener('click', function() {
    currentMode = 'sign-up';
    changeForm();
});

document.getElementById('in-btn').style.display = 'none';
document.getElementById('email').style.display = 'none';
document.getElementById('p_email').style.display = 'none';
var changeForm = function() {
    if (currentMode == 'sign-in') {
        document.getElementById('email').style.display = 'none';
        document.getElementById('p_email').style.display = 'none';
        document.getElementById('reg-btn').style.display = 'block';
        document.getElementById('in-btn').style.display = 'none';
    }
    if (currentMode == 'sign-up') {
        document.getElementById('email').style.display = 'block';
        document.getElementById('p_email').style.display = 'block';
        document.getElementById('reg-btn').style.display = 'none';
        document.getElementById('in-btn').style.display = 'block';

    }
}
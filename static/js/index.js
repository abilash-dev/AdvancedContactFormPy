/*

© abilash-dev | https://github.com/abilash-dev/AdvancedContactFormPy

*/

function handleCredentialResponse(response) {
    const data = jwt_decode(response.credential);
    document.getElementById('name-hidden').value = data.name;
    document.getElementById('email-hidden').value = data.email;
    document.getElementById('contact-form').style.display = 'block';
    document.getElementById('signin-section').style.display = 'none';
}

(function (d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "https://cdn.jsdelivr.net/npm/jwt-decode/build/jwt-decode.min.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'jwt-decode'));

setTimeout(() => {
    const flashMessages = document.querySelectorAll('.flash');
    flashMessages.forEach(flash => flash.remove());
}, 6000);



function showManualLogin() {
    document.getElementById('signin-section').style.display = 'none';
    document.getElementById('contact-form').style.display = 'block';
    document.getElementById('manual-fields').style.display = 'block';

    document.getElementById('name-hidden').value = '';
    document.getElementById('email-hidden').value = '';
}


document.getElementById('contact-form').addEventListener('submit', function (e) {
    const manualFieldsVisible = document.getElementById('manual-fields').style.display !== 'none';
    const manualName = document.getElementById('manual-name');
    const manualEmail = document.getElementById('manual-email');
    const nameHidden = document.getElementById('name-hidden');
    const emailHidden = document.getElementById('email-hidden');
    const name = manualName.value.trim();
    const email = manualEmail.value.trim();


    if (manualFieldsVisible) {
        if (!name || !email) {
            e.preventDefault();
            alert('All fields are required.');
            return;
        }

        //nameHidden.value = manualName.value.trim();
        //emailHidden.value = manualEmail.value.trim();
    }
});
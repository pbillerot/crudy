
function crudy_button_action(event) {
    var target = event.target
    var obj = target
    if (target.tagName != "BUTTON") {
        obj = target.parentElement
    }
    // obj.textContent
    var url = obj.dataset.url
    // obj.set_attribute("disabled", "disabled");
    obj.disabled = true;
    var notification = document.querySelector('.mdl-js-snackbar');
    notification.MaterialSnackbar.showSnackbar(
        {
            message: 'Veuillez patienter...'
        }
    );
    window.location = url;
}

window.addEventListener('DOMContentLoaded', function () {
    var elements = document.querySelectorAll('.crudy-button-action');
    Array.from(elements).forEach(link => {
        link.addEventListener('click', crudy_button_action, false);
    });
});



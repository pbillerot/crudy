
function crudy_button_action(event) {
    var target = event.target
    var obj = target
    if (target.tagName != "BUTTON" && target.tagName != "INPUT") {
        obj = target.parentElement
        if (obj.tagName != "BUTTON" && obj.tagName != "INPUT") {
            obj = obj.parentElement
        }
    }
    // obj.textContent
    var url = obj.dataset.url
    // obj.set_attribute("disabled", "disabled");
    obj.disabled = true;
    var notification = document.querySelector('.mdl-js-snackbar');
    notification.MaterialSnackbar.showSnackbar(
        {
            message: 'Veuillez patienter...',
            timeout: 10000
        }
    );
    window.location = url;
}
function crudy_check_action(event) {
    var obj = event.target
    if (obj.checked == true) {
        // recherche du groupe
        var group = obj.dataset.group
        if (group) {
            var elements = document.querySelectorAll('.crudy-check-action');
            for (var item of elements) {
                if (item.dataset.group == group && item.id != obj.id) {
                    if (item.checked == true) {
                        item.click()
                    }
                }
            }
        }
    }
}

window.addEventListener('DOMContentLoaded', function () {
    var elements = document.querySelectorAll('.crudy-button-action');
    Array.from(elements).forEach(link => {
        link.addEventListener('click', crudy_button_action, false);
    });
    elements = document.querySelectorAll('.crudy-check-action');
    Array.from(elements).forEach(link => {
        link.addEventListener('click', crudy_check_action, false);
    });
});



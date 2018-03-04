var dialog = document.querySelector('dialog');
if (dialog) {
    if (!dialog.showModal) {
        dialogPolyfill.registerDialog(dialog);
    }
    dialog.showModal();
}


function crudy_real(id, icarte, add_sub) {
    console.log(id, icarte, add_sub)
}

function crudy_add(event) {
    var obj = event.target
    var dest = document.getElementById(obj.dataset.for)
    var bret = true
    if (obj.dataset.action == '1') {
        if (parseInt(dest.textContent, 10) + 1 == parseInt(obj.dataset.max, 10)) {
            bret = false
        }
    } else {
        if (parseInt(dest.textContent, 10) - 1 == 0) {
            bret = false
        }
    }
    if (bret) {
        fetch(obj.dataset.url)
            .then(response => {
                if (response.status === 200) {
                    console.debug(response);
                    return response.json();
                } else {
                    throw new Error('Something went wrong on api server!');
                }
            })
            .then(response => {
                console.debug(response);
                // Traitement des données de retour
                dest.textContent = response.value
            }).catch(error => {
                console.error(error);
            });
    }
};

window.addEventListener('DOMContentLoaded', function () {
    elements = document.querySelectorAll('.crudy-add');
    Array.from(elements).forEach(link => {
        link.addEventListener('click', crudy_add, false);
    });
});



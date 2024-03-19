document.addEventListener("DOMContentLoaded", function() {
    const targetButton = document.getElementById('add-target');

    targetButton.addEventListener('click', function(event) {
        openPopup();
    });
});

function openPopup() {
    document.getElementById("popup").style.display = "block";
}

function closePopup() {
    document.getElementById("popup").style.display = "none";
}

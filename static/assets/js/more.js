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

document.addEventListener("DOMContentLoaded", function() {
    const tasks = document.querySelectorAll('.task');

    tasks.forEach(task => {
        task.addEventListener('click', function() {
            const pk = task.dataset.pk;
            const url = `/task-details/${pk}`;
            fetch(url)
                .then(response => {
                    if(!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Task details:', data);
                })
                .catch(error => {
                    console.error('Error fetching task details:', error);
                })
        });
    });
});

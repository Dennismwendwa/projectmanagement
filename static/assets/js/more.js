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

function openTaskPopup() {
    document.getElementById("popupTask").style.display = "block";
}


function closeTaskPopup() {
    document.getElementById("popupTask").style.display = "none";
}

document.addEventListener("DOMContentLoaded", function() {
    const tasks = document.querySelectorAll('.task');
    const taskDetailsElement = document.getElementById("taskPopupDetails");

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
                    
                    taskDetailsElement.innerHTML = `
                    <div>
                    <h5>Task: <strong>${data.name}</strong></h5>
                    </div>
                    <div class="d-flex align-items-center">
                    <h4 class="p-3">Completed: </h4>
                    <input class="" type="checkbox" id="complete" name="task-${data.name}" value="">
                    </div>
                    <p><strong>Location:</strong> ${data.location}</p>
                    <p><strong>Department:</strong> ${data.department}</p>
                    <p><strong>Description:</strong> ${data.description}</p>
                    
                `;
                openTaskPopup();
                })
                .catch(error => {
                    console.error('Error fetching task details:', error);
                })
        });
    });
});

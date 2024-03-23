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
                    taskDetailsElement.innerHTML = `
                    <div class="m-2">
                    <div>
                    <small>Task: <strong>${data.name}</strong></small>
                    </div>
                    <div class="d-flex align-items-center">
                    <h4 class="pe-3">Completed: </h4>
                    <input class="ps-3" type="checkbox" id="complete" name="task-${data.name}" value="">
                    </div>
                    <div>
                    <p><strong>Location:</strong> ${data.location}</p>
                    </div>
                    <div>
                    <p><strong>Department:</strong> ${data.department}</p>
                    </div>
                    <div>
                    <p><strong>Description:</strong> ${data.description}</p>
                    </div>
                    </div>
                    
                `;
                openTaskPopup();
                const completedTask = document.getElementById("complete");
                if (completedTask) {
                    completedTask.addEventListener("click", function() {
                        const taskUrl = `/completed-task/${pk}`;
                        fetch(taskUrl)
                        .then(response => {
                            if(response.ok){
                                console.log("Task updated");
                            }
                        })
                    })
                }
                })
                

                .catch(error => {
                    console.error('Error fetching task details:', error);
                })
        });
    });
});

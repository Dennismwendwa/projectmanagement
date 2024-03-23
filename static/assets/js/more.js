document.addEventListener("DOMContentLoaded", function() {
    const targetButton = document.getElementById('add-target');

    targetButton.addEventListener('click', function(event) {
        event.stopPropagation();
        openPopup();
    });
    
    document.addEventListener('click', function(event) {
        const popup = document.getElementById("popup");
        const isClickInsidePopup = popup.contains(event.target);
        if (!isClickInsidePopup) {
            closePopup();
        }
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
                    console.log(data);
                    const deadlineDate = new Date(data.deadline);
                    const dateNow = new Date();
                    const formattedDeadline = `${deadlineDate.toLocaleDateString('en-US', { month: 'long', day: 'numeric' })}, ${deadlineDate.getFullYear()}`;
                    taskDetailsElement.innerHTML = `
                    <div class="row">
                        <div class="col-md-10">
                            <div class="m-1 p-1">
                                <div class="m-3">
                                    <h4>Task: <strong>${data.name}</strong></h4>
                                </div>
                                <div class="m-3">
                                    <p class="${data.checklist ? 'bg-success' : (new Date(data.deadline) < dateNow && !data.checklist ? 'bg-danger' : 'bg-white')}">Due date: ${formattedDeadline}</p>
                                </div>
                                <div class="d-flex align-items-center mt-2">
                                    <p class="pe-3">Completed: </p>
                                    ${data.checklist ? '<input <input id="complete" class="ps-3 pb-2" type="checkbox" checked>' : '<input id="complete" class="ps-3" type="checkbox">'}
                                </div>
                                <div class="d-flex my-3">
                                    <div class="me-2">
                                        <p><strong>Location:</strong> ${data.location}</p>
                                    </div>
                                    <div class="ms-2">
                                        <p><strong>Department:</strong> ${data.department}</p>
                                    </div>
                                </div>
                                <div class="my-3">
                                    <p><strong>Description:</strong> ${data.description}</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-2 mt-4">
                            <div class="m-1 border">
                                <p class="p-2">label</p>
                            </div>
                        </div>
                    </div>
                    
                `;
                openTaskPopup();
                const completedTask = document.getElementById("complete");
                if (completedTask) {
                    completedTask.addEventListener("click", function(event) {
                    
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

document.addEventListener("DOMContentLoaded", function() {

    const completedTasksCount = JSON.parse(document.getElementById('completed_tasks_count').textContent);
    const uncompletedTasksCount = JSON.parse(document.getElementById('uncompleted_tasks_count').textContent);
    const data = {
        labels: ['Completed', 'Uncompleted'],
        datasets: [{
            data: [completedTasksCount, uncompletedTasksCount],
            backgroundColor: ['green', 'orange']
        }]
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
            labels: {
                fontColor: 'blue'
            }
        }
    };

    const ctx = document.getElementById('pieChart').getContext('2d');

    const pieChart = new Chart(ctx, {
        type: 'pie',
        data: data,
        options: options
    });
});

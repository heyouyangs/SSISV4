
document.addEventListener('DOMContentLoaded', function () {
    var getStarted = document.getElementById('getStarted');
    var modal = document.getElementById('myModal');
    var span = document.getElementsByClassName('close')[0];

    function showModal() {
        modal.style.display = 'block';
    }

    function closeModal() {
        modal.style.display = 'none';
    }

    getStarted.onclick = showModal;
    span.onclick = closeModal;

    window.onclick = function (event) {
        if (event.target === modal) {
            closeModal();
        }
    }
})




document.addEventListener('DOMContentLoaded', function () {
    var getStarted = document.getElementById('AddStudentModal');
    var modal = document.getElementById('AddStudentModal');
    var span = document.getElementsByClassName('close')[0];

    function showModal() {
        modal.style.display = 'block';
    }

    function closeModal() {
        modal.style.display = 'none';
    }

    getStarted.onclick = showModal;
    span.onclick = closeModal;

    window.onclick = function (event) {
        if (event.target === modal) {
            closeModal();
        }
    }
})
fetch(`/colleges/delete/${college_code}`, {
    method: 'DELETE',
    headers: {
        'X-CSRFToken': csrfToken
    }
})

function deleteCollege(button) {
    console.log("Delete button clicked.");
    var college_code = button.getAttribute('college-code');
    var csrfToken = button.getAttribute('csrf-token');
    if (confirm("Are you sure you want to delete this college?\nStudents and Courses under this College will also be deleted.")) {
        fetch(`/colleges/delete/${college_code}`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken
            }
        }).then(response => response.json())
        .then(data => {
            if (data.success === true) {
                window.location.reload();
            } else {
                console.error("Error: " + data.error);
            }
        });
    }
}
fetch(`/students/delete/${student_id}`, {
    method: 'DELETE',
    headers: {
        'X-CSRFToken': csrfToken
    }
})

function deleteStudent(button) {
    console.log("Delete button clicked.");
    var student_id = button.getAttribute('student-id');
    var csrfToken = button.getAttribute('csrf-token');
    if (confirm("Are you sure you want to delete this student?")) {
        fetch(`/students/delete/${student_id}`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken
            }
        }).then(response => response.json())
        .then(data => {
            if (data.success === true) {
                window.location.reload();
            } else {
                console.error("Error: " + data.error);
            }
        });
    }
}
fetch(`/courses/delete/${course_code}`, {
    method: 'DELETE',
    headers: {
        'X-CSRFToken': csrfToken
    }
})

function deleteCourses(button) {
    console.log("Delete button clicked.");
    
    // Retrieve course code and CSRF token from data attributes
    var course_code = button.getAttribute('coursecode'); // Change 'data-course-code' to 'coursecode'
    var csrfToken = button.getAttribute('csrf-token');     // Change 'data-csrf-token' to 'csrf-token'
    
    if (confirm("Are you sure you want to delete this course?\nThis action cannot be undone.")) {
        fetch(`/courses/delete/${course_code}`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success === true) {
                window.location.reload();
            } else {
                console.error("Error: " + data.error);
            }
        });
    }
}
const toggleButton = document.querySelector('.nav-button');
const sidebar = document.getElementById("nav");

toggleButton.addEventListener('click', function() {
    sidebar.classList.toggle('nav-closed');
});
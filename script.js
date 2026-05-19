function toggleNav() {
    const drawer = document.getElementById('nav-drawer');
    drawer.classList.toggle('open');
}

// Close drawer if clicking outside of it
document.addEventListener('click', function(event) {
    const drawer = document.getElementById('nav-drawer');
    const menuBtn = document.querySelector('.menu-btn');
    if (!drawer.contains(event.target) && event.target !== menuBtn && drawer.classList.contains('open')) {
        drawer.classList.remove('open');
    }
});
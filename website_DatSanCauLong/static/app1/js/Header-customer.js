function toggleDropdown() {
    const dropdown = document.getElementById('dropdownMenu');
    dropdown.classList.toggle('active');
}

// Close dropdown when clicking outside
document.addEventListener('click', function (event) {
    const dropdown = document.getElementById('dropdownMenu');
    const userInfo = document.querySelector('.user-info');
    if (!userInfo.contains(event.target) && !dropdown.contains(event.target)) {
        dropdown.classList.remove('active');
    }
});
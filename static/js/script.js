document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const form = document.getElementById('userForm');
    
    form.addEventListener('submit', function(event) {
        const name = document.getElementById('name').value.trim();
        const age = document.getElementById('age').value;
        const formClass = document.getElementById('form').value.trim();
        
        if (!name || !age || !formClass) {
            event.preventDefault();
            alert('Please fill in all fields');
            return;
        }
        
        if (age < 1 || age > 120) {
            event.preventDefault();
            alert('Please enter a valid age between 1 and 120');
            return;
        }
    });

});

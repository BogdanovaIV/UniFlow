document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('selection-shedule-templates');

    // Function to check if all required fields are filled
    function areAllFieldsFilled() {
        const requiredFields = form.querySelectorAll(
            'input[required], select[required]'
        );
        return Array.from(requiredFields).every(
            field => field.value.trim() !== ''
        );
    }

    // Function to update the selection description
    function updateSelectionDescription() {
        const termSelect = form.querySelector('select[name="term"]'); 
        const groupSelect = form.querySelector('select[name="study_group"]'); 
        
        const selectedTermText = termSelect.options[termSelect.selectedIndex].text; 
        const selectedGroupText = groupSelect.options[groupSelect.selectedIndex].text;
        // Update description based on selections
        if (selectedTermText && selectedGroupText) {
            selectionDescription.textContent = `Term: ${selectedTermText}; Study Group: ${selectedGroupText}.`;
        } else {
            selectionDescription.textContent = ''; // Clear if selections are not complete
        }
    }

    // Attach change event to all input and select elements in the form
    const inputElements = form.querySelectorAll('input, select');
    inputElements.forEach(input => {
        input.addEventListener('change', function () {
            updateSelectionDescription();
            if (areAllFieldsFilled()) {
                // Submit the form when all required fields are filled
                form.submit();
            }
        });
    });

    updateSelectionDescription();
});
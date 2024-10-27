/* jshint esversion: 11, sub:true */

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('selection-shedule-templates');
    const sheduleTemplates = document.getElementById('schedule-templates');
    // Attach change event to all input and select elements in the form
    const inputElements = form.querySelectorAll('input, select');
    inputElements.forEach(input => {
        input.addEventListener('change', function () {
            updateSelectionDescription(form, selectionDescription);

            if (areAllFieldsFilled(form) ||
                sheduleTemplates.getAttribute('data-empty') == "False") {
                form.submit();
            }
        }  );
    });

    updateSelectionDescription(form, selectionDescription)
});

// Function to check if all required fields are filled
function areAllFieldsFilled(form) {
    const requiredFields = form.querySelectorAll(
        'input[required], select[required]'
    );
    return Array.from(requiredFields).every(
        field => field.value.trim() !== ''
    );
}

// Function to update the selection description
function updateSelectionDescription(form, selectionDescription) {
    const termSelect = form.querySelector('select[name="term"]'); 
    const groupSelect = form.querySelector('select[name="study_group"]'); 
    
    const selectedTermText = termSelect.options[termSelect.selectedIndex].text; 
    const selectedGroupText = groupSelect.options[groupSelect.selectedIndex].text;

    // Update description based on selections
    if (selectedTermText || selectedGroupText) {
        selectionDescription.textContent = `Term: ${selectedTermText}; Study Group: ${selectedGroupText};`;
    } else {
        selectionDescription.textContent = ''; // Clear if selections are not complete
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { areAllFieldsFilled, updateSelectionDescription };
}
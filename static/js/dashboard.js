/* jshint esversion: 11, sub:true */

document.addEventListener('DOMContentLoaded', function () {

    //Add event for toast messages
    var toastElements = document.querySelectorAll('.toast');
    toastElements.forEach(function (toastElement) {
        var toast = new bootstrap.Toast(toastElement);
        toast.show();
    });

    const form = document.getElementById('selection-schedule');
    const schedule = document.getElementById('schedule');
    if (form) {
        const dataTemplateName = schedule.getAttribute('data-template-name');
        const fillForm = document.getElementById('fill-form');
        // Attach change event to all input and select elements in the form
        const upadateSelection = function () {
            updateSelectionDescription(form, selectionDescription, dataTemplateName);
            if (fillForm) {
                console.log(schedule.getAttribute('data-empty'));
                if (schedule.getAttribute('data-empty') == "False") {
                    if (!fillForm.hasAttribute('hidden')) {
                        fillForm.setAttribute('hidden', '');
                    }
                } else if (areAllFieldsFilled(form)) {
                    if (fillForm.hasAttribute('hidden')) {
                        fillForm.removeAttribute('hidden');
                    }
                } else {
                    if (!fillForm.hasAttribute('hidden')) {
                        fillForm.setAttribute('hidden', '');
                    }
                }
            }
            if (areAllFieldsFilled(form)) {
                form.submit();
            }
        };

        const submitSelection = document.getElementById('submit-selection');
        if (submitSelection) {
            submitSelection.addEventListener('click', upadateSelection);
        }

        const updateSelection = document.getElementById('update-selection');
        if (updateSelection) {
            updateSelection.addEventListener('click', upadateSelection);
        }

        updateSelectionDescription(form, selectionDescription, dataTemplateName);
    }

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
function updateSelectionDescription(form, selectionDescription, dataTemplateName) {
    let selectedFirstText;
    let labelFirstSelect = 'Term';
    if (dataTemplateName == 'schedule' || dataTemplateName == 'student-schedule') {
        const firstSelect = form.querySelector("[name='date']");
        selectedFirstText = firstSelect.value;
        labelFirstSelect = 'Date';
    } else {
        const firstSelect = form.querySelector("select[name='term']");
        selectedFirstText = firstSelect.options[firstSelect.selectedIndex].text;
    }

    const groupSelect = form.querySelector('select[name="study_group"]');
    const selectedGroupText = groupSelect.options[groupSelect.selectedIndex].text;

    // Update description based on selections
    if (selectedFirstText || selectedGroupText) {
        selectionDescription.textContent = `${labelFirstSelect}: ${selectedFirstText}; Study Group: ${selectedGroupText};`;
    } else {
        selectionDescription.textContent = ''; // Clear if selections are not complete
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { areAllFieldsFilled, updateSelectionDescription };
}
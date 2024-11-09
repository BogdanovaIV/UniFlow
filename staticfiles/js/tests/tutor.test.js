/**
 * @jest-environment jsdom
 */

const { areAllFieldsFilled, updateSelectionDescription } = require("../tutor");

const htmlSheduleTemplates = `
    <form id="selection-shedule-templates">
        <select name="term" required>
            <option value=""></option>
            <option value="1">Term 1</option>
            <option value="2">Term 2</option>
        </select>
        <select name="study_group" required>
            <option value=""></option>
            <option value="1">Group A</option>
            <option value="2">Group B</option>
        </select>
        <div id="selection-description"></div>
    </form>
    <div id="schedule" data-template-name="schedule-template">
`;

const htmlShedule = `
    <form id="selection-shedule-templates">
        <input type="date" name="date" required">
        <select name="study_group" required>
            <option value=""></option>
            <option value="1">Group A</option>
            <option value="2">Group B</option>
        </select>
        <div id="selection-description"></div>
    </form>
    <div id="schedule" data-template-name="schedule">
`;

describe('Schedule Template Selection Form', () => {
    let form, selectionDescription;

    beforeEach(() => {
        document.body.innerHTML = htmlSheduleTemplates;

        // Access form and description elements
        form = document.getElementById('selection-shedule-templates');
        selectionDescription = document.getElementById('selection-description');
    });

    // Test case for description update
    test('should update selection description when fields change', () => {
        const termSelect = form.querySelector('select[name="term"]');
        const groupSelect = form.querySelector('select[name="study_group"]');
        termSelect.value = '1';
        groupSelect.value = "";

        expect(areAllFieldsFilled(form)).toBe(false);
        updateSelectionDescription(form, selectionDescription);
        expect(
            selectionDescription.textContent
        ).toBe('Term: Term 1; Study Group: ;');

        groupSelect.value = "1";
        expect(areAllFieldsFilled(form)).toBe(true);
        updateSelectionDescription(form, selectionDescription);
        expect(
            selectionDescription.textContent
        ).toBe('Term: Term 1; Study Group: Group A;');
    });

    // Test case to check if all required fields are filled
    test('should return true when all required fields are filled', () => {
        const termSelect = form.querySelector('select[name="term"]');
        const groupSelect = form.querySelector('select[name="study_group"]');
        
        // Select both term and study group
        termSelect.value = '1';
        groupSelect.value = '1';
        
        expect(areAllFieldsFilled(form)).toBe(true);
    });

    // Test case to check if form is incomplete if any field is empty
    test('should return false when required fields are not filled', () => {
        const termSelect = form.querySelector('select[name="term"]');
        const groupSelect = form.querySelector('select[name="study_group"]');
        
        // Leave term and group empty
        termSelect.value = '';
        groupSelect.value = '';
        
        expect(areAllFieldsFilled(form)).toBe(false);
    });
});


describe('Schedule Selection Form', () => {
    let form, selectionDescription;

    beforeEach(() => {
        document.body.innerHTML = htmlShedule;

        // Access form and description elements
        form = document.getElementById('selection-shedule-templates');
        selectionDescription = document.getElementById('selection-description');
        const schedule = document.getElementById('schedule');
        dataTemplateName = schedule.getAttribute('data-template-name')
    });

    // Test case for description update
    test('should update selection description when fields change', () => {
        const dateSelect = form.querySelector("[name='date']");
        const groupSelect = form.querySelector('select[name="study_group"]');
        dateSelect.value = '2024-10-30';
        groupSelect.value = '';

        expect(areAllFieldsFilled(form)).toBe(false);
        updateSelectionDescription(form, selectionDescription, dataTemplateName);
        expect(
            selectionDescription.textContent
        ).toBe('Date: 2024-10-30; Study Group: ;');

        groupSelect.value = '1';
        expect(areAllFieldsFilled(form)).toBe(true);
        updateSelectionDescription(form, selectionDescription, dataTemplateName);
        expect(
            selectionDescription.textContent
        ).toBe('Date: 2024-10-30; Study Group: Group A;');
    });

    // Test case to check if all required fields are filled
    test('should return true when all required fields are filled', () => {
        const dateSelect = form.querySelector("[name='date']");
        const groupSelect = form.querySelector('select[name="study_group"]');
        
        // Select both date and study group
        dateSelect.value = '2024-10-30';
        groupSelect.value = '1';
        
        expect(areAllFieldsFilled(form)).toBe(true);
    });

    // Test case to check if form is incomplete if any field is empty
    test('should return false when required fields are not filled', () => {
        const dateSelect = form.querySelector("[name='date']");
        const groupSelect = form.querySelector('select[name="study_group"]');
        
        // Leave term and group empty
        dateSelect.value = '';
        groupSelect.value = '';
        
        expect(areAllFieldsFilled(form)).toBe(false);
    });
});
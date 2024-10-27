/**
 * @jest-environment jsdom
 */

const { areAllFieldsFilled, updateSelectionDescription } = require("../tutor");

const html = `
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
`;

describe('Schedule Template Selection Form', () => {
    let form, selectionDescription;

    beforeEach(() => {
        document.body.innerHTML = html;

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
});
document.addEventListener('DOMContentLoaded', function () {
    function handleFiles(inputField, files, label) {
        inputField.files = files;
        label.textContent = Array.from(files).map(file => file.name).join(', ');
    }

    function setupDragAndDrop(areaId, inputId) {
        const area = document.getElementById(areaId);
        const input = document.getElementById(inputId);
        const label = area.querySelector('label');

        area.addEventListener('dragover', function (e) {
            e.preventDefault();
            area.classList.add('active');
        }, false);

        area.addEventListener('dragleave', function (e) {
            e.preventDefault();
            area.classList.remove('active');
        }, false);

        area.addEventListener('drop', function (e) {
            e.preventDefault();
            area.classList.remove('active');
            handleFiles(input, e.dataTransfer.files, label);
        }, false);

        input.addEventListener('change', function () {
            handleFiles(input, input.files, label);
        }, false);
    }

    setupDragAndDrop('aesKeyUpload', 'aes_key_file');
    setupDragAndDrop('encryptedDataUpload', 'encrypted_data_file');
    setupDragAndDrop('contextUpload', 'context_file');
});

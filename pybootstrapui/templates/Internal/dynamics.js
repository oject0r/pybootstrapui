host = '!PYBSUI.INSERTHOST';

// Utility functions
function fetchJSON(url, options = {}) {
    return fetch(url, options)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }
            return response.json();
        });
}

function sendJSON(url, data) {
    return fetchJSON(url, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data),
    });
}

// Task Handling
const API = {
    tasksGet: host + "/get_tasks",
    tasksPost: host + "/task_result",
};

function fetchAndCompleteTasks() {
    fetchJSON(API.tasksGet)
        .then(tasks => {
            Object.entries(tasks).forEach(([taskId, task]) => {
                const result = handleTask(task);
                sendTaskResult(taskId, result);
            });
        })
        .catch(error => console.error("Error fetching tasks:", error));
}

/**
 * Handle various tasks dynamically based on the task type.
 * @param {Object} task - The task object containing type and related parameters.
 * @returns {string} - The result of the task or 'Task completed' if no value is returned.
 */
function handleTask(task) {
    const handlers = {
        getValue: () => getValueFromInput(task.id),
        setValue: () => setValueToInput(task.id, task.value),
        executeJavascript: () => executeJavascriptCode(task.code),
        rewriteContent: () => rewriteContent(task.id, task.newContent, task.transitionTime),
        focusOn: () => focusOn(task.id),
        getCaret: () => getCaret(task.id),
        setCaret: () => moveCursorTo(task.id, task.newPosition),
        addNew: () => addInto(task.id, task.content),
        addTooltip: () => addTooltip(task.id, task.content, task.placement),
        deleteElement: () => deleteById(task.id),
        updateProgressBar: () => updateProgressBar(task.id, task.newValue, task.newText),
        getSelectedFiles: () => getSelectedFiles(task.id),
        showFullscreenSpinner: () => showFullscreenSpinner(),
        hideFullscreenSpinner: () => hideFullscreenSpinner(),
        showModal: () => showModal(task.content),
        hideModal: () => hideModal(),
        showButtonSpinner: () => showButtonSpinner(task.id),
        hideButtonSpinner: () => hideButtonSpinner(task.id),
        customTask: () => performCustomTask(task.id),
    };

    const handler = handlers[task.type];
    if (handler) {
        const result = handler();
        return result !== undefined ? result : 'Task completed';
    } else {
        return `Unknown task type: ${task.type}`;
    }
}


/**
 * Add a spinner to a button and disable it.
 * The original button text is retained, and the spinner is added to the left.
 * @param {string} buttonId - The ID of the button.
 */
function showButtonSpinner(buttonId) {
    // Get the button element by its ID
    const button = document.getElementById(buttonId);
    if (!button) return;

    // Check if spinner already exists to prevent duplicates
    if (button.querySelector('.spinner-border')) return;

    // Create spinner element
    const spinner = document.createElement('span');
    spinner.classList.add('spinner-border', 'spinner-border-sm', 'me-2');
    spinner.setAttribute('role', 'status');
    spinner.setAttribute('aria-hidden', 'true');
    spinner.style.verticalAlign = 'middle';

    // Add spinner to the button
    button.insertBefore(spinner, button.firstChild);

    // Disable the button
    button.disabled = true;
}

/**
 * Remove the spinner from a button and enable it.
 * @param {string} buttonId - The ID of the button.
 */
function hideButtonSpinner(buttonId) {
    // Get the button element by its ID
    const button = document.getElementById(buttonId);
    if (!button) return;

    // Remove the spinner if it exists
    const spinner = button.querySelector('.spinner-border');
    if (spinner) {
        spinner.remove();
    }

    // Enable the button
    button.disabled = false;
}


/**
 * Show a modal window
 * @param {string} modalHTML - HTML content of the modal
 */
function showModal(modalHTML) {
    // Check if the modal already exists in the DOM
    if (document.getElementById('customModal')) {
        document.getElementById('customModal').remove();
    }

    // Append the modal to the body
    document.body.insertAdjacentHTML('beforeend', modalHTML);

    // Initialize and display the Bootstrap modal
    const modalElement = document.getElementById('customModal');
    const modalInstance = new bootstrap.Modal(modalElement);
    modalInstance.show();

}

/**
 * Hide and remove the modal window from the DOM
 */
function hideModal() {
    // Get the modal element from the DOM
    const modalElement = document.getElementById('customModal');
    if (!modalElement) {
        return;
    }

    // Hide the modal using Bootstrap's API
    const modalInstance = bootstrap.Modal.getInstance(modalElement);
    if (modalInstance) {
        modalInstance.hide();
    }

    // Remove the modal element from the DOM after hiding
    setTimeout(() => {
        modalElement.remove();
    }, 200);
}


function sendTaskResult(taskId, result) {
    sendJSON(API.tasksPost, {task_id: taskId, result})
        .then(() => console.log(`Task ${taskId} completed and result sent.`))
        .catch(error => console.error(`Error sending result for task ${taskId}:`, error));
}

// Input and Content Manipulation
function getValueFromInput(inputId) {
    const element = document.getElementById(inputId);
    return element?.value ?? null;
}

function setValueToInput(inputId, value) {
    const element = document.getElementById(inputId);
    if (element) {
        element.value = value;
    }
    return value;
}


function showFullscreenSpinner() {
    // Создаем div для спиннера
    const spinner = document.createElement('div');
    spinner.id = 'fullscreen-spinner';
    spinner.className = 'position-fixed top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center bg-dark bg-opacity-75';
    spinner.style.zIndex = '1050';

    // Добавляем внутренний HTML со спиннером
    spinner.innerHTML = `
        <div class="spinner-border text-light" role="status" style="width: 4rem; height: 4rem;">
            <span class="visually-hidden">Loading...</span>
        </div>
    `;

    // Добавляем спиннер в body
    document.body.appendChild(spinner);
    return 'j';
}

function hideFullscreenSpinner() {
    const spinner = document.getElementById('fullscreen-spinner');
    if (spinner) {
        spinner.remove();
    }
    return 'i';
}


function rewriteContent(containerId, newContent, transitionTime = 0) {
    const container = document.getElementById(containerId);

    if (container) {
        // Set transition for smooth disappearance
        container.style.transition = `opacity ${transitionTime}ms ease-in-out`;
        container.style.opacity = "0";

        // After hiding is complete, check the type of change
        setTimeout(() => {
            if (typeof newContent === "string") {
                // If HTML content is passed, update the content
                container.innerHTML = newContent;
            } else if (typeof newContent === "object") {
                // If an object with changes is passed, apply the styles
                if (newContent.style) {
                    Object.assign(container.style, newContent.style);
                }
                if (newContent.text) {
                    container.textContent = newContent.text;
                }
            }

            // Smooth appearance
            container.style.opacity = "1";
        }, transitionTime);

        return "Content updated successfully!";
    }

    return `Error: Container '${containerId}' not found.`;
}

function updateProgressBar(elementId, newValue, newText) {
    const progressBar = document.getElementById(elementId);
    const hostPB = document.getElementById(elementId + 'HOST');

    if (progressBar) {
        // Clamp the value in the range 0-100
        const clampedValue = Math.max(0, Math.min(100, newValue));

        // Adjust the progress bar width
        progressBar.style.width = `${clampedValue}%`;

        // Update the value inside the progress bar
        progressBar.textContent = newText;
        hostPB.setAttribute("aria-valuenow", clampedValue);
    } else {
        console.error(`Progress bar with ID "${elementId}" not found.`);
    }
    return 'h';
}

// Focus and Caret Handling
function focusOn(elementId) {
    const elem = document.getElementById(elementId);
    if (elem) {
        elem.focus();
        return "Focused on!";
    }
    return "No such element!";
}

function getCaret(elementId) {
    const e = document.getElementById(elementId);
    return e ? getCursorPosition(e) : "No such element!";
}

function getCursorPosition(element) {
    return element.value.slice(0, element.selectionStart).length;
}

function moveCursorTo(elementId, caretPos) {
    const input = document.getElementById(elementId);
    if (input) {
        input.focus();
        input.setSelectionRange(caretPos, caretPos);
        return "Cursor moved!";
    }
    return "No such element!";
}

// JavaScript Execution
function executeJavascriptCode(code) {
    try {
        return eval(code) || "Code executed successfully!";
    } catch (error) {
        console.error(`Error executing JS code: ${code}`, error);
        return `Error: ${error.message}`;
    }
}

// Custom Tasks
function performCustomTask(taskId) {
    console.log(`Performing custom task for: ${taskId}`);
    return `Task ${taskId} completed.`;
}

// Event Handling
function sendEvent(eventContext, eventType) {
    sendJSON(host + "/action", {
        event: eventType,
        data: {id: eventContext},
    });
}

function sendEventCustom(eventContext, eventType, customData) {
    sendJSON(host + "/action", {
        event: eventType,
        data: customData,
    });
}

function sendAction(eventContext, eventType) {
    sendJSON(host + '/action', {
        event: eventType,
        data: {id: eventContext}
    });
}

function sendButtonClick(buttonId, spinnerIndicator = true, customData = '') {
    sendEventCustom(buttonId, "button_click", {
        id: buttonId,
        indicateSpinner: spinnerIndicator,
        data: customData
    });
}

function sendInputOnInput(id, value, eventTypeCustom = 'on_input') {
    sendEventCustom(id, eventTypeCustom, {
        id: id,
        value: value,
        caret_position: getCaret(id)
    });
}

function sendOnChoice(id) {
    const element = document.getElementById(id);
    sendEventCustom(id, 'on_choice', {
        id: id,
        value: element.value
    });
}

function getValueId(id) {
    const element = document.getElementById(id);
    return element ? element.value : null;
}

function addInto(id, content) {
    const element = document.getElementById(id);
    if (element) {
        // Create a temporary container for new content
        const tempDiv = document.createElement('div');
        // Insert new content
        tempDiv.innerHTML = content.trim();
        const newElement = tempDiv.firstElementChild;

        // Add 'hidden' class for the initial state
        newElement.classList.add('hidden');
        element.appendChild(newElement);

        // Switch to visible after a short delay
        setTimeout(() => {
            newElement.classList.add('visible');
            newElement.classList.remove('hidden');
        }, 10);

        return 'Content added successfully!';
    } else {
        return 'Element not found!';
    }
}

function deleteById(id) {
    const element = document.getElementById(id);
    if (element) {
        element.remove();
        return 'Element was deleted.';
    } else {
        return 'Element not found!';
    }
}

function addTooltip(targetId, content, placement = "top") {
    const targetElement = document.getElementById(targetId);

    if (!targetElement) {
        console.error(`Tooltip target with ID "${targetId}" not found.`);
        return;
    }

    // Check if the tooltip already exists, remove the old one
    if (targetElement._tooltipInstance) {
        targetElement._tooltipInstance.dispose();
    }

    // Initialize the tooltip using Bootstrap
    const tooltip = new bootstrap.Tooltip(targetElement, {
        title: content,
        placement: placement,
    });

    // Save the tooltip instance for removal if needed
    targetElement._tooltipInstance = tooltip;
}

function getSelectedFiles(inputId) {
    const inputElement = document.getElementById(inputId);

    if (!inputElement) {
        console.error(`File input with ID "${inputId}" not found.`);
        return [];
    }

    const files = Array.from(inputElement.files || []);
    return files.map(file => ({
        name: file.name,
        size: file.size,
        type: file.type,
        path: file.path,
    }));
}

function handleFiles(files, inputId) {
    const inputElement = document.getElementById(inputId);
    const uploadedFiles = document.getElementById(`${inputId}-uploaded-files`);

    Array.from(files).forEach((file, index) => {
        const fileSize = (file.size / 1024 / 1024).toFixed(2) + ' MB';

        const listItem = document.createElement('li');
        listItem.innerHTML = `
            <span class="file-name"><i class="bi bi-file-earmark"></i> ${file.name}</span>
            <span class="file-size">${fileSize}</span>
            <span class="delete-button" onclick="deleteFile('${inputId}', ${index}, this.parentElement)">
                <i class="bi bi-trash"></i>
            </span>
        `;
        uploadedFiles.appendChild(listItem);
    });
}

// Function for deleting a file
function deleteFile(inputId, index, listItem) {
    const inputElement = document.getElementById(inputId);

    if (!inputElement || !inputElement.files) {
        console.error('File input not found or unsupported.');
        return;
    }

    const dataTransfer = new DataTransfer();
    const files = Array.from(inputElement.files);

    // Add all files except the one being deleted
    files.forEach((file, i) => {
        if (i !== index) {
            dataTransfer.items.add(file);
        }
    });

    // Assign the updated file list back to the input
    inputElement.files = dataTransfer.files;

    // Remove the item from the DOM
    listItem.remove();
}

// Polling for tasks
setInterval(fetchAndCompleteTasks, !PYBSUI.TASKTIMINGS);

const textareas = document.querySelectorAll('textarea.auto-resize');

textareas.forEach(textarea => {
    textarea.addEventListener('input', function () {
        this.style.height = 'auto';  // Сбрасываем высоту
        this.style.height = (this.scrollHeight - 20) + 'px';  // Устанавливаем высоту по содержимому
    });
});


autosize(document.querySelectorAll('textarea.auto-resize'));
host = '!PYBSUI.INSERTHOST'

// Utility functions
function fetchJSON(url, options = {}) {
    return fetch(url, options)
        .then(response => {
            if (!response.ok) throw new Error(`Server error: ${response.status}`);
            return response.json();
        });
}

function sendJSON(url, data) {
    return fetchJSON(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
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

function handleTask(task) {
    const handlers = {
        getValue: () => getValueFromInput(task.id),
        setValue: () => setValueToInput(task.id, task.value),
        executeJavascript: () => executeJavascriptCode(task.code),
        rewriteContent: () => rewriteContent(task.id, task.newContent),
        focusOn: () => focusOn(task.id),
        getCaret: () => getCaret(task.id),
        setCaret: () => moveCursorTo(task.id, task.newPosition),
        addNew: () => addInto(task.id, task.content),
        deleteElement: () => deleteById(task.id),
        customTask: () => performCustomTask(task.id),

    };

    const handler = handlers[task.type];
    return handler ? handler() : `Unknown task type: ${task.type}`;
}

function sendTaskResult(taskId, result) {
    sendJSON(API.tasksPost, { task_id: taskId, result })
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
    if (element) element.value = value;
    return value;
}

function rewriteContent(containerId, newContent) {
    console.log('Got rewrite content!')
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = newContent;
        return "Content updated successfully!";
    }
    return `Error: Container '${containerId}' not found.`;
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
        data: { id: eventContext },
    });
}

function sendEventCustom(eventContext, eventType, customData) {
    sendJSON(host + "/action", {
        event: eventType,
        data: customData,
    });
}

function sendButtonClick(buttonId) {
    sendEvent(buttonId, "button_click");
}

function sendInputOnInput(id, value) {
    sendEventCustom(id, 'on_input', {
        id: id,
        value: value,
        caret_position: getCaret(id)
    })
}

function sendOnChoice(id) {
    const element = document.getElementById(id)
    sendEventCustom(id, 'on_choice', {
        id: id,
        value: element.value
    })
}

function getValueId(id) {
    const element = document.getElementById(id);
    return element ? element.value : null;
}

function addInto(id, content) {
    const element = document.getElementById(id);
    if (element) {
        element.insertAdjacentHTML('beforeend', content);
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


// Polling for tasks
setInterval(fetchAndCompleteTasks, 45);

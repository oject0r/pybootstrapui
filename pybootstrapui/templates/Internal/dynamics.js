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
        rewriteContent: () => rewriteContent(task.id, task.newContent, task.transitionTime),
        focusOn: () => focusOn(task.id),
        getCaret: () => getCaret(task.id),
        setCaret: () => moveCursorTo(task.id, task.newPosition),
        addNew: () => addInto(task.id, task.content),
        deleteElement: () => deleteById(task.id),
        updateProgressBar: () => updateProgressBar(task.id, task.newValue, task.newText),
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

function rewriteContent(containerId, newContent, transitionTime = 0) {
    const container = document.getElementById(containerId);

    if (container) {
        // Устанавливаем переход для плавного исчезновения
        container.style.transition = `opacity ${transitionTime}ms ease-in-out`;
        container.style.opacity = "0"; // Плавно скрываем элемент

        // После завершения скрытия проверяем тип изменения
        setTimeout(() => {
            if (typeof newContent === "string") {
                // Если передан HTML-контент, обновляем содержимое
                container.innerHTML = newContent;
            } else if (typeof newContent === "object") {
                // Если передан объект изменений, применяем стили
                if (newContent.style) {
                    Object.assign(container.style, newContent.style);
                }
                if (newContent.text) {
                    container.textContent = newContent.text;
                }
            }

            // Плавное появление
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
        // Ограничиваем значение в диапазоне 0-100
        const clampedValue = Math.max(0, Math.min(100, newValue));

        // Изменяем ширину прогресс-бара
        progressBar.style.width = `${clampedValue}%`;

        // Обновляем значение внутри прогресс-бара
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
        data: { id: eventContext },
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
        data: {
            id: eventContext
        }
    })
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
        // Создаём временный контейнер для нового контента
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = content.trim(); // Вставляем новый контент
        const newElement = tempDiv.firstElementChild;

        // Добавляем класс hidden для начального состояния
        newElement.classList.add('hidden');
        element.appendChild(newElement);

        // Переключаем на видимый через короткую задержку
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


// Polling for tasks
setInterval(fetchAndCompleteTasks, 45);

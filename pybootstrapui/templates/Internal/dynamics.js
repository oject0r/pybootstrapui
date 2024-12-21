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
        addTooltip: () => addTooltip(task.id, task.content, task.placement),
        deleteElement: () => deleteById(task.id),
        updateProgressBar: () => updateProgressBar(task.id, task.newValue, task.newText),
        getSelectedFiles: () => getSelectedFiles(task.id),
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

function addTooltip(targetId, content, placement = "top") {
    const targetElement = document.getElementById(targetId);

    if (!targetElement) {
        console.error(`Tooltip target with ID "${targetId}" not found.`);
        return;
    }

    // Проверяем, если тултип уже существует, удаляем старый
    if (targetElement._tooltipInstance) {
        targetElement._tooltipInstance.dispose();
    }

    // Инициализация тултипа с помощью Bootstrap
    const tooltip = new bootstrap.Tooltip(targetElement, {
        title: content,
        placement: placement,
    });

    // Сохраняем экземпляр тултипа для удаления при необходимости
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

// Функция для удаления файла
function deleteFile(inputId, index, listItem) {
    const inputElement = document.getElementById(inputId);

    if (!inputElement || !inputElement.files) {
        console.error('File input not found or unsupported.');
        return;
    }

    const dataTransfer = new DataTransfer();
    const files = Array.from(inputElement.files);

    // Добавляем все файлы, кроме удаляемого
    files.forEach((file, i) => {
        if (i !== index) {
            dataTransfer.items.add(file);
        }
    });

    // Присваиваем обновлённый список файлов обратно в input
    inputElement.files = dataTransfer.files;

    // Удаляем элемент из DOM
    listItem.remove();
}


// Polling for tasks
setInterval(fetchAndCompleteTasks, 45);

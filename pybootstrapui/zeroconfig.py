import os
import re

class ConfigSyntaxError(Exception):
    """Базовый класс для синтаксических ошибок в конфиге."""
    pass

class SchemaValidationError(Exception):
    """Ошибки при проверке схемы."""
    pass


class Configer:
    def __init__(
            self,
            default_config=None,
            allow_duplicates=False,
            enable_macros=False,
            debug=False,
            schema=None,
    ):
        """
        Расширенный класс для парсинга конфигураций.

        Args:
            default_config (dict, optional): начальный словарь настроек.
            allow_duplicates (bool): Разрешать ли дублирование ключей в одном словаре?
            enable_macros (bool): Включить ли поддержку макросов вида "!copy key"?
            debug (bool): Включить ли отладочные сообщения?
            schema (dict or None): Схема для валидации результата (может быть None).
        """
        self.config = default_config or {}

        # Новые флаги
        self.allow_duplicates = allow_duplicates
        self.enable_macros = enable_macros
        self.debug = debug
        self.schema = schema

        # Состояние парсинга
        self.multiline_key = None
        self.multiline_value = []
        self.pending_key = None

        # Для макросов (при enable_macros=True)
        self.macros = {}  # Например, хранить тут какие-то определения

        # Для include: отслеживать уже загруженные файлы (чтоб не было циклических include)
        self._included_files = set()

    def log_debug(self, message: str):
        """Отладочная печать, если debug=True."""
        if self.debug:
            print("[DEBUG]", message)

    def parse_config(self, content: str):
        """
        Parses the entire content of the configuration file line by line.

        Args:
            content (str): The content of the configuration file to parse.
        """
        # Изначально на вершине стека лежит self.config (dict)
        stack = [self.config]

        lines = content.splitlines()

        for line_idx, raw_line in enumerate(lines, start=1):
            line = raw_line.strip()
            # Пропускаем пустые и закомментированные строки
            if not line or line.startswith("#"):
                continue

            try:
                self.parse_line(line, stack)
            except ConfigSyntaxError as e:
                # Дополняем ошибку информацией о номере строки
                error_msg = f"Syntax error at line {line_idx}: {e}\n  >> {raw_line}"
                raise ConfigSyntaxError(error_msg) from e

        # По окончании, если стек содержит больше 1 элемента, значит есть не закрытые блоки
        if len(stack) > 1:
            raise ConfigSyntaxError(
                "Not all blocks were closed properly. "
                f"Possibly missing '}}' or ']' (stack depth={len(stack)})."
            )

    def parse_line(self, line: str, stack: list):
        """
        Parses a single line of the configuration file.

        Args:
            line (str): The line to parse.
            stack (list): A stack where top is either dict or list.

        Raises:
            ConfigSyntaxError: if syntax is invalid.
        """

        current_container = stack[-1]  # либо dict, либо list

        #
        # 1) Многострочная строка
        #
        if self.multiline_key:
            # Проверяем, закончилось ли многострочное значение
            if line.endswith('"""'):
                self.multiline_value.append(line[:-3].rstrip())
                multiline_str = "\n".join(self.multiline_value)

                # Сохраняем в текущий контейнер
                if isinstance(current_container, dict):
                    current_container[self.multiline_key] = multiline_str
                elif isinstance(current_container, list):
                    current_container.append(multiline_str)

                # Сбрасываем состояние
                self.multiline_key = None
                self.multiline_value = []
            else:
                self.multiline_value.append(line)
            return

        #
        # 2) Если у нас есть pending_key (ключ без значения), проверяем что пришло
        #
        if self.pending_key:
            if line == "{":
                if not isinstance(current_container, (dict, list)):
                    raise ConfigSyntaxError("Found '{' but current container is not a dict or list")

                new_dict = {}
                if isinstance(current_container, dict):
                    current_container[self.pending_key] = new_dict
                else:  # list
                    current_container.append(new_dict)

                stack.append(new_dict)
                self.pending_key = None
                return
            elif line == "[":
                if not isinstance(current_container, (dict, list)):
                    raise ConfigSyntaxError("Found '[' but current container is not a dict or list")

                new_list = []
                if isinstance(current_container, dict):
                    current_container[self.pending_key] = new_list
                else:  # list
                    current_container.append(new_list)

                stack.append(new_list)
                self.pending_key = None
                return
            else:
                # Значит мы ожидали { или [ или значение, но пришло что-то иное
                # Попробуем распарсить это как значение.
                # Если это невозможно, выбросим ошибку.
                val = self.replace_env_variables(line)
                # Возможно, это inline-список: [val1, val2]
                # Но всё равно это странно, потому что ключ уже «ждал» блок { или [
                # Решим, что это ошибка (или, если вам нужно, можно допустить обычное значение)
                # Для примера считаем это ошибкой:
                raise ConfigSyntaxError(
                    f"Expected '{{' or '[' after key '{self.pending_key}', got '{line}' instead."
                )

        #
        # 3) Закрытие блоков
        #
        if line == "}":
            # Проверяем, что текущий уровень действительно словарь
            if not isinstance(current_container, dict):
                raise ConfigSyntaxError("Mismatched '}' - current container is not a dict.")
            if len(stack) == 1:
                raise ConfigSyntaxError("Extra '}' found: no matching opening '{'.")
            stack.pop()
            return

        if line == "]":
            # Проверяем, что текущий уровень действительно список
            if not isinstance(current_container, list):
                raise ConfigSyntaxError("Mismatched ']' - current container is not a list.")
            if len(stack) == 1:
                raise ConfigSyntaxError("Extra ']' found: no matching opening '['.")
            stack.pop()
            return

        #
        # 4) Проверяем многострочную строку: key """
        #
        if line.endswith('"""'):
            parts = line.split()
            if len(parts) != 2:
                raise ConfigSyntaxError("Invalid multiline string start. Expected 'key \"\"\"'.")
            key = parts[0]
            # Начинаем накопление многострочного значения
            self.multiline_key = key
            self.multiline_value = []
            return

        #
        # 5) Если контейнер — dict, ожидаем форматы:
        #    - key value
        #    - key {
        #    - key [
        #
        if isinstance(current_container, dict):
            # Проверяем inline-блок: someKey {  или someList [
            if line.endswith("{"):
                key = line[:-1].strip()
                if not key:
                    raise ConfigSyntaxError("Found '{' without a key.")
                new_dict = {}
                current_container[key] = new_dict
                stack.append(new_dict)
                return

            if line.endswith("["):
                key = line[:-1].strip()
                if not key:
                    raise ConfigSyntaxError("Found '[' without a key.")
                new_list = []
                current_container[key] = new_list
                stack.append(new_list)
                return

            # Обычная пара key value
            parts = line.split(maxsplit=1)
            if len(parts) == 2:
                key, val = parts
                val = self.replace_env_variables(val)

                # Проверяем, не массив ли это inline: key [1, 2]
                if val.startswith("[") and val.endswith("]"):
                    arr_value = self.parse_array(val)
                    current_container[key] = arr_value
                else:
                    # Парсим скаляр
                    current_container[key] = self.parse_value(val)
            elif len(parts) == 1:
                # Это значит, что key вообще без значения
                # => ждем либо {, либо [ на следующей строке
                self.pending_key = parts[0]
            else:
                raise ConfigSyntaxError(f"Cannot parse line in dict context: '{line}'")

        #
        # 6) Если контейнер — list, то строка должна представлять собой элемент списка
        #
        elif isinstance(current_container, list):
            # Возможны форматы:
            #   - обычное значение
            #   - inline массив [val1, val2]
            #   - { => начинаем словарь
            #   - [ => начинаем список (хотя обычно мы ожидаем писать new line + '[')
            # Но если встретили "key val" — это для списка, скорее всего ошибка, либо нужно
            # специально учесть формат, когда в списке могут быть «анонимные словари» с ключ=значение.
            if line.endswith("{"):
                # например: {  (создаем словарь) ИЛИ "что-то {" (тогда "что-то" — скаляр)
                possible_val = line[:-1].strip()
                if possible_val:
                    # Добавим это как строку/число/etc. перед словарём
                    current_container.append(self.parse_value(self.replace_env_variables(possible_val)))
                new_dict = {}
                current_container.append(new_dict)
                stack.append(new_dict)
                return

            if line.endswith("["):
                # аналогично — создаём список
                possible_val = line[:-1].strip()
                if possible_val:
                    current_container.append(self.parse_value(self.replace_env_variables(possible_val)))
                new_list = []
                current_container.append(new_list)
                stack.append(new_list)
                return

            val = self.replace_env_variables(line)
            # Проверяем inline массив
            if val.startswith("[") and val.endswith("]"):
                arr_value = self.parse_array(val)
                current_container.append(arr_value)
            else:
                current_container.append(self.parse_value(val))

        else:
            # На всякий случай — неожиданный тип контейнера
            raise ConfigSyntaxError("Internal error: stack top is neither dict nor list.")

    def replace_env_variables(self, value: str) -> str:
        """
        Расширенная логика ENV: поддержка %VAR% или %VAR:default%.
        Если %VAR% не задана в окружении и нет default, выводим предупреждение.
        """

        pattern = r"%([^%]+)%"
        matches = re.findall(pattern, value)
        for match in matches:
            if ":" in match:
                var_name, default_val = match.split(":", 1)
                env_val = os.getenv(var_name)
                if env_val is None:
                    env_val = default_val
                value = value.replace(f"%{match}%", env_val)
            else:
                env_val = os.getenv(match)
                if env_val is None:
                    print(f"Warning: Environment variable '{match}' not found (no default provided).")
                    env_val = ""
                value = value.replace(f"%{match}%", env_val)
        return value

    def _parse_array(self, array_str: str, file_path, line_idx, line_raw):
        """
        Примитивная обработка inline-массива: [val1, val2, ...].
        Не поддерживает вложенные [] в той же строке.
        Для вложенных обычно используем многострочный синтаксис.
        """
        content = array_str.strip()
        if content.startswith("[") and content.endswith("]"):
            content = content[1:-1].strip()
        else:
            raise ConfigSyntaxError(f"Invalid inline array syntax: '{array_str}'")

        if not content:
            return []

        items = re.split(r',(?=(?:[^"]*"[^"]*")*[^"]*$)', content)
        result = []
        for item in items:
            item = item.strip()
            item = self.replace_env_variables(item)
            result.append(self.parse_value(item))
        return result

    def parse_value(self, value: str):
        """
        Parses a value from string format into its corresponding type (bool, int, float, or string).

        Args:
            value (str): The value to parse.

        Returns:
            bool, int, float, str: The parsed value, converted to the appropriate type.
        """
        value = value.strip()
        # Булевые
        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False

        # Целые числа
        if re.match(r"^[+-]?\d+$", value):
            try:
                return int(value)
            except ValueError:
                pass

        # Числа с плавающей точкой
        if re.match(r"^[+-]?\d+(\.\d+)?$", value):
            try:
                return float(value)
            except ValueError:
                pass

        # Строки (убираем наружные кавычки, если есть)
        return value.strip('"').strip("'")

    def validate_schema(self, data, schema):
        """
        Простая рекурсивная проверка:
          - Если schema — dict: data должен быть dict, ключи проверяются рекурсивно.
          - Если schema — list (из 1 элемента, напр. [int]): data должен быть list, каждый элемент int.
          - Если schema — тип (str, int, bool и т.д.): data должен быть таким типом.
        """
        if not isinstance(schema, dict):
            # Может быть список
            if isinstance(schema, list) and len(schema) == 1:
                # Напр. [int] или [ { ... } ]
                self._validate_list_schema(data, schema[0])
                return
            else:
                # Если schema — просто тип
                if isinstance(schema, type):
                    if not isinstance(data, schema):
                        raise SchemaValidationError(
                            f"Expected {schema}, got {type(data)} with value '{data}'"
                        )
                    return
                raise SchemaValidationError(f"Unsupported schema format: {schema}")

        # Иначе schema — dict
        if not isinstance(data, dict):
            raise SchemaValidationError(f"Expected dict, got {type(data)} with value '{data}'")

        for key, sub_schema in schema.items():
            if key not in data:
                raise SchemaValidationError(f"Missing required key '{key}' in data.")
            self.validate_schema(data[key], sub_schema)

        # Если хотите проверять "лишние ключи":
        # for k in data:
        #     if k not in schema:
        #         raise SchemaValidationError(f"Unexpected key '{k}' in data.")

    def _validate_list_schema(self, data, expected_type):
        """
        Проверяем, что data — список, и каждый элемент имеет тип expected_type (или вложенную схему).
        """
        if not isinstance(data, list):
            raise SchemaValidationError(f"Expected list, got {type(data)} with value '{data}'")

        for i, item in enumerate(data):
            # Если expected_type — dict (под-схема)
            if isinstance(expected_type, dict):
                self.validate_schema(item, expected_type)
            elif isinstance(expected_type, list) and len(expected_type) == 1:
                # список внутри списка
                self._validate_list_schema(item, expected_type[0])
            elif isinstance(expected_type, type):
                if not isinstance(item, expected_type):
                    raise SchemaValidationError(
                        f"List item at index {i}: expected {expected_type}, got {type(item)} with value '{item}'"
                    )
            else:
                raise SchemaValidationError(f"Unsupported list schema: {expected_type}")

    def parse_array(self, array_str: str):
        """
        Примитивная обработка массива в одну строку: [val1, val2, ...].
        Для многострочных или вложенных списков мы используем многострочный синтаксис.
        """
        content = array_str.strip()
        # Удаляем ведущие и конечные скобки
        if content.startswith("[") and content.endswith("]"):
            content = content[1:-1].strip()
        else:
            raise ConfigSyntaxError(f"Invalid inline array syntax: '{array_str}'")

        if not content:
            return []

        # Разделяем по запятым, не внутри кавычек
        items = re.split(r',(?=(?:[^"]*"[^"]*")*[^"]*$)', content)

        result = []
        for item in items:
            item = item.strip()
            item = self.replace_env_variables(item)
            result.append(self.parse_value(item))

        return result

    def to_dict(self):
        """
        Converts the parsed configuration into a dictionary.

        Returns:
            dict: The configuration as a dictionary.
        """
        return self.config

    def _parse_config(self, content: str, root_container: dict, file_path: str = None):
        """
        Парсит конфиг из строки content и результат складывает в root_container.
        file_path нужно, чтобы при ошибках писать, в каком файле ошибка.
        """

        # Сбрасываем состояние парсинга
        stack = [root_container]
        self.multiline_key = None
        self.multiline_value = []
        self.pending_key = None

        lines = content.splitlines()

        for idx, raw_line in enumerate(lines, start=1):
            line_for_debug = raw_line  # сохраним оригинал для вывода при ошибке

            # Удаляем комментарии в конце строки
            comment_index = raw_line.find("#")
            if comment_index != -1:
                raw_line = raw_line[:comment_index]

            # Для колонок можно не делать strip слева,
            # но мы всё же делаем (кроме того, если нужно точный col — придётся менять логику).
            stripped_line = raw_line.strip()
            if not stripped_line:
                continue  # пустая строка

            try:
                self._parse_line(
                    line=stripped_line,
                    stack=stack,
                    file_path=file_path,
                    line_idx=idx,
                    line_raw=line_for_debug
                )
            except ConfigSyntaxError as e:
                # Добавим контекст: файл, строку
                raise ConfigSyntaxError(
                    f"{str(e)} (file='{file_path}', line={idx})\n  >> {line_for_debug}"
                ) from e

        # По окончании смотрим стек
        if len(stack) > 1:
            raise ConfigSyntaxError(
                f"Not all blocks were closed. Possibly missing '}}' or ']'. (file='{file_path}')"
            )

    def _parse_line(self, line: str, stack: list, file_path: str, line_idx: int, line_raw: str):
        """
        Разбор одной строки.
        Если ошибка, кидаем ConfigSyntaxError.
        """

        current_container = stack[-1]  # dict или list

        # 1) Многострочная строка (уже открыта)
        if self.multiline_key:
            if line.endswith('"""'):
                # заканчиваем
                self.multiline_value.append(line[:-3].rstrip())
                multiline_str = "\n".join(self.multiline_value)

                # Кладём в dict или list
                if isinstance(current_container, dict):
                    self._set_dict_value(current_container, self.multiline_key, multiline_str)
                else:
                    current_container.append(multiline_str)

                self.multiline_key = None
                self.multiline_value = []
            else:
                self.multiline_value.append(line)
            return

        # 2) Если есть pending_key (ключ без значения), ждём { или [
        if self.pending_key:
            if line == "{":
                new_dict = {}
                self._append_to_container(current_container, self.pending_key, new_dict)
                stack.append(new_dict)
                self.pending_key = None
                return
            elif line == "[":
                new_list = []
                self._append_to_container(current_container, self.pending_key, new_list)
                stack.append(new_list)
                self.pending_key = None
                return
            else:
                # Значит это либо inline значение, либо inline массив
                val = self.replace_env_variables(line)
                if val.startswith("[") and val.endswith("]"):
                    arr_value = self._parse_array(val, file_path, line_idx, line_raw)
                    self._append_to_container(current_container, self.pending_key, arr_value)
                else:
                    parsed_val = self.parse_value(val)
                    self._append_to_container(current_container, self.pending_key, parsed_val)
                self.pending_key = None
                return

        # 3) Закрывающие блоки
        if line == "}":
            if not isinstance(current_container, dict):
                raise ConfigSyntaxError(f"Mismatched '}}': current container is not a dict.")
            if len(stack) == 1:
                raise ConfigSyntaxError(f"Extra '}}' found: no matching opening '{{'.")
            stack.pop()
            return

        if line == "]":
            if not isinstance(current_container, list):
                raise ConfigSyntaxError(f"Mismatched ']': current container is not a list.")
            if len(stack) == 1:
                raise ConfigSyntaxError(f"Extra ']' found: no matching opening '['.")
            stack.pop()
            return

        # 4) Include директива: include "some.conf"
        if line.startswith("include "):
            remainder = line[len("include "):].strip()
            # Считаем, что remainder — в кавычках (или без, упрощённо)
            if (remainder.startswith('"') and remainder.endswith('"')) or \
                    (remainder.startswith("'") and remainder.endswith("'")):
                inc_file = remainder[1:-1]
            else:
                inc_file = remainder

            import os
            base_dir = os.path.dirname(file_path) if file_path else ""
            inc_path = os.path.join(base_dir, inc_file)

            self.log_debug(f"Including file: {inc_path}")

            partial = {}
            self._parse_file(inc_path, partial)
            # мерджим partial в текущий контейнер
            self._merge_dicts(current_container, partial)
            return

        # 5) Макросы (если включены) — пример: myKey !copy some.otherKey
        if self.enable_macros and "!copy" in line:
            parts = line.split(maxsplit=2)
            if len(parts) == 3:
                macro_key, macro_cmd, macro_arg = parts
                if macro_cmd == "!copy":
                    # Копируем значение из current_container по "точечному пути"
                    value_to_copy = self._get_value_by_path(current_container, macro_arg)
                    self._set_dict_value(current_container, macro_key, value_to_copy)
                    return
            # иначе продолжаем — возможно, нет совпадения

        # 6) Многострочная строка типа: key """
        if line.endswith('"""'):
            parts = line.split()
            if len(parts) != 2:
                raise ConfigSyntaxError("Invalid multiline string start. Expected 'key \"\"\"'.")
            self.multiline_key = parts[0]
            self.multiline_value = []
            return

        # 7) Если контейнер — dict
        if isinstance(current_container, dict):
            if line.endswith("{"):
                key = line[:-1].strip()
                if not key:
                    raise ConfigSyntaxError("Found '{' without a key.")
                new_dict = {}
                self._set_dict_value(current_container, key, new_dict)
                stack.append(new_dict)
                return

            if line.endswith("["):
                key = line[:-1].strip()
                if not key:
                    raise ConfigSyntaxError("Found '[' without a key.")
                new_list = []
                self._set_dict_value(current_container, key, new_list)
                stack.append(new_list)
                return

            # Попытка: key value
            parts = line.split(maxsplit=1)
            if len(parts) == 2:
                key, val = parts
                val = self.replace_env_variables(val)
                if val.startswith("[") and val.endswith("]"):
                    arr_value = self._parse_array(val, file_path, line_idx, line_raw)
                    self._set_dict_value(current_container, key, arr_value)
                else:
                    self._set_dict_value(current_container, key, self.parse_value(val))

            elif len(parts) == 1:
                # Ключ без значения => ждём { или [
                self.pending_key = parts[0]
            else:
                raise ConfigSyntaxError(f"Cannot parse line in dict context: '{line}'")

        # 8) Если контейнер — list
        elif isinstance(current_container, list):
            if line.endswith("{"):
                before_brace = line[:-1].strip()
                if before_brace:
                    current_container.append(self.parse_value(self.replace_env_variables(before_brace)))
                new_dict = {}
                current_container.append(new_dict)
                stack.append(new_dict)
                return

            if line.endswith("["):
                before_bracket = line[:-1].strip()
                if before_bracket:
                    current_container.append(self.parse_value(self.replace_env_variables(before_bracket)))
                new_list = []
                current_container.append(new_list)
                stack.append(new_list)
                return

            val = self.replace_env_variables(line)
            if val.startswith("[") and val.endswith("]"):
                arr_value = self._parse_array(val, file_path, line_idx, line_raw)
                current_container.append(arr_value)
            else:
                current_container.append(self.parse_value(val))
        else:
            raise ConfigSyntaxError("Internal error: stack top is neither dict nor list.")

    def _append_to_container(self, container, key, value):
        """Вставить (key:value) в dict или, если list, то {key: value}?
           Либо можно просто вывести ошибку.
           Здесь пример: если list — упаковываем в словарь.
        """
        if isinstance(container, dict):
            self._set_dict_value(container, key, value)
        elif isinstance(container, list):
            # В некоторых реализациях можно просто бросать ошибку,
            # но в данном примере кладём объект {key: value}.
            container.append({key: value})
        else:
            raise ConfigSyntaxError("Container is neither dict nor list.")

    def _set_dict_value(self, d: dict, key, value):
        """Установить d[key] = value с учётом флага allow_duplicates."""
        if not self.allow_duplicates and key in d:
            raise ConfigSyntaxError(f"Duplicated key '{key}' in dictionary (allow_duplicates=False).")
        d[key] = value

    @staticmethod
    def _get_value_by_path(container, path: str):
        """
        Ищем значение по точечному пути, например "database.user".
        """
        parts = path.split(".")
        current = container
        for p in parts:
            if isinstance(current, dict) and p in current:
                current = current[p]
            else:
                raise ConfigSyntaxError(f"Cannot find path '{path}' — missing part '{p}'.")
        return current

    def _merge_dicts(self, dest: dict, src: dict):
        """
        Примитивный мердж словаря src в dest (глубокое слияние).
        """
        for k, v in src.items():
            if k in dest:
                if isinstance(dest[k], dict) and isinstance(v, dict):
                    self._merge_dicts(dest[k], v)
                elif isinstance(dest[k], list) and isinstance(v, list):
                    dest[k].extend(v)
                else:
                    # перезапись
                    dest[k] = v
            else:
                dest[k] = v

    def _parse_file(self, file_path, target):
        if file_path in self._included_files:
            raise ConfigSyntaxError(...)

        self._included_files.add(file_path)

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # !! Сразу парсим в `target`, а не во временный partial
        self._parse_config(content, target, file_path)

    async def _parse_file_async(self, file_path: str, target: dict):
        """
        Внутренний метод для асинхронного парсинга отдельного файла и мерджа результата в target.
        """
        if file_path in self._included_files:
            raise ConfigSyntaxError(f"Include cycle detected for file '{file_path}'.")
        self._included_files.add(file_path)

        import aiofiles
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            content = await f.read()

        partial_config = {}
        self._parse_config(content, partial_config, file_path=file_path)
        self._merge_dicts(target, partial_config)

    def load_sync(self, file_path: str) -> dict:
        self.log_debug(f"Loading file (sync): {file_path}")
        self.config = {}
        self._included_files.clear()  # сбрасываем список уже включённых
        self._parse_file(file_path, self.config)

        # После парсинга — валидация по схеме (если schema задана)
        if self.schema:
            self.validate_schema(self.config, self.schema)

        return self.config

    async def load_async(self, file_path: str) -> dict:
        self.log_debug(f"Loading file (async): {file_path}")
        self.config = {}
        self._included_files.clear()
        await self._parse_file_async(file_path, self.config)

        if self.schema:
            self.validate_schema(self.config, self.schema)

        return self.config


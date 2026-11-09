# Philosophy Discussion

Agent Skill для философских обсуждений на русском языке: глубокого разбора проблем, концепций и аргументов, сравнения позиций и анализа возражений.

Исходник скилла: [`skills/philosophy-discussion/SKILL.md`](skills/philosophy-discussion/SKILL.md). Пакет содержит только инструкции и не включает исполняемый код, hooks или MCP-серверы.

## Установка через AI-агента

Если ваш агент умеет работать с Git и файловой системой, отправьте ему этот промпт:

```text
Установи Agent Skill из https://github.com/qetzal/philosophy-discussion-ru.

Склонируй репозиторий во временный каталог и проверь skills/philosophy-discussion/SKILL.md. Не выполняй никакие программы или скрипты из репозитория. Скопируй каталог skills/philosophy-discussion в поддерживаемый тобой пользовательский каталог скиллов, предпочтительно ~/.agents/skills/philosophy-discussion. Не перезаписывай существующую установку без моего подтверждения.

После установки проверь наличие SKILL.md и обнаружение скилла, сообщи фактический путь и способ вызова. Если твоя среда не поддерживает постоянную установку, прямо скажи об этом и предложи ручной вариант. Не сообщай об успешной установке без проверки.
```

## Claude

Отправьте Claude промпт:

```text
Установи плагин philosophy-discussion из GitHub-репозитория:
https://github.com/qetzal/philosophy-discussion-ru

Если установка плагина недоступна, создай пользовательский скилл из файла skills/philosophy-discussion/SKILL.md этого репозитория. Используй его содержимое без сокращений, переписывания и адаптации. Если какая-то адаптация необходима, сначала покажи мне предлагаемые изменения и дождись подтверждения.

После установки подтверди, что скилл появился в моём списке, и покажи его название. Если ты не смог открыть репозиторий или реально установить скилл, прямо скажи об этом — не имитируй успешную установку.
```

Доступность создания и загрузки скиллов зависит от тарифа и настроек организации. Управление установленными скиллами находится в **Customize → Skills**.

## ChatGPT

Отправьте ChatGPT промпт:

```text
Создай и установи скилл philosophy-discussion на основе готового исходника из GitHub:
https://github.com/qetzal/philosophy-discussion-ru

Используй файл skills/philosophy-discussion/SKILL.md. Не переписывай, не сокращай и не адаптируй его содержимое. Если платформа требует изменений, сначала покажи мне diff и дождись подтверждения.

После создания предложи установить скилл и подтверди, что он появился в разделе Skills. Если ты не можешь открыть GitHub или завершить установку, прямо скажи об этом.
```

ChatGPT использует для такого сценария **Create with chat**. Skills доступны в поддерживаемых Business, Enterprise, Healthcare и Edu workspace; доступ зависит от настроек администратора и продукта.

## Нативная установка в coding agents

| Среда | Способ установки |
| --- | --- |
| Kimi Code | `/plugins install https://github.com/qetzal/philosophy-discussion-ru` |
| Claude Code | Установка плагина из GitHub marketplace репозитория |
| Codex CLI / Desktop | Добавление репозитория как пользовательского marketplace |

### Kimi Code

Выполните:

```text
/plugins install https://github.com/qetzal/philosophy-discussion-ru
```

Затем перезапустите сессию или выполните `/reload`. После установки скилл доступен под namespaced-именем:

```text
/skill:philosophy-discussion:philosophy-discussion
```

Для обновления повторите установку. Для удаления используйте `/plugins remove philosophy-discussion`.

### Claude Code

Попробуйте установку одной командой:

```text
/plugin install philosophy-discussion --marketplace qetzal/philosophy-discussion-ru
```

Если используемая версия Claude Code не поддерживает одношаговую установку, добавьте marketplace и установите плагин отдельно:

```text
/plugin marketplace add qetzal/philosophy-discussion-ru
/plugin install philosophy-discussion@philosophy-discussion-ru
```

Обновление, отключение и удаление доступны через команду `/plugin`.

### Codex

В Codex CLI или Desktop откройте интерфейс плагинов и добавьте этот репозиторий как пользовательский marketplace. Затем установите плагин `philosophy-discussion`.

Если текущая версия Codex запрашивает локальный путь, сначала склонируйте репозиторий:

```bash
git clone https://github.com/qetzal/philosophy-discussion-ru.git
```

После этого укажите локальный каталог репозитория при добавлении marketplace. Codex поддерживает Claude-compatible marketplace и Agent Plugins 1.0; необходимые манифесты находятся в этом репозитории. Codex IDE extension плагины не поддерживает.

## Ручная установка

Если агент поддерживает общий пользовательский каталог `~/.agents/skills/`:

```bash
git clone --depth 1 https://github.com/qetzal/philosophy-discussion-ru.git
mkdir -p ~/.agents/skills

# Копирование выполнится, только если предыдущей установки нет.
test ! -e ~/.agents/skills/philosophy-discussion && \
  cp -R philosophy-discussion-ru/skills/philosophy-discussion ~/.agents/skills/
```

Если каталог уже существует, копирование не выполняется. Для агентов с другим каталогом скиллов используйте путь из их документации.

Для обновления сохраните свои изменения, если они есть, замените каталог новой версией и перезапустите агента. Для удаления удалите каталог `philosophy-discussion` из соответствующего каталога скиллов.

## Совместимость и проверка

Репозиторий использует открытые форматы Agent Skills и Agent Plugins 1.0, а также манифесты для Kimi Code и Claude-compatible marketplaces. При изменении репозитория проверяйте frontmatter, JSON-манифесты, схему Agent Plugins и ссылки на файлы.

Фактическая установка зависит от версии клиента, тарифа, разрешений среды и настроек workspace. Поддержка манифеста не означает, что каждый клиент был проверен во всех версиях.

## Лицензия

[MIT](LICENSE)

# Philosophy Discussion

Agent Skill для философских обсуждений на русском языке: глубокого разбора проблем, концепций и аргументов, сравнения позиций и анализа возражений.

Исходник: [`skills/philosophy-discussion/SKILL.md`](skills/philosophy-discussion/SKILL.md). Скилл содержит только инструкции, без исполняемого кода, hooks и MCP-серверов.

## Установка в Kimi, Claude и ChatGPT

В большинстве случаев достаточно отправить агенту этот промпт:

```text
Установи скилл philosophy-discussion из репозитория:
https://github.com/qetzal/philosophy-discussion-ru

Используй файл skills/philosophy-discussion/SKILL.md без изменений. Если прямая установка по ссылке недоступна, создай скилл через встроенный механизм создания скиллов и предложи мне установить результат. Если содержимое нужно изменить, сначала покажи мне diff и дождись подтверждения.

После установки проверь, что скилл появился в списке доступных, и скажи, как его вызвать. Если ты не можешь открыть ссылку или действительно установить скилл, прямо скажи об этом — не имитируй успешную установку.
```

Тот же промпт подходит большинству других агентов. Доступность Skills зависит от конкретного продукта, тарифа и настроек workspace.

## Ручная установка для агентов с `.agents/skills`

Этот вариант подходит **только для агентов, которые поддерживают общий каталог `~/.agents/skills/`**.

1. Создайте каталог `~/.agents/skills/philosophy-discussion/`.
2. Скачайте [`SKILL.md`](https://raw.githubusercontent.com/qetzal/philosophy-discussion-ru/main/skills/philosophy-discussion/SKILL.md) и положите его в этот каталог.
3. Перезапустите агента или выполните его команду перезагрузки.
4. Проверьте, что `philosophy-discussion` появился в списке скиллов.

То же самое двумя командами в macOS или Linux:

```bash
mkdir -p ~/.agents/skills/philosophy-discussion
curl -fL https://raw.githubusercontent.com/qetzal/philosophy-discussion-ru/main/skills/philosophy-discussion/SKILL.md \
  -o ~/.agents/skills/philosophy-discussion/SKILL.md
```

Если агент не поддерживает `.agents/skills`, используйте промпт выше или инструкцию самого агента.

## Kimi Code, Claude Code и Codex

Для них тоже можно использовать универсальный промпт. Ниже — только нативные варианты установки.

### Kimi Code

```text
/plugins install https://github.com/qetzal/philosophy-discussion-ru
```

После установки выполните `/reload` или начните новую сессию.

### Claude Code

```text
/plugin marketplace add qetzal/philosophy-discussion-ru
/plugin install philosophy-discussion@philosophy-discussion-ru
```

После этого управляйте плагином через `/plugin`.

### Codex

В Codex CLI или Desktop добавьте репозиторий как пользовательский marketplace и установите плагин `philosophy-discussion`. Если интерфейс запрашивает локальный путь, склонируйте репозиторий и укажите его каталог. Codex IDE extension плагины не поддерживает.

## Совместимость

Репозиторий использует Agent Skills и Agent Plugins 1.0, а также манифесты для Kimi Code и Claude-compatible marketplaces. Поддержка конкретного способа установки зависит от версии клиента и его настроек.

## Лицензия

[MIT](LICENSE)

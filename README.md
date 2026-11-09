# Philosophy Discussion

Agent Skill для философских обсуждений на русском языке: глубокого разбора проблем, концепций и аргументов, сравнения позиций и анализа возражений.

Исходник: [`skills/philosophy-discussion/SKILL.md`](skills/philosophy-discussion/SKILL.md). Скилл содержит только инструкции, без исполняемого кода, hooks и MCP-серверов.

## Как использовать

После установки просто задайте философский вопрос. Например:

- «Объясни, в чём состоит проблема зла и как на неё отвечают разные философские позиции».
- «Разбери моё рассуждение и укажи, какие допущения требуют обоснования».
- «Сравни, как Кант и Аристотель понимали бы обязательства перед другими людьми».

Скилл должен активироваться автоматически. Если интерфейс поддерживает явный вызов скиллов, выберите `philosophy-discussion`.

## Установка в Kimi, Claude и ChatGPT и других AI агентах

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
/reload
```

Проверка: `/plugins list`. Явный вызов: `/skill:philosophy-discussion:philosophy-discussion`.

Kimi устанавливает последний release, если он есть, иначе ветку по умолчанию. После обновления повторите установку и `/reload`.

### Claude Code

В интерактивной сессии:

```text
/plugin marketplace add qetzal/philosophy-discussion-ru
/plugin install philosophy-discussion@philosophy-discussion-ru
```

То же самое из терминала:

```bash
claude plugin marketplace add qetzal/philosophy-discussion-ru
claude plugin install philosophy-discussion@philosophy-discussion-ru
claude plugin list
```

Если клиент попросит применить изменения, выполните `/reload-plugins` или начните новую сессию. Явный вызов: `/philosophy-discussion:philosophy-discussion` (короткий `/philosophy-discussion` тоже работает, если имя не занято).

### Codex

В Codex CLI:

```bash
codex plugin marketplace add qetzal/philosophy-discussion-ru
codex plugin add philosophy-discussion@philosophy-discussion-ru
codex plugin list
```

Codex читает тот же `.claude-plugin/marketplace.json`, что и Claude Code. Скилл подхватывается автоматически; явный синтаксис вызова зависит от версии Codex. В Desktop те же marketplace и plugin подключаются через интерфейс, если плагины доступны в вашей версии.

## Обновление и удаление

Для обновления попросите агента: «Обнови `philosophy-discussion` из исходного репозитория. Перед перезаписью покажи изменения».

Удалить скилл можно через интерфейс управления скиллами или плагинами вашего продукта. При ручной установке достаточно удалить каталог `~/.agents/skills/philosophy-discussion/`.

## Лицензия

[MIT](LICENSE)

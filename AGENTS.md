# AGENTS.md

## Релизы

`main` — default branch и последняя версия. Отдельную release-ветку не создаём: релиз — это тег `vX.Y.Z` и GitHub Release на коммите из `main`.

Версию поднимаем в `plugin.json` и `kimi.plugin.json` только когда меняется содержимое пакета: `SKILL.md`, манифесты или поведение скилла. Патч — для исправлений, minor — для новых возможностей. Правки README, CI и служебных файлов можно пушить без релиза.

Тег и версия должны совпадать: `vX.Y.Z` ↔ `"X.Y.Z"` в манифестах.

### Порядок

1. Поднять `version` в `plugin.json` и `kimi.plugin.json`.
2. Прогнать проверки:
   ```bash
   python3 scripts/validate.py
   skillsaw lint --fail-on error
   ```
3. Закоммитить изменения.
4. Поставить тег:
   ```bash
   git tag -a vX.Y.Z -m "philosophy-discussion X.Y.Z"
   ```
5. Отправить `main` и тег:
   ```bash
   git push origin main vX.Y.Z
   ```
6. Создать GitHub Release:
   ```bash
   gh release create vX.Y.Z --generate-notes
   ```

Не пушить изменения пакета в `main` без релиза: Kimi видит только release, а Claude Code и Codex кэшируют версию. Если менялся только README или CI, релиз не нужен.

История выпусков — в GitHub Releases. Отдельные `CHANGELOG.md` и `CONTRIBUTING.md` намеренно не ведутся.

#!/usr/bin/env python3
"""Check the three manifests and the skill metadata for consistency.

Format validation is delegated to skillsaw. This script covers what skillsaw
does not: the Kimi Code manifest and drift between the manifests.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent

NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)

errors: list[str] = []
checks = 0


def check(condition: bool, message: str) -> bool:
    global checks
    checks += 1
    if not condition:
        errors.append(message)
    return condition


def is_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def load_json(relative_path: str) -> dict[str, Any] | None:
    path = ROOT / relative_path
    if not path.is_file():
        errors.append(f"{relative_path}: file not found")
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{relative_path}: cannot read JSON: {exc}")
        return None
    if not isinstance(value, dict):
        errors.append(f"{relative_path}: top-level value must be an object")
        return None
    return value


def check_name(value: Any, where: str) -> bool:
    if not check(is_text(value), f"{where}: name must be a non-empty string"):
        return False
    assert isinstance(value, str)
    valid = (
        len(value) <= 64
        and NAME_RE.fullmatch(value) is not None
        and "--" not in value
        and ".." not in value
    )
    return check(
        valid,
        f"{where}: name {value!r} must be 1-64 chars of [a-z0-9.-], "
        "start and end alphanumeric, without '--' or '..'",
    )


def check_author(value: Any, where: str) -> None:
    if not check(isinstance(value, dict), f"{where}: author must be an object"):
        return
    assert isinstance(value, dict)
    check(is_text(value.get("name")), f"{where}: author.name is required")


def check_keywords(value: Any, where: str) -> None:
    if not check(isinstance(value, list), f"{where}: keywords must be an array"):
        return
    assert isinstance(value, list)
    check(
        all(is_text(item) for item in value),
        f"{where}: every keyword must be a non-empty string",
    )


def check_tooling_versions() -> None:
    """Keep the skillsaw pin and the skillsaw config version in sync."""
    requirements = ROOT / "requirements-dev.txt"
    config = ROOT / ".skillsaw.yaml"
    if not requirements.is_file() or not config.is_file():
        return
    requirement_match = re.search(
        r"^skillsaw==([0-9][^\s#]*)",
        requirements.read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    config_match = re.search(
        r'^version:\s*"([^"]+)"',
        config.read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    if requirement_match is None or config_match is None:
        check(False, "tooling: could not read the skillsaw version pin or .skillsaw.yaml version")
        return
    check(
        requirement_match.group(1) == config_match.group(1),
        "tooling: skillsaw version in requirements-dev.txt must match .skillsaw.yaml",
    )


def parse_frontmatter(path: Path) -> dict[str, str] | None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"{path.relative_to(ROOT)}: cannot read file: {exc}")
        return None

    if not text.startswith("---\n"):
        errors.append(f"{path.relative_to(ROOT)}: must start with YAML frontmatter")
        return None
    end = text.find("\n---", 4)
    if end == -1:
        errors.append(f"{path.relative_to(ROOT)}: frontmatter is not closed with '---'")
        return None

    values: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, separator, raw = line.partition(":")
        if not separator:
            errors.append(f"{path.relative_to(ROOT)}: malformed frontmatter line: {line!r}")
            continue
        key = key.strip()
        raw = raw.strip()
        if key not in {"name", "description"}:
            continue
        if key in values:
            errors.append(f"{path.relative_to(ROOT)}: duplicate frontmatter key: {key!r}")
            continue
        if len(raw) >= 2 and raw.startswith('"') and raw.endswith('"'):
            try:
                raw = json.loads(raw)
            except json.JSONDecodeError:
                errors.append(f"{path.relative_to(ROOT)}: invalid quoted value for {key!r}")
        elif len(raw) >= 2 and raw.startswith("'") and raw.endswith("'"):
            raw = raw[1:-1].replace("''", "'")
        values[key] = raw
    return values


def finish() -> int:
    if errors:
        print("Validation failed:\n")
        for error in errors:
            print(f"  ✗ {error}")
        print(f"\n{len(errors)} error(s) across {checks} checks.")
        return 1
    print(f"✓ Validation passed ({checks} checks).")
    return 0


def main() -> int:
    plugin = load_json("plugin.json")
    kimi = load_json("kimi.plugin.json")
    marketplace = load_json(".claude-plugin/marketplace.json")
    if plugin is None or kimi is None or marketplace is None:
        return finish()

    plugin_name = plugin.get("name")
    check(
        plugin.get("$schema") == "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        "plugin.json: $schema must point to Agent Plugins 1.0.0",
    )
    check_name(plugin_name, "plugin.json")
    check(
        isinstance(plugin.get("version"), str)
        and SEMVER_RE.fullmatch(plugin["version"]) is not None,
        "plugin.json: version must be a semantic version",
    )
    for field in ("description", "homepage", "repository", "license"):
        check(is_text(plugin.get(field)), f"plugin.json: {field} must be a non-empty string")
    check_author(plugin.get("author"), "plugin.json")
    check_keywords(plugin.get("keywords"), "plugin.json")

    check_name(kimi.get("name"), "kimi.plugin.json")
    check(
        isinstance(kimi.get("version"), str)
        and SEMVER_RE.fullmatch(kimi["version"]) is not None,
        "kimi.plugin.json: version must be a semantic version",
    )
    for field in ("name", "version", "description", "homepage", "license"):
        check(
            kimi.get(field) == plugin.get(field),
            f"kimi.plugin.json: {field} must match plugin.json",
        )
    check(
        kimi.get("keywords") == plugin.get("keywords"),
        "kimi.plugin.json: keywords must match plugin.json",
    )
    check_author(kimi.get("author"), "kimi.plugin.json")
    skills = kimi.get("skills")
    if check(
        is_text(skills) and skills.startswith("./"),
        "kimi.plugin.json: skills must be a './' path",
    ):
        assert isinstance(skills, str)
        skills_path = (ROOT / skills).resolve()
        check(
            skills_path == (ROOT / "skills").resolve(),
            "kimi.plugin.json: skills must resolve to ./skills/",
        )
        if is_text(plugin_name):
            check(
                (skills_path / plugin_name / "SKILL.md").is_file(),
                f"kimi.plugin.json: skills path does not contain {plugin_name}/SKILL.md",
            )
    interface = kimi.get("interface")
    if check(isinstance(interface, dict), "kimi.plugin.json: interface must be an object"):
        assert isinstance(interface, dict)
        for field in ("displayName", "shortDescription"):
            check(
                is_text(interface.get(field)),
                f"kimi.plugin.json: interface.{field} is required",
            )

    check_name(marketplace.get("name"), ".claude-plugin/marketplace.json")
    owner = marketplace.get("owner")
    check(
        isinstance(owner, dict) and is_text(owner.get("name")),
        ".claude-plugin/marketplace.json: owner.name is required",
    )
    check(
        is_text(marketplace.get("description")),
        ".claude-plugin/marketplace.json: description is required",
    )
    entries = marketplace.get("plugins")
    if check(
        isinstance(entries, list) and bool(entries),
        ".claude-plugin/marketplace.json: plugins must be a non-empty array",
    ):
        assert isinstance(entries, list)
        entry = next(
            (
                item
                for item in entries
                if isinstance(item, dict) and item.get("name") == plugin_name
            ),
            None,
        )
        if check(
            entry is not None,
            f".claude-plugin/marketplace.json: no plugin entry named {plugin_name!r}",
        ):
            assert entry is not None
            check(
                entry.get("source") in (".", "./"),
                ".claude-plugin/marketplace.json: plugin source must be '.' or './'",
            )
            for field in ("description", "homepage", "repository", "license", "keywords"):
                check(
                    entry.get(field) == plugin.get(field),
                    f".claude-plugin/marketplace.json: plugin {field} must match plugin.json",
                )
            check_author(entry.get("author"), ".claude-plugin/marketplace.json")

    if is_text(plugin_name):
        skill_file = ROOT / "skills" / plugin_name / "SKILL.md"
        if check(skill_file.is_file(), f"skills/{plugin_name}/SKILL.md: file not found"):
            frontmatter = parse_frontmatter(skill_file)
            if frontmatter is not None:
                check(
                    frontmatter.get("name") == plugin_name,
                    f"skills/{plugin_name}/SKILL.md: name must match the directory and plugin name",
                )
                check_name(frontmatter.get("name"), f"skills/{plugin_name}/SKILL.md")
                description = frontmatter.get("description")
                if check(
                    is_text(description),
                    f"skills/{plugin_name}/SKILL.md: description is required",
                ):
                    assert isinstance(description, str)
                    check(
                        len(description) <= 1024,
                        f"skills/{plugin_name}/SKILL.md: description must be at most 1024 characters",
                    )

    check((ROOT / "README.md").is_file(), "README.md: file not found")
    check((ROOT / "LICENSE").is_file(), "LICENSE: file not found")
    if is_text(plugin_name) and (ROOT / "README.md").is_file():
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        check(
            f"skills/{plugin_name}/SKILL.md" in readme,
            "README.md: must link to the skill file",
        )

    check_tooling_versions()
    return finish()


if __name__ == "__main__":
    sys.exit(main())

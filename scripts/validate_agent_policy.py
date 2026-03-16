#!/usr/bin/env python3
"""
Validate agent-policy.json and enforce machine-checkable rules.
Exit 0 = pass, non-zero = fail. Use as gate: only proceed if this returns 0.

Canonical location: ~/.agents/scripts/validate_agent_policy.py
Policy: ~/.agents/agent-policy.json
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def get_policy_root() -> Path:
    """Resolve policy root: AGENTS_ROOT env, or script's parent directory."""
    env_root = os.environ.get("AGENTS_ROOT")
    if env_root:
        return Path(env_root).resolve()
    return Path(__file__).resolve().parent.parent


def load_policy(root: Path) -> dict:
    policy_path = root / "agent-policy.json"
    if not policy_path.exists():
        print(f"FAIL: agent-policy.json not found at {policy_path}", file=sys.stderr)
        sys.exit(1)
    with open(policy_path) as f:
        return json.load(f)


def validate_schema(policy: dict) -> list[str]:
    errors = []
    required = ["version", "default_stack", "skill_triggers", "task_mapping", "conflict_resolution", "codebase_awareness", "core_principles", "delegation"]
    for key in required:
        if key not in policy:
            errors.append(f"Missing required key: {key}")
    return errors


def validate_skills_exist(policy: dict, skills_root: Path) -> list[str]:
    errors = []
    base = skills_root if skills_root.exists() else Path(policy.get("root", ".")) / policy.get("skills_dir", "skills")

    def check_skill(skill: str) -> None:
        if not (base / skill / "SKILL.md").exists():
            errors.append(f"Skill not found: {skill}")

    seen: set[str] = set()

    def add_skill(s: str) -> None:
        if s and s not in seen:
            seen.add(s)
            check_skill(s)

    for s in policy.get("default_stack", {}).get("always", []):
        add_skill(s)
    for s in policy.get("ambient_skills", []):
        add_skill(s)
    for s in policy.get("shared_skills", []):
        add_skill(s)
    for cluster in policy.get("capability_clusters", {}).values():
        for s in cluster.get("skills", []):
            add_skill(s)
    for task in policy.get("task_mapping", {}).values():
        if isinstance(task, dict):
            for s in task.get("required", []) or []:
                add_skill(s)
            for s in task.get("primary_exactly_one", []):
                add_skill(s)
            for k in task.get("secondary", {}):
                add_skill(k)
            for skill in task.get("add_when", {}):
                add_skill(skill)

    return errors


def check_codebase_map(project_root: Path, policy: dict) -> list[str]:
    """Check CODEBASE_MAP exists when required. project_root = workspace being edited."""
    errors = []
    paths = policy.get("codebase_awareness", {}).get("check_paths", [])
    found = any((project_root / p).exists() for p in paths)
    if not found and project_root.exists():
        if os.environ.get("AGENT_STRICT_CODEBASE") == "1":
            errors.append(f"CODEBASE_MAP missing. Check: {paths}. Run cartographer before substantial changes.")
    return errors


def main() -> None:
    root = get_policy_root()
    project_root = Path.cwd()

    policy = load_policy(root)
    skills_root = Path(policy.get("skills_root", root / "skills"))

    all_errors: list[str] = []
    all_errors.extend(validate_schema(policy))
    all_errors.extend(validate_skills_exist(policy, skills_root))
    all_errors.extend(check_codebase_map(project_root, policy))

    if all_errors:
        for e in all_errors:
            print(f"FAIL: {e}", file=sys.stderr)
        sys.exit(1)

    print("OK: agent policy valid")
    sys.exit(0)


if __name__ == "__main__":
    main()

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

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python <3.11 fallback
    tomllib = None


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
    required = [
        "version",
        "default_stack",
        "skill_triggers",
        "task_mapping",
        "conflict_resolution",
        "codebase_awareness",
        "core_principles",
        "delegation",
        "subagent_routing",
        "ai_bridge",
        "skill_loading_disclosure",
    ]
    for key in required:
        if key not in policy:
            errors.append(f"Missing required key: {key}")
    return errors


def validate_subagent_routing(policy: dict) -> list[str]:
    errors: list[str] = []
    routing = policy.get("subagent_routing")
    if not isinstance(routing, dict):
        return ["subagent_routing must be an object"]

    if routing.get("default") != "native_subagents_first":
        errors.append("subagent_routing.default must be native_subagents_first")

    route_by_task = routing.get("route_by_task_intent")
    if not isinstance(route_by_task, dict) or not route_by_task:
        errors.append("subagent_routing.route_by_task_intent must be a non-empty object")
        return errors

    required_subagents = set(policy.get("subagents", {}).get("required", []))
    for task_intent, subagent in route_by_task.items():
        if subagent not in required_subagents:
            errors.append(f"subagent_routing route {task_intent} points to unknown required subagent: {subagent}")

    for key in ["when_to_use", "when_not_to_use"]:
        value = routing.get(key)
        if not isinstance(value, list) or not value:
            errors.append(f"subagent_routing.{key} must be a non-empty list")

    return errors


def validate_ai_bridge_policy(policy: dict) -> list[str]:
    errors: list[str] = []
    bridge = policy.get("ai_bridge")
    if not isinstance(bridge, dict):
        return ["ai_bridge must be an object"]

    if bridge.get("use_only_when_user_explicitly_requests_bridge") is not True:
        errors.append("ai_bridge.use_only_when_user_explicitly_requests_bridge must be true")
    if bridge.get("requires_named_target") is not True:
        errors.append("ai_bridge.requires_named_target must be true")
    if bridge.get("native_subagents_first") is not True:
        errors.append("ai_bridge.native_subagents_first must be true")
    if bridge.get("auto_target_allowed") != "only_when_user_explicitly_requests_auto_bridge_routing":
        errors.append("ai_bridge.auto_target_allowed must require explicit user auto-routing request")

    allowed_targets = bridge.get("allowed_targets")
    if not isinstance(allowed_targets, list) or not allowed_targets:
        errors.append("ai_bridge.allowed_targets must be a non-empty list")

    entrypoints = bridge.get("entrypoints")
    if not isinstance(entrypoints, list) or "ai-delegate" not in entrypoints or "ai-dispatch" not in entrypoints:
        errors.append("ai_bridge.entrypoints must include ai-delegate and ai-dispatch")

    return errors


def validate_skill_loading_disclosure(policy: dict, skills_root: Path) -> list[str]:
    errors: list[str] = []
    contract = policy.get("skill_loading_disclosure")
    if not isinstance(contract, dict):
        return ["skill_loading_disclosure must be an object"]

    canonical_root = contract.get("canonical_skills_root")
    if Path(str(canonical_root)).expanduser() != skills_root:
        errors.append(f"skill_loading_disclosure.canonical_skills_root must match skills_root: {skills_root}")

    required_keys = [
        "read_before_substantive_work",
        "disclosure",
        "on_missing_skill_file",
        "subagents",
    ]
    for key in required_keys:
        if key not in contract:
            errors.append(f"skill_loading_disclosure missing key: {key}")

    disclosure = contract.get("disclosure", {})
    if not isinstance(disclosure, dict):
        errors.append("skill_loading_disclosure.disclosure must be an object")
    else:
        for key in ["when", "format", "must_include"]:
            if key not in disclosure:
                errors.append(f"skill_loading_disclosure.disclosure missing key: {key}")

    subagents = contract.get("subagents", {})
    if not isinstance(subagents, dict):
        errors.append("skill_loading_disclosure.subagents must be an object")
    else:
        for key in ["must_read", "must_disclose"]:
            if key not in subagents:
                errors.append(f"skill_loading_disclosure.subagents missing key: {key}")

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


def extract_frontmatter_keys(path: Path) -> set[str]:
    text = path.read_text()
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return set()

    keys: set[str] = set()
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key = line.split(":", 1)[0].strip()
        if key:
            keys.add(key)
    return keys


def validate_canonical_subagents(root: Path, policy: dict) -> tuple[list[str], Path | None]:
    errors: list[str] = []
    subagents = policy.get("subagents", {})
    if not subagents.get("enabled"):
        return errors, None

    directory = subagents.get("directory")
    if not directory:
        return ["subagents.enabled is true but subagents.directory is missing"], None

    subagent_root = root / directory
    if not subagent_root.is_dir():
        return [f"Canonical subagent directory missing: {subagent_root}"], subagent_root

    required = subagents.get("required", [])
    required_keys = subagents.get("frontmatter_keys", [])
    for name in required:
        agent_path = subagent_root / f"{name}.md"
        if not agent_path.exists():
            errors.append(f"Required subagent missing: {agent_path}")
            continue
        text = agent_path.read_text()
        keys = extract_frontmatter_keys(agent_path)
        if not keys:
            errors.append(f"Subagent missing frontmatter: {agent_path}")
            continue
        missing_keys = [key for key in required_keys if key not in keys]
        if missing_keys:
            errors.append(f"Subagent missing frontmatter keys {missing_keys}: {agent_path}")
        if "Skill loading (mandatory)" not in text:
            errors.append(f"Subagent missing mandatory skill-loading rule: {agent_path}")

    return errors, subagent_root


def validate_codex_subagent_config(codex_root: Path) -> list[str]:
    errors: list[str] = []
    config_path = codex_root / "config.toml"
    if not config_path.exists():
        errors.append(f"Codex config missing: {config_path}")
        return errors
    if tomllib is None:
        errors.append("tomllib unavailable; cannot validate Codex child_agents_md feature")
        return errors

    try:
        with open(config_path, "rb") as f:
            config = tomllib.load(f)
    except Exception as exc:  # pragma: no cover - config parse failure is runtime-dependent
        errors.append(f"Failed to parse Codex config {config_path}: {exc}")
        return errors

    features = config.get("features", {})
    if features.get("child_agents_md") is not True:
        errors.append(f"Codex child_agents_md feature must be enabled in {config_path}")

    return errors


def validate_peer_subagent_sync(root: Path, policy: dict, canonical_dir: Path | None) -> list[str]:
    errors: list[str] = []
    if canonical_dir is None:
        return errors

    required = policy.get("subagents", {}).get("required", [])
    peers = policy.get("sync", {}).get("peer_roots", [])
    canonical_dir = canonical_dir.resolve()
    canonical_agents = sorted(path for path in canonical_dir.iterdir() if path.is_file() and path.suffix == ".md")

    for peer in peers:
        subagents = peer.get("subagents", {})
        if not subagents.get("enabled"):
            continue

        peer_root = Path(peer.get("root", "")).expanduser()
        if not peer_root.exists():
            continue

        directory = subagents.get("directory")
        if not directory:
            errors.append(f"Peer {peer.get('name', '<unknown>')} has subagents enabled but no directory")
            continue

        peer_dir = peer_root / directory
        if not peer_dir.is_dir():
            errors.append(f"Peer subagent directory missing: {peer_dir}")
            continue

        for canonical_file in canonical_agents:
            peer_file = peer_dir / canonical_file.name
            if not peer_file.exists():
                errors.append(f"Peer subagent missing: {peer_file}")
                continue
            try:
                if peer_file.resolve() != canonical_file.resolve():
                    errors.append(
                        f"Peer subagent not synced to canonical source: {peer_file} -> {peer_file.resolve()} "
                        f"(expected {canonical_file})"
                    )
            except FileNotFoundError:
                errors.append(f"Peer subagent has broken target: {peer_file}")

        if peer.get("name") == "codex":
            errors.extend(validate_codex_subagent_config(peer_root))

    return errors


def validate_peer_skill_sync(root: Path, policy: dict, skills_root: Path) -> list[str]:
    errors: list[str] = []
    peers = policy.get("sync", {}).get("peer_roots", [])
    canonical_skills = sorted(
        entry for entry in skills_root.iterdir() if entry.is_dir() and not entry.name.startswith(".")
    )

    for peer in peers:
        peer_root = Path(peer.get("root", "")).expanduser()
        if not peer_root.exists():
            continue

        peer_skills_dir = peer_root / peer.get("skills_dir", policy.get("skills_dir", "skills"))
        if not peer_skills_dir.is_dir():
            errors.append(f"Peer skills directory missing: {peer_skills_dir}")
            continue

        for canonical_skill in canonical_skills:
            peer_skill = peer_skills_dir / canonical_skill.name
            if not peer_skill.exists():
                errors.append(f"Peer skill missing: {peer_skill}")
                continue
            try:
                if peer_skill.resolve() != canonical_skill.resolve():
                    errors.append(
                        f"Peer skill not synced to canonical source: {peer_skill} -> {peer_skill.resolve()} "
                        f"(expected {canonical_skill})"
                    )
            except FileNotFoundError:
                errors.append(f"Peer skill has broken target: {peer_skill}")

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
    all_errors.extend(validate_subagent_routing(policy))
    all_errors.extend(validate_ai_bridge_policy(policy))
    all_errors.extend(validate_skill_loading_disclosure(policy, skills_root))
    all_errors.extend(validate_skills_exist(policy, skills_root))
    subagent_errors, canonical_subagent_dir = validate_canonical_subagents(root, policy)
    all_errors.extend(subagent_errors)
    all_errors.extend(validate_peer_subagent_sync(root, policy, canonical_subagent_dir))
    all_errors.extend(validate_peer_skill_sync(root, policy, skills_root))
    all_errors.extend(check_codebase_map(project_root, policy))

    if all_errors:
        for e in all_errors:
            print(f"FAIL: {e}", file=sys.stderr)
        sys.exit(1)

    print("OK: agent policy valid")
    sys.exit(0)


if __name__ == "__main__":
    main()

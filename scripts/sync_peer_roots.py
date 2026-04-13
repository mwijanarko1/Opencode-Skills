#!/usr/bin/env python3
"""
Synchronize peer tool roots to the canonical ~/.agents source of truth.

This script manages:
- AGENTS.md and agent-policy.json symlinks
- shared subagent markdown files
- shared skill directories (excluding hidden/system entries)
"""
from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path


def get_policy_root() -> Path:
    env_root = os.environ.get("AGENTS_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    return Path(__file__).resolve().parent.parent


def load_policy(root: Path) -> dict:
    with open(root / "agent-policy.json", encoding="utf-8") as handle:
        return json.load(handle)


def ensure_dir(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)


def remove_path(target: Path) -> None:
    if target.is_symlink() or target.is_file():
        target.unlink()
        return
    if target.is_dir():
        shutil.rmtree(target)


def ensure_symlink(link_path: Path, source_path: Path) -> bool:
    ensure_dir(link_path.parent)
    if link_path.exists() or link_path.is_symlink():
        try:
            if link_path.resolve() == source_path.resolve() and link_path.is_symlink():
                return False
        except FileNotFoundError:
            pass
        remove_path(link_path)
    link_path.symlink_to(source_path)
    return True


def canonical_skill_dirs(skills_root: Path) -> list[Path]:
    return sorted(
        entry
        for entry in skills_root.iterdir()
        if entry.is_dir() and not entry.name.startswith(".")
    )


def canonical_agent_files(agents_root: Path) -> list[Path]:
    return sorted(
        entry
        for entry in agents_root.iterdir()
        if entry.is_file() and entry.suffix == ".md"
    )


def sync_peer(root: Path, policy: dict, peer: dict) -> list[str]:
    changes: list[str] = []
    peer_root = Path(peer["root"]).expanduser().resolve()
    if not peer_root.exists():
        return changes

    canonical_agents = root / policy["subagents"]["directory"]
    canonical_skills = Path(policy.get("skills_root", root / policy.get("skills_dir", "skills"))).resolve()

    agents_link = peer_root / "AGENTS.md"
    if ensure_symlink(agents_link, root / "AGENTS.md"):
        changes.append(f"{agents_link} -> {root / 'AGENTS.md'}")

    policy_link = peer_root / "agent-policy.json"
    if ensure_symlink(policy_link, root / "agent-policy.json"):
        changes.append(f"{policy_link} -> {root / 'agent-policy.json'}")

    subagent_cfg = peer.get("subagents", {})
    if subagent_cfg.get("enabled"):
        peer_agents_dir = peer_root / subagent_cfg["directory"]
        ensure_dir(peer_agents_dir)
        for source in canonical_agent_files(canonical_agents):
            target = peer_agents_dir / source.name
            if ensure_symlink(target, source):
                changes.append(f"{target} -> {source}")

    peer_skills_dir = peer_root / peer.get("skills_dir", policy.get("skills_dir", "skills"))
    ensure_dir(peer_skills_dir)
    managed_skill_names = {skill_dir.name for skill_dir in canonical_skill_dirs(canonical_skills)}
    for skill_dir in canonical_skill_dirs(canonical_skills):
        target = peer_skills_dir / skill_dir.name
        if ensure_symlink(target, skill_dir):
            changes.append(f"{target} -> {skill_dir}")

    for entry in peer_skills_dir.iterdir():
        if entry.name.startswith("."):
            continue
        if entry.name not in managed_skill_names:
            continue

    return changes


def main() -> int:
    root = get_policy_root()
    policy = load_policy(root)
    all_changes: list[str] = []
    for peer in policy.get("sync", {}).get("peer_roots", []):
        all_changes.extend(sync_peer(root, policy, peer))

    if all_changes:
        print("SYNCED:")
        for change in all_changes:
            print(f"- {change}")
    else:
        print("SYNCED: no changes needed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

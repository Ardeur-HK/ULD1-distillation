#!/usr/bin/env python3
"""Read-only comparison of imported snapshots with their upstream Git blobs."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCES = (
    ("llm-recipes", "ab6e79800d28a1820348d72fc43ad964bb51ac29"),
    ("llm-distillation", "70e728f33b15cdd8c15d09eec53b590ebf034907"),
)
ENV = dict(os.environ, GIT_NO_LAZY_FETCH="1", GIT_ALLOW_PROTOCOL="",
           GIT_TERMINAL_PROMPT="0", GIT_OPTIONAL_LOCKS="0",
           GIT_NO_REPLACE_OBJECTS="1")


def git(*args):
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, env=ENV, stderr=subprocess.PIPE)


def entries(ref):
    result = {}
    for record in git("ls-tree", "-r", "-z", ref).split(b"\0"):
        if not record:
            continue
        metadata, name = record.split(b"\t", 1)
        mode, kind, oid = metadata.decode("ascii").split()
        if kind != "blob":
            raise ValueError("unsupported non-blob entry in " + ref)
        path = name.decode("utf-8")
        if Path(path).is_absolute() or ".." in Path(path).parts:
            raise ValueError("unsafe path in Git tree")
        result[path] = (mode, oid)
    return result


def lfs_identity(blob):
    if not blob.startswith(b"version https://git-lfs.github.com/spec/v1\n"):
        return None
    oid = re.search(rb"^oid sha256:([0-9a-f]{64})$", blob, re.MULTILINE)
    size = re.search(rb"^size ([0-9]+)$", blob, re.MULTILINE)
    if not oid or not size:
        raise ValueError("invalid Git LFS pointer")
    return oid.group(1).decode("ascii"), int(size.group(1))


def check_component(prefix, source):
    expected = entries(source)
    current = entries("HEAD:" + prefix)
    tracked_differences = sorted(
        name for name in set(expected) | set(current)
        if expected.get(name) != current.get(name))
    directory = ROOT / prefix
    working_paths = {
        path.relative_to(directory).as_posix()
        for path in directory.rglob("*") if path.is_file() or path.is_symlink()
    }
    extra_paths = sorted(working_paths - set(expected))
    mismatches = []
    pointers_only = 0
    payloads_verified = 0
    for name, (mode, oid) in expected.items():
        original = git("cat-file", "blob", oid)
        path = directory / name
        if mode == "120000":
            actual = os.fsencode(os.readlink(path)) if path.is_symlink() else None
        else:
            actual = path.read_bytes() if path.is_file() and not path.is_symlink() else None
        pointer = lfs_identity(original)
        if actual == original:
            pointers_only += int(pointer is not None)
        elif pointer and actual is not None:
            digest, size = pointer
            if len(actual) == size and hashlib.sha256(actual).hexdigest() == digest:
                payloads_verified += 1
            else:
                mismatches.append(name)
        else:
            mismatches.append(name)
    return {
        "component": prefix, "upstream_commit": source,
        "files_compared": len(expected),
        "tracked_differences": tracked_differences,
        "working_file_mismatches": mismatches,
        "unexpected_working_files": extra_paths,
        "lfs_pointers_without_payload_verification": pointers_only,
        "materialized_lfs_payloads_verified": payloads_verified,
    }


def main():
    try:
        head = git("rev-parse", "HEAD").decode("ascii").strip()
        components = [check_component(*source) for source in SOURCES]
        ok = all(not any(component[key] for key in (
            "tracked_differences", "working_file_mismatches",
            "unexpected_working_files")) for component in components)
        print(json.dumps({"ok": ok, "head": head, "components": components,
                          "training_or_benchmark_executed": False}, indent=2))
        return 0 if ok else 1
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        # Missing local objects fail without a network fetch or repair attempt.
        print(json.dumps({"ok": False, "status": "insufficient_local_evidence",
                          "error": type(exc).__name__,
                          "detail": "A complete local Git history and readable imported files are required."}),
              file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

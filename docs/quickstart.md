# Quick Start: Inspect Sources

This entry point checks source provenance locally. It needs **Python 3.9+ and Git**, with no training packages, GPU, model weights, or credentials.

## Clone and check

Use a full clone so the imported upstream history is available. Skipping Git LFS downloads is sufficient for the source check:

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/Ardeur-HK/ULD1-distillation.git
cd ULD1-distillation
python3 scripts/verify_upstream.py
```

The checker reads the pinned upstream commits and current imported trees from the local Git object database, compares paths, file modes, and blob IDs, then compares working files with their source blobs. Missing history or changed files cause a nonzero exit; the checker does not fetch missing objects or modify files.

For an unchanged checkout, expect `"ok": true` and two component summaries:

| Component | Files compared | Tracked differences | Working-file mismatches |
| --- | ---: | ---: | ---: |
| `llm-recipes` | 32 | 0 | 0 |
| `llm-distillation` | 294 | 0 | 0 |

The JSON also reports unexpected files and Git LFS pointers. A pointer match verifies the tracked pointer, not an absent dataset payload. When an LFS payload is already present, its size and SHA-256 are checked against the pointer. ZIP downloads and shallow clones may lack the history needed for this check.

This verifies imported source identity. It does not validate the algorithm, dataset rights, benchmark scores, or completion of a training run.

## Training status

Start with the preserved [training README](../llm-recipes/README.md) and [data/prompting project](../llm-distillation/README.md). Their entry points and examples remain upstream material. This archive has no verified combined training setup or pinned dependency environment.

The example student/teacher pair is `EleutherAI/pythia-410m-deduped` / `meta-llama/Llama-2-7b-chat-hf`. The [student defaults](../llm-recipes/configs/training.py) and [teacher defaults](../llm-recipes/configs/distillation.py) instead name `meta-llama/Llama-2-7b-hf`, with distillation disabled in the training defaults. Upstream loaders also assume specific local directory layouts.

Before attempting training, resolve dependency compatibility, dataset availability and permissions, model access and terms, and the exact teacher/student/tokenizer configuration. Bundled results remain attributed to upstream. See [contributions and source boundaries](contributions.md).

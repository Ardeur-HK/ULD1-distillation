# Cross-Tokenizer Distillation Study Archive

An exploratory collection of upstream LLM training and dataset tools, assembled while studying knowledge distillation and model merging.

The two imported directories are unchanged upstream snapshots. Bundled datasets, predictions, confidence files, and benchmark results came with those snapshots; they are **upstream artifacts, not my experimental results**. This archive does not document a completed personal ULD training run or a model-merging experiment.

## Contents and attribution

| Directory | Upstream source | Imported commit |
| --- | --- | --- |
| [`llm-recipes/`](llm-recipes/) | [Nicolas-BZRD/llm-recipes](https://github.com/Nicolas-BZRD/llm-recipes): training and ULD-style loss implementation | [`ab6e798`](https://github.com/Nicolas-BZRD/llm-recipes/commit/ab6e79800d28a1820348d72fc43ad964bb51ac29) |
| [`llm-distillation/`](llm-distillation/) | [Nicolas-BZRD/llm-distillation](https://github.com/Nicolas-BZRD/llm-distillation): dataset, prompting, and benchmark materials | [`70e728f`](https://github.com/Nicolas-BZRD/llm-distillation/commit/70e728f33b15cdd8c15d09eec53b590ebf034907) |

The method is described in Boizard et al., [*Towards Cross-Tokenizer Distillation: the Universal Logit Distillation Loss for LLMs*](https://arxiv.org/abs/2402.12030). The original citation is preserved in the [upstream training README](llm-recipes/README.md#citation).

## Inspect the archive

With Python 3.9+ and Git, run from a full clone:

```bash
python3 scripts/verify_upstream.py
```

This offline check compares all imported Git blobs with the pinned upstream commits, then checks the working files. It does not run training or benchmarks. See the [Quick Start](docs/quickstart.md) for expected output and limitations, and [contributions](docs/contributions.md) for the personal contribution boundary.

The [source-provenance CI](.github/workflows/source-provenance.yml) runs the same check with full Git history and skips LFS payload downloads.

The upstream README's example uses a Pythia-410M student and Llama-2-7B-Chat teacher. Code defaults instead name Llama-2-7B on both sides and leave distillation disabled; neither configuration establishes a personal training run.

## Licensing and reuse

No explicit license file was found in either imported snapshot. This collection does not grant a blanket license to upstream code, models, data, or results. Confirm the relevant authors' terms and the individual model/data permissions before reuse or redistribution. Training setup remains an upstream workflow with unresolved dependency and permission requirements; see the [training notes](docs/quickstart.md#training-status).

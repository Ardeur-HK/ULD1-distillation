# Contributions and Upstream Boundaries

## Personal scope

I assembled this exploratory archive while studying LLM distillation and model merging. My recorded contribution here is importing the upstream projects with their history, organizing the entry documentation, and adding a local source-provenance check.

The imported implementation, datasets, predictions, confidence files, and benchmark results are upstream material. They do not demonstrate a personal algorithm implementation, a completed ULD reproduction, or a completed model-merging experiment. No separate personal training result or checkpoint is documented in this archive.

## Pinned sources

| Imported directory | Original repository and complete commit | Local import commit |
| --- | --- | --- |
| `llm-recipes/` | [Nicolas-BZRD/llm-recipes @ ab6e79800d28a1820348d72fc43ad964bb51ac29](https://github.com/Nicolas-BZRD/llm-recipes/tree/ab6e79800d28a1820348d72fc43ad964bb51ac29) | [`2c12e9a`](https://github.com/Ardeur-HK/ULD1-distillation/commit/2c12e9ac60b3d619fcf34cf0e4e07d013ecd1f04) |
| `llm-distillation/` | [Nicolas-BZRD/llm-distillation @ 70e728f33b15cdd8c15d09eec53b590ebf034907](https://github.com/Nicolas-BZRD/llm-distillation/tree/70e728f33b15cdd8c15d09eec53b590ebf034907) | [`bdca396`](https://github.com/Ardeur-HK/ULD1-distillation/commit/bdca3960767f3f8b578d25db965a84d8582c9796) |

The original root README was added in [`d65380b`](https://github.com/Ardeur-HK/ULD1-distillation/commit/d65380b1dc6fbbe63895d197a8e299cc939625b3). The two imported trees contain 32 and 294 files respectively; the [offline checker](../scripts/verify_upstream.py) compares their actual blobs and working files against these upstream commits.

The ULD loss and teacher/student training code in [`llm-recipes/models/distillation_model.py`](../llm-recipes/models/distillation_model.py) are upstream implementations. Cite Nicolas Boizard, Kevin El Haddad, Céline Hudelot, and Pierre Colombo, [*Towards Cross-Tokenizer Distillation: the Universal Logit Distillation Loss for LLMs*](https://arxiv.org/abs/2402.12030), when referring to that method. The upstream README also records its Llama recipes ancestry.

In particular, [`llm-distillation/benchmark/`](../llm-distillation/benchmark/) and [`llm-distillation/datasets/`](../llm-distillation/datasets/) were imported with the source. Their contents retain upstream provenance; this archive does not relabel them as personal measurements or certify their independent reproducibility.

## Permissions and documentation

No explicit license file was found in either pinned snapshot. Preserve existing authorship and source information, and obtain or confirm applicable permissions for code, benchmark material, datasets, and model use. The root documentation does not relicense the collection.

This documentation update was AI-assisted. The accompanying verification checks source identity only; no training or benchmark was executed for the update.

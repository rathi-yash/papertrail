# LoRA paper — manual prototype notes

Source: PRD.md Section 8 (Validation / Prototyping Findings)

- Paper: "LoRA: Low-Rank Adaptation of Large Language Models" (arXiv:2106.09685)
- Repo: https://github.com/microsoft/LoRA
- Paper-side ground truth: Table 11 (Section D.3, GPT-2 hyperparameters for E2E NLG)
- Repo-side ground truth: `examples/NLG/README.md` reproduction command

## Result

Near-perfect match on all fields present in both. One genuine gap found:
the repo's README command pins `--random_seed 110`, which is not stated
anywhere in the paper's Table 11. This is exactly the class of finding
the tool should surface: a repo-side detail relevant to reproduction
that the paper doesn't mention.

## Field-by-field (see expected_output.json for the structured form)

| Field | Paper (Table 11) | Repo (README command) | Status |
|---|---|---|---|
| Batch size | 8 | `--train_batch_size 8` | matched |
| Learning rate | 0.0002 | `--lr 0.0002` | matched |
| Weight decay | 0.01 | `--weight_decay 0.01` | matched |
| Epochs | 5 | `--max_epoch 5` | matched |
| Warmup steps | 500 | `--warmup_step 500` | matched |
| LoRA rank | 4 (rq = rv = 4) | `--lora_dim 4` | matched (name differs: "Adaptation" -> `lora_dim`) |
| LoRA alpha | 32 | `--lora_alpha 32` | matched |
| Label smoothing | 0.1 | `--label_smooth 0.1` | matched |
| Dropout | 0.1 ("Dropout Prob") | `--lora_dropout 0.1` | matched (fuzzy name match needed) |
| Random seed | not stated | `--random_seed 110` | **repo-only, flag this** |

This file is the source for expected_output.json and should be kept in
sync if the manual analysis is ever redone or corrected.

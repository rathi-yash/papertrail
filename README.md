# PaperTrail

I built this because reproducing ML papers is a real, common pain: hyperparameters go unstated, repo defaults drift from what the paper says, dataset links rot, and you usually only find out after burning hours on a broken run. PaperTrail points at a paper and its linked GitHub repo, cross-references what the paper claims against what the repo actually does, and gives you a confidence-rated report of what's missing before you start.

This isn't a replacement for research on reproducibility, it's a practical companion to it. Related academic work like ReproRepo, PaperBench, Paper2Code, and "What Papers Don't Tell You" treats this as a benchmark problem for evaluating frontier agents at scale. This tool is the thing you actually open and run when you're stuck on one specific paper today.

See `PRD.md` for the full spec.

## Status

Early build, Stage 1 (gap finder) in progress.

## Install

TODO: once packaged, `pip install papertrail`

## Usage

```
papertrail check <arxiv-url> <repo-url>
```

## Bring your own key

Set `ANTHROPIC_API_KEY` in your environment for the best extraction quality. Without it, the tool falls back to a local open-weight model, free, but weaker on messy or ambiguous paper text. See `.env.example`.

## License

TODO

# Upstream Skill Sources

This repo includes upstream skills managed as git submodules. Their original source repos are listed below.

## Submodules

| Skill(s) | Plugin | Source Repo | Submodule Path |
|-----------|--------|------------|----------------|
| deep-research, academic-paper, academic-paper-reviewer, academic-pipeline | academic-pipeline | https://github.com/Imbad0202/academic-research-skills | `plugins/academic-pipeline` |
| paper-mentor | paper-pipeline | https://github.com/sellerbubble/paper-mentor-skill | `plugins/paper-pipeline/skills/paper-mentor` |
| paper-reader | paper-pipeline | https://github.com/AIED007/paper-reader | `plugins/paper-pipeline/skills/paper-reader` |

## How to Update from Upstream

```bash
# Update all submodules to latest
git submodule update --remote --merge

# Or update a specific one
cd plugins/academic-pipeline
git pull origin main
cd ../..

# Commit the updated references
git add .
git commit -m "chore: sync upstream skills"
git push
```

## How to Clone This Repo (includes submodules)

```bash
git clone --recurse-submodules https://github.com/zenggy202406/research-skills.git
```

Or if already cloned without submodules:

```bash
git submodule update --init --recursive
```

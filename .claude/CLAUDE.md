# CLAUDE.md

This file provides guidance to AI coding agents working with code in this repository.

## Project Overview

A single-page primer that teaches OpenTelemetry concepts progressively. Each entry builds on the last, following Vygotskian constructivist principles. No interactivity — just clear, well-structured prose.

Live at otel-primer.mreider.com, hosted via GitHub Pages.

## Core Principles

1. **Constructivist flow**: Each concept introduces exactly one new idea and references only concepts already established above it. Never N+1 — always N.
2. **Simple language**: Explain concepts in the simplest accurate terms. Concrete before abstract. Start with what you can observe, then name it.
3. **No zen, no poetry**: This is a primer, not a meditation. Direct, clear descriptions only.
4. **Technical accuracy**: Never invent details about OpenTelemetry. Only use information from specifications and documentation. Flag contradictions immediately.
5. **Print-inspired design**: The CSS follows the aesthetic of a printed dictionary — Crimson Text serif, white background, clean typography. No animations, no dark mode, no glassmorphism.
6. **Cite sources**: Reference OpenTelemetry specification documents or documentation when making technical claims.

## Repository Structure

```
index.html    # The entire primer — single page
style.css     # Print-inspired typography
CNAME         # Custom domain for GitHub Pages
```

## Adding New Content

When the user proposes a new concept, **do not just write it**. First, have a Q&A conversation covering:

1. **What is the concept?** Clarify the idea and make sure we agree on scope. What does it teach? What question does it answer?
2. **Where does it go?** Which existing entries does it depend on? Which entries depend on ideas it would introduce? Find the right slot in the sequence.
3. **Does it need to be broken up?** If the concept requires understanding two new ideas at once, it must be split into separate entries — always N, never N+1.
4. **What breaks?** Does inserting it require refactoring existing entries? Do later entries now need to reference it? Does the TOC, numbering, or phase structure need updating?
5. **What example or illustration does it need?** Every entry gets a concrete `.ex` block, SVG illustration, or definition list.

Only after alignment on all five questions should we write the entry and update the primer.

## Important Reminders

- **Git identity**: Always use mreider@gmail.com for all git operations
- **One page**: Everything lives in index.html. Do not split into multiple pages.
- **No JavaScript**: This is a static document. No interactivity, no animations.
- **Concept order matters**: The entries are carefully sequenced. Do not reorder without verifying the constructivist dependency chain — each entry may only reference concepts introduced before it.
- **No em dashes**: Use en dashes (`&ndash;`) with spaces around them, never em dashes (`&mdash;`). This applies to all content in index.html.

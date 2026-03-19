# CLAUDE.md

This file provides guidance to AI coding agents working with code in this repository.

## Project Overview

A single-page reference site that teaches OpenTelemetry concepts progressively. 28 entries, each building on the last, following Vygotskian constructivist principles. No interactivity — just clear, well-structured prose.

Live at otel-ref.mreider.com, hosted via GitHub Pages.

## Core Principles

1. **Constructivist flow**: Each concept introduces exactly one new idea and references only concepts already established above it. Never N+1 — always N.
2. **Simple language**: Explain concepts in the simplest accurate terms. Concrete before abstract. Start with what you can observe, then name it.
3. **No zen, no poetry**: This is a reference, not a meditation. Direct, clear descriptions only.
4. **Technical accuracy**: Never invent details about OpenTelemetry. Only use information from specifications and documentation. Flag contradictions immediately.
5. **Print-inspired design**: The CSS follows the aesthetic of a printed dictionary — Crimson Text serif, white background, clean typography. No animations, no dark mode, no glassmorphism.
6. **Cite sources**: Reference OpenTelemetry specification documents or documentation when making technical claims.

## Repository Structure

```
index.html    # The entire reference — single page
style.css     # Print-inspired typography
CNAME         # Custom domain for GitHub Pages
```

## Important Reminders

- **Git identity**: Always use mreider@gmail.com for all git operations
- **One page**: Everything lives in index.html. Do not split into multiple pages.
- **No JavaScript**: This is a static document. No interactivity, no animations.
- **Concept order matters**: The 28 entries are carefully sequenced. Do not reorder without verifying the constructivist dependency chain — each entry may only reference concepts introduced before it.
- **No em dashes**: Use en dashes (`&ndash;`) with spaces around them, never em dashes (`&mdash;`). This applies to all content in index.html.

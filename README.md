# Skip to Review - Anki Add-On

## Build
### Nix
- `nix build`

To get a shell with all development tools: `nix shell`

## Other systems
### Requirements
- `zip`
- `goredo`
- If you build on another system, send a patch with build instructions

To build: `redo ./skip-to-review.ankiaddon`

And the add-on file will be at that path.

## Installation
- In Anki, select Add-ons
- "Install from file..."
- `./result/skip-to-review.ankiaddon`

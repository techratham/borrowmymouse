# BorrowMyMouse

Free remote desktop for Windows and macOS. No accounts, no session limits, no "commercial use detected" popups. Rebranded fork of [RustDesk](https://github.com/rustdesk/rustdesk) (AGPL-3.0).

## Downloads (per release)

| File | Platform | Kind |
|---|---|---|
| `BorrowMyMouse-<ver>-windows-x64.exe` | Windows 10/11 | Portable. Runs without installing; has a built-in "Install" button |
| `BorrowMyMouse-<ver>-windows-x64.msi` | Windows 10/11 | Installer (silent install: `msiexec /i file.msi /qn`) |
| `BorrowMyMouse-<ver>-macos-aarch64.dmg` | macOS 12.3+ Apple Silicon | Installer (drag to Applications) |
| `BorrowMyMouse-<ver>-macos-x86_64.dmg` | macOS 10.14+ Intel | Installer |
| `BorrowMyMouse-<ver>-macos-*-portable.zip` | macOS | Portable `.app`; run from anywhere |

The macOS builds are ad-hoc signed, not notarized. On first launch: right-click the app → Open, or run `xattr -cr /Applications/BorrowMyMouse.app`.

## Connectivity

Uses RustDesk's free public ID/relay servers by default. To switch to your own server later: Settings → Network → ID/Relay server.

## Branding

All branding lives in `brand/`:

- `brand/apply.py` is idempotent. It patches app name, bundle ID, Windows version info and icons. CI runs it after checkout, so pulling upstream changes and re-running it is the whole upgrade path. It fails loudly if upstream moves an anchor.
- `brand/make_icons.py` regenerates `brand/out/*` (PNG, ICO, ICNS, SVG). It needs Pillow.

## Build

Builds run in GitHub Actions (`.github/workflows/borrowmymouse.yml`). Windows binaries can't be built on a Mac.

- Actions → "BorrowMyMouse release" → Run workflow: the artifacts appear on the run.
- Push a `v*` tag: the same build, plus a GitHub Release with all files and `SHA256SUMS.txt`.

## License

AGPL-3.0, inherited from RustDesk. Anyone you distribute binaries to is entitled to the source, so keep this repo public and keep the RustDesk attribution in the About screen.

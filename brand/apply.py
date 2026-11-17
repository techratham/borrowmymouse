#!/usr/bin/env python3
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRAND = Path(__file__).resolve().parent

NAME = "BorrowMyMouse"
LOWER = NAME.lower()
BUNDLE_ID = "com.techratham.borrowmymouse"
COMPANY = "TechRatham"
COPYRIGHT = "Copyright © 2026 TechRatham. Free forever. AGPL-3.0, based on RustDesk."

PATCHES = [
    ("libs/hbb_common/src/config.rs", [
        ('APP_NAME: RwLock<String> = RwLock::new("RustDesk".to_owned())',
         f'APP_NAME: RwLock<String> = RwLock::new("{NAME}".to_owned())'),
    ]),
    ("Cargo.toml", [
        ('description = "RustDesk Remote Desktop"', f'description = "{NAME} Remote Desktop"'),
        ('LegalCopyright = "Copyright © 2026 Purslane Tech Pte. Ltd. All rights reserved."', f'LegalCopyright = "{COPYRIGHT}"'),
        ('ProductName = "RustDesk"', f'ProductName = "{NAME}"'),
        ('FileDescription = "RustDesk Remote Desktop"', f'FileDescription = "{NAME} Remote Desktop"'),
        ('OriginalFilename = "rustdesk.exe"', f'OriginalFilename = "{NAME}.exe"'),
        ('name = "RustDesk"\nidentifier = "com.carriez.rustdesk"', f'name = "{NAME}"\nidentifier = "{BUNDLE_ID}"'),
    ]),
    ("libs/portable/Cargo.toml", [
        ('description = "RustDesk Remote Desktop"', f'description = "{NAME} Remote Desktop"'),
        ('LegalCopyright = "Copyright © 2026 Purslane Tech Pte. Ltd. All rights reserved."', f'LegalCopyright = "{COPYRIGHT}"'),
        ('ProductName = "RustDesk"', f'ProductName = "{NAME}"'),
        ('OriginalFilename = "rustdesk.exe"', f'OriginalFilename = "{NAME}.exe"'),
        ('FileDescription = "RustDesk Remote Desktop"', f'FileDescription = "{NAME} Remote Desktop"'),
    ]),
    ("flutter/macos/Runner/Configs/AppInfo.xcconfig", [
        ("PRODUCT_NAME = RustDesk", f"PRODUCT_NAME = {NAME}"),
        ("PRODUCT_BUNDLE_IDENTIFIER = com.carriez.flutterHbb", f"PRODUCT_BUNDLE_IDENTIFIER = {BUNDLE_ID}"),
        ("PRODUCT_COPYRIGHT = Copyright © 2026 Purslane Tech Pte. Ltd. All rights reserved.", f"PRODUCT_COPYRIGHT = {COPYRIGHT}"),
    ]),
    ("flutter/macos/Runner.xcodeproj/project.pbxproj", [
        ("PRODUCT_BUNDLE_IDENTIFIER = com.carriez.rustdesk;", f"PRODUCT_BUNDLE_IDENTIFIER = {BUNDLE_ID};"),
    ]),
    ("flutter/macos/Runner/Info.plist", [
        ("<string>com.carriez.rustdesk</string>", f"<string>{BUNDLE_ID}</string>"),
        ("<string>rustdesk</string>", f"<string>{LOWER}</string>"),
    ]),
    ("flutter/windows/runner/Runner.rc", [
        ('VALUE "CompanyName", "Purslane Tech Pte. Ltd."', f'VALUE "CompanyName", "{COMPANY}"'),
        ('VALUE "FileDescription", "RustDesk Remote Desktop"', f'VALUE "FileDescription", "{NAME} Remote Desktop"'),
        ('VALUE "InternalName", "rustdesk"', f'VALUE "InternalName", "{LOWER}"'),
        ('VALUE "LegalCopyright", "Copyright © 2026 Purslane Tech Pte. Ltd. All rights reserved."', f'VALUE "LegalCopyright", "{COPYRIGHT}"'),
        ('VALUE "OriginalFilename", "rustdesk.exe"', f'VALUE "OriginalFilename", "{NAME}.exe"'),
        ('VALUE "ProductName", "RustDesk"', f'VALUE "ProductName", "{NAME}"'),
    ]),
    ("flutter/windows/runner/main.cpp", [
        ('std::wstring app_name = L"RustDesk";', f'std::wstring app_name = L"{NAME}";'),
    ]),
    ("build.py", [
        ("Products/Release/RustDesk.app/Contents/MacOS/')", f"Products/Release/{NAME}.app/Contents/MacOS/')"),
    ]),
]

ICONS = {
    "icon-1024.png": ["res/icon.png", "res/mac-icon.png"],
    "icon-128.png": ["res/128x128.png"],
    "icon-256.png": ["res/128x128@2x.png"],
    "icon-64.png": ["res/64x64.png"],
    "icon-32.png": ["res/32x32.png"],
    "icon.ico": ["res/icon.ico", "res/tray-icon.ico", "flutter/windows/runner/resources/app_icon.ico"],
    "AppIcon.icns": ["flutter/macos/Runner/AppIcon.icns"],
    "icon.svg": ["flutter/assets/icon.svg", "res/logo.svg", "res/scalable.svg"],
}


def patch():
    errors = []
    for rel, pairs in PATCHES:
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        orig = text
        for old, new in pairs:
            if old in text:
                text = text.replace(old, new)
            elif new not in text:
                errors.append(f"{rel}: anchor not found: {old!r}")
        if text != orig:
            path.write_text(text, encoding="utf-8")
            print(f"patched {rel}")
    return errors


def icons():
    out = BRAND / "out"
    if not (out / "icon.ico").exists():
        import make_icons
        make_icons.main(out)
    for src, dests in ICONS.items():
        for d in dests:
            dest = ROOT / d
            if dest.parent.exists():
                shutil.copyfile(out / src, dest)


if __name__ == "__main__":
    sys.path.insert(0, str(BRAND))
    errs = patch()
    icons()
    if errs:
        print("\n".join(errs), file=sys.stderr)
        sys.exit(1)
    print(f"{NAME} branding applied")

#!/usr/bin/env python3
"""
TLSA 한글패치 ZIP 빌더
게임 루트에 덮어쓰기하면 바로 적용되는 구조로 패키징
"""
import os
import zipfile
import sys

sys.stdout.reconfigure(encoding='utf-8')

SOURCE = "C:/Users/admin/Projects/hanpaemo/thelast/thalast"
OUT_ZIP = "C:/Users/admin/Projects/hanpaemo/thelast/한패모_TLSA-한글패치.zip"

# 게임 루트에 직접 들어가는 파일/폴더
ROOT_ITEMS = [
    "winhttp.dll",
    "doorstop_config.ini",
    ".doorstop_version",
    "nanumgothic",
    "dohyeon",
    "dotnet",
]

# BepInEx 하위에서 포함할 폴더 (interop/cache/unity-libs/patchers 제외)
BEPINEX_SUBDIRS = [
    "core",
    "plugins",
    "config",
    "Translation",
]

README = """The Last Stand: Aftermath - 한글패치 v1.0
=========================================

[제작]
- 한패모 (https://hanpaemo.blogspot.com)
- 대상: 모든 NPC 대화, 아이템/스킬/퀘스트 UI, 생존 가이드/일기/메모 등 게임 내 텍스트

[설치 방법]
1. 이 zip 파일 안의 모든 파일/폴더를 게임 설치 폴더에 덮어쓰기
   (기본 경로: Steam\\steamapps\\common\\The Last Stand Aftermath)
2. 게임 실행
3. 첫 실행 시 BepInEx 초기화로 1~2분 로딩이 길어질 수 있습니다 (정상)

[번역 범위]
- NPC 전체 대화 (Radioman, Amy, Hector, Buzzard, Mikhail, Lord Zee, Jack Davis 등)
- 아이템/스킬/돌연변이/퀘스트/UI 텍스트
- 인게임 책/메모/일기 (생존 가이드, HERC 문서, 의사 일기, 랜덤 메모 17종 등)

[주의사항]
- BepInEx + XUnity.AutoTranslator 포함 (별도 설치 불필요)
- 기존에 BepInEx가 설치된 경우 덮어쓰기하면 됩니다
- 게임 업데이트 시 번역이 깨질 수 있습니다

[문의]
번역 오류나 누락이 있으면 알려주세요.
- GitHub Issues: https://github.com/hanpaemo/tlsa-korean-patch/issues
- 블로그: https://hanpaemo.blogspot.com

🎮 다른 인디게임 한글패치도 찾아보세요 → https://hanpaemo.blogspot.com
"""

def add_dir(zf, src_path, zip_path):
    """폴더를 재귀적으로 zip에 추가"""
    for root, dirs, files in os.walk(src_path):
        for file in files:
            full_path = os.path.join(root, file)
            rel = os.path.relpath(full_path, src_path)
            arc_name = os.path.join(zip_path, rel).replace("\\", "/")
            zf.write(full_path, arc_name)

with zipfile.ZipFile(OUT_ZIP, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
    # README 추가
    zf.writestr("설치방법.txt", README.encode('utf-8').decode('utf-8'))
    print("Added: 설치방법.txt")

    # 게임 루트 파일/폴더 추가
    for item in ROOT_ITEMS:
        src = os.path.join(SOURCE, item)
        if not os.path.exists(src):
            print(f"SKIP (not found): {item}")
            continue
        if os.path.isfile(src):
            zf.write(src, item)
            size = os.path.getsize(src) / 1024 / 1024
            print(f"Added file: {item} ({size:.1f} MB)")
        else:
            add_dir(zf, src, item)
            count = sum(len(files) for _, _, files in os.walk(src))
            print(f"Added dir: {item}/ ({count} files)")

    # BepInEx 하위 폴더 추가
    bepinex_src = os.path.join(SOURCE, "BepInEx")
    for subdir in BEPINEX_SUBDIRS:
        src = os.path.join(bepinex_src, subdir)
        if not os.path.exists(src):
            print(f"SKIP (not found): BepInEx/{subdir}")
            continue
        zip_path = f"BepInEx/{subdir}"
        add_dir(zf, src, zip_path)
        count = sum(len(files) for _, _, files in os.walk(src))
        print(f"Added dir: BepInEx/{subdir}/ ({count} files)")

# 결과 출력
size_mb = os.path.getsize(OUT_ZIP) / 1024 / 1024
print(f"\n완료! 출력 파일: {OUT_ZIP}")
print(f"파일 크기: {size_mb:.1f} MB")

# 내용물 목록 확인
print("\n--- ZIP 내용물 (상위 항목) ---")
with zipfile.ZipFile(OUT_ZIP, 'r') as zf:
    seen = set()
    for name in sorted(zf.namelist()):
        top = name.split('/')[0]
        if top not in seen:
            seen.add(top)
            print(f"  {top}/") if '/' in name else print(f"  {name}")

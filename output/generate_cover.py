#!/usr/bin/env python3
"""
표지 이미지 생성 — 오픈클로 101가지 활용법
메인안 A (디지털 워커): output/images/cover_a.png
대안 B (101 임팩트): output/images/cover_b.png
전자책 규격: 1600×2560px (1:1.6 비율)
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch, Circle
import numpy as np
import os

# ─── 경로 ───
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(BASE_DIR, "output", "images")
font_path = os.path.join(BASE_DIR, "font", "Pretendard-Regular.otf")
bold_path = os.path.join(BASE_DIR, "font", "Pretendard-Bold.otf")

# ─── 색상 ───
# 메인안 A
A_BG_TOP    = '#0D1B2A'
A_BG_BOT    = '#1B2A4A'
A_GOLD      = '#C08B2D'
A_STEEL     = '#4A9EDB'
A_WHITE     = '#FFFFFF'
A_GRAY      = '#B0BEC5'

# 대안 B
B_TEAL      = '#0D9488'
B_NAVY      = '#1F4E79'
B_WHITE     = '#FFFFFF'
B_GRAY      = '#6B7280'
B_TEAL_LIGHT= '#CCFBF1'


def setup_font():
    if os.path.exists(font_path):
        fm.fontManager.addfont(font_path)
    if os.path.exists(bold_path):
        fm.fontManager.addfont(bold_path)
    available = {f.name for f in fm.fontManager.ttflist}
    for candidate in ['Pretendard', 'AppleGothic', 'NanumGothic', 'Malgun Gothic']:
        if candidate in available:
            plt.rcParams['font.family'] = candidate
            print(f"  폰트: {candidate}")
            return candidate
    return 'DejaVu Sans'


def draw_node(ax, cx, cy, r, color, label, label_size=9, label_color='white'):
    """허브 노드 그리기"""
    circle = Circle((cx, cy), r, color=color, zorder=5)
    ax.add_patch(circle)
    # 테두리
    circle_border = Circle((cx, cy), r, fill=False, edgecolor='white', lw=1.5, alpha=0.4, zorder=6)
    ax.add_patch(circle_border)
    ax.text(cx, cy, label, ha='center', va='center',
            fontsize=label_size, color=label_color, weight='bold', zorder=7,
            multialignment='center')


def cover_a():
    """메인안 A — 디지털 워커 컨셉 (네이비 배경 + 에이전트 네트워크)"""
    # 전자책 비율 1:1.6 → 10×16 인치 @ 160dpi = 1600×2560px
    fig, ax = plt.subplots(figsize=(10, 16), dpi=160)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 16)
    ax.axis('off')

    # ── 배경 그라데이션 (상단 어둡게 → 하단 약간 밝게) ──
    for i in range(320):
        t = i / 320
        r = int(0x0D + (0x1B - 0x0D) * t)
        g = int(0x1B + (0x2A - 0x1B) * t)
        b = int(0x2A + (0x4A - 0x2A) * t)
        color = f'#{r:02X}{g:02X}{b:02X}'
        ax.add_patch(patches.Rectangle((0, i * 16/320), 10, 16/320,
                                        facecolor=color, edgecolor='none', zorder=0))

    # ── 상단 장식선 ──
    ax.plot([0.5, 9.5], [15.4, 15.4], color=A_GOLD, lw=2, zorder=3)
    ax.plot([0.5, 9.5], [15.2, 15.2], color=A_STEEL, lw=0.8, alpha=0.6, zorder=3)

    # ── 중앙 허브 (에이전트 아이콘) ──
    hub_cx, hub_cy = 5.0, 10.2
    draw_node(ax, hub_cx, hub_cy, 1.1, A_STEEL, '하나\n(에이전트)', label_size=13)

    # ── 방사형 연결선 + 외부 노드 ──
    outer_nodes = [
        (3.0, 12.5, A_GOLD,   '#\n이메일'),
        (6.5, 12.8, '#2E75B6', '캘린더'),
        (2.2, 10.2, '#059669', '슬랙'),
        (7.8, 10.2, '#7C3AED', '리포트'),
        (3.0, 7.8,  '#DC4A3A', 'Cron\n예약'),
        (7.0, 7.9,  '#C08B2D', 'Memory'),
    ]
    for ox, oy, color, label in outer_nodes:
        # 연결선 (점선)
        ax.plot([hub_cx, ox], [hub_cy, oy], color=A_STEEL,
                lw=1.2, alpha=0.5, linestyle='--', zorder=2)
        # 중간 점 (흐름 느낌)
        mid_x = (hub_cx + ox) / 2
        mid_y = (hub_cy + oy) / 2
        ax.plot(mid_x, mid_y, 'o', color=A_STEEL, markersize=4, alpha=0.7, zorder=3)
        # 외부 노드
        draw_node(ax, ox, oy, 0.62, color, label, label_size=9)

    # ── 제목 영역 ──
    # "오픈클로"
    ax.text(5, 5.8, '오픈클로', ha='center', va='center',
            fontsize=58, color=A_WHITE, weight='bold', zorder=5)
    # "101가지 활용법"
    ax.text(5, 4.5, '101가지 활용법', ha='center', va='center',
            fontsize=44, color=A_GOLD, weight='bold', zorder=5)

    # 구분선
    ax.plot([1.5, 8.5], [3.9, 3.9], color=A_GOLD, lw=1.5, alpha=0.8, zorder=3)

    # 부제
    ax.text(5, 3.35, '팀장이 바로 쓰는 실전 활용법 101가지', ha='center', va='center',
            fontsize=17, color=A_GRAY, zorder=5)

    # ── 하단 장식 + 저자 ──
    ax.plot([0.5, 9.5], [0.8, 0.8], color=A_GOLD, lw=2, zorder=3)
    ax.text(5, 0.45, '레오클로 지음', ha='center', va='center',
            fontsize=14, color=A_GRAY, zorder=5)

    # 저장
    path = os.path.join(IMG_DIR, "cover_a.png")
    fig.savefig(path, dpi=160, bbox_inches='tight', facecolor=A_BG_TOP,
                edgecolor='none', pad_inches=0)
    plt.close(fig)
    print(f"  cover_a.png saved → {path}")


def cover_b():
    """대안 B — 101 임팩트 컨셉 (흰 배경 + 틸 그라데이션 + 대형 숫자)"""
    fig, ax = plt.subplots(figsize=(10, 16), dpi=160)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 16)
    ax.axis('off')
    fig.patch.set_facecolor(B_WHITE)

    # ── 상단 틸 배경 영역 (전체 상단 40%) ──
    for i in range(128):
        t = i / 128
        # 틸 → 흰색으로 그라데이션
        r = int(0x0D + (0xFF - 0x0D) * t)
        g = int(0x94 + (0xFF - 0x94) * t)
        b = int(0x88 + (0xFF - 0x88) * t)
        color = f'#{r:02X}{g:02X}{b:02X}'
        y = 16 - i * 7.5/128
        ax.add_patch(patches.Rectangle((0, y), 10, 7.5/128,
                                        facecolor=color, edgecolor='none', zorder=0))

    # ── 흰 배경 (하단 60%) ──
    ax.add_patch(patches.Rectangle((0, 0), 10, 8.5,
                                    facecolor=B_WHITE, edgecolor='none', zorder=0))

    # ── 대형 "101" 워터마크 (틸 영역) ──
    ax.text(5, 13.5, '101', ha='center', va='center',
            fontsize=200, color='white', alpha=0.18, weight='bold', zorder=2)

    # ── 상단 틸 영역 텍스트 ──
    ax.text(5, 11.8, '오픈클로', ha='center', va='center',
            fontsize=60, color=B_WHITE, weight='bold', zorder=5)

    # ── 구분선 ──
    ax.plot([1.0, 9.0], [10.8, 10.8], color=B_WHITE, lw=2, alpha=0.7, zorder=3)

    # ── 부제 (틸 영역 하단) ──
    ax.text(5, 10.3, '팀장이 바로 쓰는', ha='center', va='center',
            fontsize=20, color=B_WHITE, alpha=0.95, zorder=5)
    ax.text(5, 9.7, '실전 활용법 101가지', ha='center', va='center',
            fontsize=20, color=B_WHITE, alpha=0.95, zorder=5)

    # ── 흰 영역 — 메인 타이포 ──
    ax.text(5, 8.2, '101가지 활용법', ha='center', va='center',
            fontsize=46, color=B_TEAL, weight='bold', zorder=5)

    # ── 아이콘 가로 줄 ──
    icons = ['✉', '📅', '💬', '⚡', '📊', '🤖']
    labels = ['이메일', '캘린더', '슬랙', '자동화', '리포트', 'AI']
    icon_x = [1.0, 2.7, 4.4, 6.1, 7.8, 9.5]

    for i, (ic, lb) in enumerate(zip(icons, labels)):
        x = icon_x[i] if i < len(icon_x) else 5
        # 아이콘 원형 배경
        circle = Circle((x, 6.8), 0.55, color=B_TEAL_LIGHT, zorder=3)
        ax.add_patch(circle)
        ax.text(x, 6.8, lb, ha='center', va='center',
                fontsize=9, color=B_NAVY, weight='bold', zorder=5)

    # ── 한 줄 설명 ──
    ax.text(5, 5.7, '코딩 없이, 오늘부터 AI가 대신 일한다', ha='center', va='center',
            fontsize=16, color=B_GRAY, zorder=5)

    # ── 구분선 + 저자 ──
    ax.plot([0.5, 9.5], [1.2, 1.2], color=B_TEAL, lw=2, zorder=3)
    ax.text(5, 0.7, '레오클로 지음', ha='center', va='center',
            fontsize=14, color=B_NAVY, zorder=5)

    # 테두리
    rect = patches.Rectangle((0.05, 0.05), 9.9, 15.9,
                               fill=False, edgecolor=B_TEAL, lw=3, zorder=10)
    ax.add_patch(rect)

    # 저장
    path = os.path.join(IMG_DIR, "cover_b.png")
    fig.savefig(path, dpi=160, bbox_inches='tight', facecolor=B_WHITE,
                edgecolor='none', pad_inches=0)
    plt.close(fig)
    print(f"  cover_b.png saved → {path}")


def main():
    os.makedirs(IMG_DIR, exist_ok=True)
    setup_font()
    plt.rcParams['axes.unicode_minus'] = False

    print("=" * 50)
    print("표지 이미지 생성 — 오픈클로 101가지 활용법")
    print("=" * 50)

    cover_a()
    cover_b()

    print("=" * 50)
    print(f"완료! output/images/cover_a.png, cover_b.png")
    print("=" * 50)


if __name__ == '__main__':
    main()

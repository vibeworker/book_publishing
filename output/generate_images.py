#!/usr/bin/env python3
"""
30개 그림을 McKinsey 스타일로 생성 — 오픈클로 101가지 활용법
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

# ─── 설정 ───
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(BASE_DIR, "output", "images")
font_path = os.path.join(BASE_DIR, "font", "Pretendard-Regular.otf")
bold_path = os.path.join(BASE_DIR, "font", "Pretendard-Bold.otf")

# ═══════════════════════════════════════════════════════
# McKinsey 디자인 시스템
# ═══════════════════════════════════════════════════════

# 배경
BG = '#FFFFFF'
BG_SUBTLE = '#F7F9FC'

# 프라이머리 컬러 — 네이비 그라데이션
NAVY_DARK = '#0D1B2A'
NAVY = '#1B2A4A'
NAVY_MED = '#2C4A6E'
STEEL = '#4A7FB5'
STEEL_LIGHT = '#7BA7CC'

# 악센트 컬러 — 절제된 하이라이트
TEAL = '#0D9488'
TEAL_LIGHT = '#99F6E4'
CORAL = '#DC4A3A'
CORAL_LIGHT = '#FEE2E2'
GOLD = '#C08B2D'
GOLD_LIGHT = '#FEF3C7'
EMERALD = '#059669'
EMERALD_LIGHT = '#D1FAE5'
PURPLE = '#7C3AED'

# 뉴트럴
GRAY_900 = '#111827'
GRAY_700 = '#374151'
GRAY_500 = '#6B7280'
GRAY_400 = '#9CA3AF'
GRAY_300 = '#D1D5DB'
GRAY_200 = '#E5E7EB'
GRAY_100 = '#F3F4F6'
WHITE = '#FFFFFF'

# 그래프용 순서 컬러 (맥킨지 보고서 느낌)
SEQ_COLORS = [NAVY, STEEL, TEAL, GOLD, CORAL, PURPLE, '#0EA5E9', EMERALD]


def save_fig(fig, num):
    path = os.path.join(IMG_DIR, f"fig{num:02d}.png")
    fig.savefig(path, dpi=220, bbox_inches='tight', facecolor=BG, edgecolor='none',
                pad_inches=0.3)
    plt.close(fig)
    print(f"  fig{num:02d}.png saved")
    return path


def _shadow_box(ax, x, y, w, h, color, radius="round,pad=0.12", zorder=2):
    """그림자 + 박스 조합으로 입체감"""
    # 그림자
    ax.add_patch(FancyBboxPatch((x + 0.06, y - 0.06), w, h, boxstyle=radius,
                                 facecolor='#00000008', edgecolor='none', zorder=zorder - 1))
    # 본체
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=radius,
                                 facecolor=color, edgecolor='none', zorder=zorder))


def add_rounded_box(ax, x, y, w, h, text, color=NAVY, text_color=WHITE,
                    fontsize=11, bold=True, zorder=3):
    _shadow_box(ax, x, y, w, h, color, zorder=zorder)
    weight = 'bold' if bold else 'normal'
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center',
            fontsize=fontsize, color=text_color, weight=weight, zorder=zorder + 1)


def add_arrow(ax, x1, y1, x2, y2, color=GRAY_400, lw=1.8):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                                connectionstyle='arc3,rad=0'))


def _title(ax, x, y, text, fontsize=16):
    ax.text(x, y, text, ha='center', va='center',
            fontsize=fontsize, color=NAVY_DARK, weight='bold')


def _subtitle(ax, x, y, text, fontsize=10):
    ax.text(x, y, text, ha='center', va='center',
            fontsize=fontsize, color=GRAY_500, style='italic')


def _divider(ax, x1, x2, y, color=GRAY_200, lw=1):
    ax.plot([x1, x2], [y, y], color=color, lw=lw, zorder=1)


# ═══════════════════════════════════════════════════════
# 범용 차트 함수들
# ═══════════════════════════════════════════════════════

def create_flow_chart(num, title, steps, subtitle=""):
    n = len(steps)
    fig_w = max(12, n * 3)
    fig, ax = plt.subplots(1, 1, figsize=(fig_w, 4))
    total_w = n * 2.5
    ax.set_xlim(-0.5, total_w + 0.5)
    ax.set_ylim(-1, 3)
    ax.axis('off')
    fig.patch.set_facecolor(BG)

    _title(ax, total_w / 2, 2.6, title, fontsize=16)

    for i, step in enumerate(steps):
        x = i * 2.5 + 0.25
        c = SEQ_COLORS[i % len(SEQ_COLORS)]
        add_rounded_box(ax, x, 0.2, 2.0, 1.4, step, color=c, fontsize=10)
        if i < n - 1:
            ax.annotate('', xy=(x + 2.35, 0.9), xytext=(x + 2.08, 0.9),
                        arrowprops=dict(arrowstyle='->', color=GOLD, lw=2.2),
                        zorder=5)

    if subtitle:
        _subtitle(ax, total_w / 2, -0.5, subtitle)

    return save_fig(fig, num)


def create_comparison(num, title, left_title, left_items, right_title, right_items):
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    ax.set_xlim(0, 20)
    _n_max = max(len(left_items), len(right_items))
    _bottom = _n_max + 3 - 2.3 - (_n_max - 1) * 0.85 - 0.6
    ax.set_ylim(_bottom, _n_max + 3.5)
    ax.axis('off')
    fig.patch.set_facecolor(BG)

    top = max(len(left_items), len(right_items)) + 3
    _title(ax, 10, top, title, fontsize=16)

    # 좌측 헤더
    _shadow_box(ax, 0.5, top - 1.8, 8.5, 1.0, CORAL)
    ax.text(4.75, top - 1.3, f"사용 전: {left_title}", ha='center', va='center',
            fontsize=12, color=WHITE, weight='bold', zorder=5)

    # 우측 헤더
    _shadow_box(ax, 11, top - 1.8, 8.5, 1.0, EMERALD)
    ax.text(15.25, top - 1.3, f"사용 후: {right_title}", ha='center', va='center',
            fontsize=12, color=WHITE, weight='bold', zorder=5)

    for j, item in enumerate(left_items):
        y = top - 2.3 - j * 0.85
        ax.add_patch(FancyBboxPatch((0.5, y - 0.3), 8.5, 0.65, boxstyle="round,pad=0.08",
                                     facecolor=CORAL_LIGHT, edgecolor='none', zorder=2))
        ax.text(1.0, y + 0.02, f"•  {item}", ha='left', va='center',
                fontsize=10, color=GRAY_700, zorder=3)

    for j, item in enumerate(right_items):
        y = top - 2.3 - j * 0.85
        ax.add_patch(FancyBboxPatch((11, y - 0.3), 8.5, 0.65, boxstyle="round,pad=0.08",
                                     facecolor=EMERALD_LIGHT, edgecolor='none', zorder=2))
        ax.text(11.5, y + 0.02, f"•  {item}", ha='left', va='center',
                fontsize=10, color=GRAY_700, zorder=3)

    # 중앙 화살표 (콘텐츠 영역의 세로 중앙)
    _n = max(len(left_items), len(right_items))
    _y_top_item = top - 2.3 + 0.02
    _y_bot_item = top - 2.3 - (_n - 1) * 0.85 + 0.02
    mid_y = (_y_top_item + _y_bot_item) / 2
    ax.annotate('', xy=(10.8, mid_y), xytext=(9.2, mid_y),
                arrowprops=dict(arrowstyle='->', color=GOLD, lw=3), zorder=5)

    return save_fig(fig, num)


def create_venn_like(num, title, items):
    fig, ax = plt.subplots(1, 1, figsize=(11, 7))
    ax.set_xlim(-5, 5)
    ax.set_ylim(-3.5, 4.5)
    ax.axis('off')
    fig.patch.set_facecolor(BG)
    _title(ax, 0, 4, title)

    positions = [(-2.5, 0.3), (0, 0.3), (2.5, 0.3)]
    colors = [STEEL, CORAL, TEAL]
    alphas = [0.15, 0.15, 0.15]

    for (name, desc), (x, y), c, a in zip(items, positions, colors, alphas):
        circle = plt.Circle((x, y), 1.7, facecolor=c, alpha=a,
                             edgecolor=c, linewidth=2.5, linestyle='-')
        ax.add_patch(circle)
        ax.text(x, y + 0.4, name, ha='center', va='center',
                fontsize=13, color=c, weight='bold')
        ax.text(x, y - 0.3, desc, ha='center', va='center',
                fontsize=10, color=GRAY_700)

    # 중앙 교집합 레이블
    ax.text(0, -2.5, "각 도구의 강점을 조합하면 생산성이 극대화된다",
            ha='center', fontsize=10, color=GRAY_500, style='italic')

    return save_fig(fig, num)


def create_pyramid(num, title, levels):
    n = len(levels)
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(-7, 7)
    ax.set_ylim(-1, n * 1.6 + 1.5)
    ax.axis('off')
    fig.patch.set_facecolor(BG)
    _title(ax, 0, n * 1.6 + 0.8, title)

    grad = [NAVY_DARK, NAVY, NAVY_MED, STEEL]
    for i, (label, desc) in enumerate(levels):
        w = 4.5 + i * 2.2
        h = 1.2
        c = grad[i] if i < len(grad) else STEEL_LIGHT
        y = i * 1.6
        _shadow_box(ax, -w / 2, y, w, h, c)
        # 라벨 (상단)
        ax.text(0, y + h * 0.65, label, ha='center', va='center',
                fontsize=13, color=WHITE, weight='bold', zorder=5)
        # 설명 (하단)
        ax.text(0, y + h * 0.3, desc, ha='center', va='center',
                fontsize=9.5, color='#CBD5E1', zorder=5)

    return save_fig(fig, num)


def create_ui_mock(num, title, panels):
    fig, axes = plt.subplots(1, 3, figsize=(14, 6),
                              gridspec_kw={'width_ratios': [1, 2, 1]})
    fig.patch.set_facecolor(BG)
    fig.suptitle(title, fontsize=16, color=NAVY_DARK, weight='bold', y=0.98)

    panel_bgs = [BG_SUBTLE, WHITE, BG_SUBTLE]
    header_colors = [NAVY, STEEL, NAVY]
    for ax, (panel_title, panel_items), bg, hc in zip(axes, panels, panel_bgs, header_colors):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        # 카드 배경
        ax.add_patch(FancyBboxPatch((0.2, 0.2), 9.6, 9.6, boxstyle="round,pad=0.15",
                                     facecolor=bg, edgecolor=GRAY_200, linewidth=1))
        # 헤더 바
        ax.add_patch(FancyBboxPatch((0.2, 8.5), 9.6, 1.3, boxstyle="round,pad=0.15",
                                     facecolor=hc, edgecolor='none'))
        ax.text(5, 9.15, panel_title, ha='center', va='center', fontsize=12,
                color=WHITE, weight='bold')
        for j, item in enumerate(panel_items):
            y = 7.5 - j * 1.2
            ax.add_patch(FancyBboxPatch((0.6, y - 0.35), 8.8, 0.7, boxstyle="round,pad=0.06",
                                         facecolor=WHITE, edgecolor=GRAY_200, linewidth=0.5))
            ax.text(1.1, y, item, ha='left', va='center', fontsize=9, color=GRAY_700)

    plt.tight_layout(rect=[0, 0, 1, 0.93])
    return save_fig(fig, num)


def create_cycle(num, title, nodes, center_text=""):
    fig, ax = plt.subplots(1, 1, figsize=(9, 7))
    ax.set_xlim(-4.5, 4.5)
    ax.set_ylim(-2.5, 4.5)
    ax.axis('off')
    fig.patch.set_facecolor(BG)
    _title(ax, 0, 4, title)

    n = len(nodes)
    r = 2.5
    node_colors = [NAVY, TEAL, GOLD]

    # 화살표 먼저 (zorder 낮게) — 박스 바깥에서 시작/끝
    _bw, _bhalf = 1.0, 0.55  # 박스 반폭, 반높이
    for i in range(n):
        angle = 90 - i * (360 / n)
        rad = np.radians(angle)
        x, y = r * np.cos(rad), r * np.sin(rad)
        next_i = (i + 1) % n
        next_angle = 90 - next_i * (360 / n)
        next_rad = np.radians(next_angle)
        x2, y2 = r * np.cos(next_rad), r * np.sin(next_rad)
        # 방향 벡터
        dx, dy = x2 - x, y2 - y
        dist = np.sqrt(dx**2 + dy**2)
        ux, uy = dx / dist, dy / dist
        # 박스 경계까지 오프셋 계산 (사각형 박스 교차점)
        if abs(ux) < 1e-6:
            t_start = _bhalf / abs(uy)
        elif abs(uy) < 1e-6:
            t_start = _bw / abs(ux)
        else:
            t_start = min(_bw / abs(ux), _bhalf / abs(uy))
        if abs(ux) < 1e-6:
            t_end = _bhalf / abs(uy)
        elif abs(uy) < 1e-6:
            t_end = _bw / abs(ux)
        else:
            t_end = min(_bw / abs(ux), _bhalf / abs(uy))
        margin = 0.15
        sx = x + ux * (t_start + margin)
        sy = y + uy * (t_start + margin)
        ex = x2 - ux * (t_end + margin)
        ey = y2 - uy * (t_end + margin)
        ax.annotate('', xy=(ex, ey), xytext=(sx, sy),
                    arrowprops=dict(arrowstyle='->', color=GOLD, lw=2.5,
                                   mutation_scale=15),
                    zorder=1)

    # 노드
    for i, (label, desc) in enumerate(nodes):
        angle = 90 - i * (360 / n)
        rad = np.radians(angle)
        x, y = r * np.cos(rad), r * np.sin(rad)
        c = node_colors[i % len(node_colors)]
        _shadow_box(ax, x - 1.0, y - 0.55, 2.0, 1.1, c, zorder=3)
        ax.text(x, y + 0.12, label, ha='center', va='center',
                fontsize=12, color=WHITE, weight='bold', zorder=5)
        ax.text(x, y - 0.25, desc, ha='center', va='center',
                fontsize=9, color='#CBD5E1', zorder=5)

    if center_text:
        _shadow_box(ax, -1.0, -0.45, 2.0, 0.9, NAVY_DARK, zorder=4)
        ax.text(0, 0, center_text, ha='center', va='center',
                fontsize=11, color=WHITE, weight='bold', zorder=6)

    return save_fig(fig, num)


def create_card_grid(num, title, cards):
    n = len(cards)
    cols = min(n, 5)
    rows = (n + cols - 1) // cols
    fig_w = cols * 3.2
    fig_h = rows * 3.2 + 1.2
    fig, axes = plt.subplots(rows, cols, figsize=(fig_w, fig_h))
    fig.patch.set_facecolor(BG)
    fig.suptitle(title, fontsize=15, color=NAVY_DARK, weight='bold', y=0.97)

    if n == 1:
        axes = [axes]
    elif rows == 1:
        axes = list(axes)
    else:
        axes = [ax for row in axes for ax in row]

    card_colors = [NAVY, STEEL, TEAL, GOLD, CORAL, EMERALD, PURPLE, '#0EA5E9']
    for i, (card_title, card_desc) in enumerate(cards):
        if i < len(axes):
            ax = axes[i]
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 7)
            ax.axis('off')
            c = card_colors[i % len(card_colors)]
            # 카드 본체
            ax.add_patch(FancyBboxPatch((0.3, 0.3), 9.4, 6.4, boxstyle="round,pad=0.15",
                                         facecolor=WHITE, edgecolor=GRAY_200, linewidth=1))
            # 상단 컬러 바
            ax.add_patch(FancyBboxPatch((0.3, 5.0), 9.4, 1.7, boxstyle="round,pad=0.15",
                                         facecolor=c, edgecolor='none'))
            ax.text(5, 5.85, card_title, ha='center', va='center',
                    fontsize=12, color=WHITE, weight='bold')
            ax.text(5, 2.8, card_desc, ha='center', va='center',
                    fontsize=10, color=GRAY_700, linespacing=1.5)

    for i in range(n, len(axes)):
        axes[i].axis('off')

    plt.tight_layout(rect=[0, 0, 1, 0.93])
    return save_fig(fig, num)


def create_timeline(num, title, events):
    n = len(events)
    fig, ax = plt.subplots(1, 1, figsize=(13, 4.5))
    total_w = n * 2.5
    ax.set_xlim(-0.5, total_w + 0.5)
    ax.set_ylim(-2, 3)
    ax.axis('off')
    fig.patch.set_facecolor(BG)
    _title(ax, total_w / 2, 2.5, title)

    # 타임라인 바
    ax.plot([0.3, total_w - 0.3], [0.5, 0.5], color=NAVY, lw=3, zorder=1, solid_capstyle='round')

    for i, (time_label, desc) in enumerate(events):
        x = i * 2.5 + 0.5 + (2.5 - 1) / 2
        c = SEQ_COLORS[i % len(SEQ_COLORS)]
        # 노드
        ax.plot(x, 0.5, 'o', color=c, markersize=14, zorder=3,
                markeredgecolor=WHITE, markeredgewidth=2)
        # 라벨
        ax.text(x, 1.5, time_label, ha='center', va='center', fontsize=12,
                color=NAVY_DARK, weight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor=GRAY_100, edgecolor='none'))
        ax.text(x, -0.5, desc, ha='center', va='center', fontsize=10,
                color=GRAY_700, linespacing=1.4)

    return save_fig(fig, num)


# ═══════════════════════════════════════════════════════
# 40개 그림 생성
# ═══════════════════════════════════════════════════════

def main():
    os.makedirs(IMG_DIR, exist_ok=True)

    # 폰트 등록 — Pretendard 우선, 없으면 AppleGothic/NanumGothic 폴백
    if os.path.exists(font_path):
        fm.fontManager.addfont(font_path)
    if os.path.exists(bold_path):
        fm.fontManager.addfont(bold_path)

    # 사용 가능한 한글 폰트 자동 선택
    available = {f.name for f in fm.fontManager.ttflist}
    for _candidate in ['Pretendard', 'AppleGothic', 'NanumGothic', 'Malgun Gothic']:
        if _candidate in available:
            plt.rcParams['font.family'] = _candidate
            print(f"  폰트: {_candidate} 사용")
            break
    plt.rcParams['axes.unicode_minus'] = False

    print("=" * 50)
    print("그림 생성 시작 (30개) — McKinsey Style")
    print("=" * 50)

    # ── 그림 1: ChatGPT vs Zapier vs 오픈클로 포지셔닝 비교 (2×2 맵) ──
    fig, ax = plt.subplots(1, 1, figsize=(10, 9))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    fig.patch.set_facecolor(BG)
    _title(ax, 5, 9.5, 'ChatGPT vs Zapier vs 오픈클로: 어디서 쓰이는가?', fontsize=16)
    # 사분면 배경
    ax.add_patch(patches.Rectangle((1, 1), 4, 3.5, facecolor=GOLD_LIGHT, edgecolor=GRAY_300, lw=1, zorder=1))
    ax.add_patch(patches.Rectangle((5, 1), 4, 3.5, facecolor=TEAL_LIGHT, edgecolor=GRAY_300, lw=1, zorder=1))
    ax.add_patch(patches.Rectangle((1, 4.5), 4, 3.5, facecolor=CORAL_LIGHT, edgecolor=GRAY_300, lw=1, zorder=1))
    ax.add_patch(patches.Rectangle((5, 4.5), 4, 3.5, facecolor=EMERALD_LIGHT, edgecolor=GRAY_300, lw=1, zorder=1))
    # 축 레이블
    ax.text(5, 0.5, '데이터 원천: 범용 지식 → 내 자료', ha='center', va='center', fontsize=11, color=GRAY_700)
    ax.text(0.5, 5.25, '자동화\n수준\n높음', ha='center', va='center', fontsize=10, color=GRAY_700, rotation=90)
    ax.text(0.5, 2.75, '자동화\n수준\n낮음', ha='center', va='center', fontsize=10, color=GRAY_700, rotation=90)
    # 도구 포지션
    _shadow_box(ax, 5.8, 5.5, 2.4, 1.8, EMERALD)
    ax.text(7, 6.4, '오픈클로', ha='center', va='center', fontsize=14, color=WHITE, weight='bold', zorder=5)
    ax.text(7, 5.9, '내 자료 + 자동화', ha='center', va='center', fontsize=9, color=WHITE, zorder=5)
    _shadow_box(ax, 5.8, 1.8, 2.4, 1.5, TEAL)
    ax.text(7, 2.55, 'Zapier', ha='center', va='center', fontsize=14, color=WHITE, weight='bold', zorder=5)
    ax.text(7, 2.1, '규칙 기반 자동화', ha='center', va='center', fontsize=9, color=WHITE, zorder=5)
    _shadow_box(ax, 1.8, 5.5, 2.4, 1.8, CORAL)
    ax.text(3, 6.4, 'ChatGPT', ha='center', va='center', fontsize=14, color=WHITE, weight='bold', zorder=5)
    ax.text(3, 5.9, '범용 지식 + 생성', ha='center', va='center', fontsize=9, color=WHITE, zorder=5)
    save_fig(fig, 1)

    # ── 그림 2: 오픈클로 도입 전/후 하루 업무 흐름 비교 ──
    create_comparison(2, "오픈클로 도입 전/후: 아침 8시-9시 루틴",
        "오픈클로 없이", [
            "8:00  메일함 열기 (읽지 않은 34건)",
            "8:10  하나하나 클릭해서 확인",
            "8:30  슬랙 알림 별도 확인",
            "8:45  캘린더 열어 일정 파악",
            "8:55  뉴스 앱 켜서 업계 동향 체크",
            "9:05  이제야 업무 시작 (집중력 분산)",
        ],
        "오픈클로 활용", [
            "8:00  '하나야, 오늘 브리핑 줘'",
            "8:02  중요 메일 3건 요약 수신",
            "8:03  오늘 회의·마감 일정 정리 확인",
            "8:04  업계 주요 뉴스 3줄 요약",
            "8:05  오늘 집중 과제 1순위 확정",
            "8:10  업무 시작 (50분 빠르게)",
        ])

    # ── 그림 3: 에이전트-세션-메모리-페르소나 관계도 ──
    create_card_grid(3, "오픈클로 7가지 핵심 구조: 직장 조직도 비유",
        [("에이전트\n(팀장)", "목표를 정하고\n전체를 지휘"),
         ("페르소나\n(직함+성격)", "어떤 역할로\n행동할지 정의"),
         ("스킬\n(업무 도구)", "이메일·캘린더\n슬랙 등 실행"),
         ("메모리\n(업무일지)", "지난 맥락을\n기억·누적"),
         ("세션\n(오늘 회의)", "지금 이 대화\n작업 단위"),
         ("Heartbeat\n(자동 감지)", "조건 발생 시\n스스로 작동"),
         ("Cron\n(예약 알람)", "정해진 시간에\n자동 실행")])

    # ── 그림 4: Heartbeat vs Cron 동작 흐름 비교 ──
    create_comparison(4, "Heartbeat vs Cron: 경비원 vs 알람 시계",
        "Heartbeat (경비원 순찰)", [
            "24시간 조건 감지 대기",
            "이상 발생 즉시 반응",
            "'재고 0 감지' → 즉시 발주",
            "'경쟁사 가격 변동' → 알림 발송",
            "사건 기반 실행",
            "언제 실행될지 모름",
        ],
        "Cron (알람 시계)", [
            "매일 오전 8시 정각 실행",
            "매주 월요일 주간 리포트",
            "매월 1일 정산 자동화",
            "시간 기반 실행",
            "언제 실행될지 예측 가능",
            "사건 발생 여부 무관",
        ])

    # ── 그림 5: 보안 체크리스트 요약표 ──
    create_card_grid(5, "오픈클로 운영 전 보안 체크리스트",
        [("최소 권한\n원칙", "필요한 스킬만\n연결, 초과 권한 제거"),
         ("승인 게이트\n설정", "중요 작업 전\n인간 확인 단계"),
         ("외부 입력\n샌드박스", "이메일 원문 직접\n실행 컨텍스트 금지"),
         ("메모리\nTTL 설정", "정보 유효기간\n범주별 만료 설정"),
         ("중복 실행\n방지", "Cron 멱등성 확보\n실행 ID 저장"),
         ("모니터링\n에이전트", "Heartbeat 자체\n감시 루프 설정")])

    # ── 그림 6: 오픈클로 첫 실행 화면 목업 ──
    create_ui_mock(6, "오픈클로 온보딩: 3단계로 첫 에이전트 만들기",
        [("1단계: 에이전트 생성", ["이름 입력: '하나'", "역할 선택: 업무 비서", "페르소나 설정 →"]),
         ("2단계: 스킬 연결", ["이메일(Gmail) 연결", "캘린더 연결", "슬랙 연결 (선택)"]),
         ("3단계: 첫 명령", ["'하나야, 오늘 중요한 메일 알려줘'", "→ 결과 확인", "→ 조정 후 저장"])])

    # ── 그림 7: 업무 유형별 모델 선택 결정 트리 ──
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    fig.patch.set_facecolor(BG)
    _title(ax, 6, 7.5, '업무 유형별 모델 선택 결정 트리', fontsize=16)
    # 시작
    _shadow_box(ax, 4.5, 6.2, 3, 0.8, NAVY)
    ax.text(6, 6.6, '어떤 작업인가?', ha='center', va='center', fontsize=12, color=WHITE, weight='bold', zorder=5)
    # 분기 1
    _shadow_box(ax, 0.5, 4.5, 3.2, 0.8, GOLD)
    ax.text(2.1, 4.9, '단순 분류·요약', ha='center', va='center', fontsize=11, color=WHITE, weight='bold', zorder=5)
    _shadow_box(ax, 4.4, 4.5, 3.2, 0.8, GOLD)
    ax.text(6, 4.9, '복잡한 분석·판단', ha='center', va='center', fontsize=11, color=WHITE, weight='bold', zorder=5)
    _shadow_box(ax, 8.3, 4.5, 3.2, 0.8, GOLD)
    ax.text(9.9, 4.9, '창의적 생성', ha='center', va='center', fontsize=11, color=WHITE, weight='bold', zorder=5)
    # 결과
    _shadow_box(ax, 0.5, 2.5, 3.2, 1.2, TEAL)
    ax.text(2.1, 3.1, '경량 모델\n(비용 70% 절감)', ha='center', va='center', fontsize=11, color=WHITE, zorder=5)
    _shadow_box(ax, 4.4, 2.5, 3.2, 1.2, NAVY_MED)
    ax.text(6, 3.1, '고급 모델\n(GPT-4 / Claude)', ha='center', va='center', fontsize=11, color=WHITE, zorder=5)
    _shadow_box(ax, 8.3, 2.5, 3.2, 1.2, PURPLE)
    ax.text(9.9, 3.1, '창의 특화 모델\n(GPT-4o 등)', ha='center', va='center', fontsize=11, color=WHITE, zorder=5)
    # 화살표
    add_arrow(ax, 6, 6.2, 2.1, 5.3, GRAY_400)
    add_arrow(ax, 6, 6.2, 6, 5.3, GRAY_400)
    add_arrow(ax, 6, 6.2, 9.9, 5.3, GRAY_400)
    add_arrow(ax, 2.1, 4.5, 2.1, 3.7, GRAY_400)
    add_arrow(ax, 6, 4.5, 6, 3.7, GRAY_400)
    add_arrow(ax, 9.9, 4.5, 9.9, 3.7, GRAY_400)
    _subtitle(ax, 6, 0.5, '페르소나에 모델 라우팅 규칙 설정 → 자동 최적 선택')
    save_fig(fig, 7)

    # ── 그림 8: 레시피 선택 가이드 매트릭스 ──
    fig, ax = plt.subplots(1, 1, figsize=(10, 9))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    fig.patch.set_facecolor(BG)
    _title(ax, 5, 9.5, '레시피 선택 가이드: 난이도 × ROI 매트릭스', fontsize=15)
    # 사분면 배경
    ax.add_patch(patches.Rectangle((1, 1), 4, 4, facecolor=GOLD_LIGHT, edgecolor=GRAY_300, lw=1, zorder=1))
    ax.add_patch(patches.Rectangle((5, 1), 4, 4, facecolor=EMERALD_LIGHT, edgecolor=GRAY_300, lw=1, zorder=1))
    ax.add_patch(patches.Rectangle((1, 5), 4, 4, facecolor=CORAL_LIGHT, edgecolor=GRAY_300, lw=1, zorder=1))
    ax.add_patch(patches.Rectangle((5, 5), 4, 4, facecolor=TEAL_LIGHT, edgecolor=GRAY_300, lw=1, zorder=1))
    ax.text(3, 0.5, '낮은 난이도', ha='center', fontsize=11, color=GRAY_700)
    ax.text(7, 0.5, '높은 난이도', ha='center', fontsize=11, color=GRAY_700)
    ax.text(0.5, 3, '낮은\nROI', ha='center', va='center', fontsize=10, color=GRAY_700, rotation=90)
    ax.text(0.5, 7, '높은\nROI', ha='center', va='center', fontsize=10, color=GRAY_700, rotation=90)
    ax.text(3, 8.6, '고ROI 쉬운 레시피 → 먼저 시작!', ha='center', fontsize=10, color=CORAL, weight='bold')
    ax.text(7, 8.6, '고ROI 고난이도 → 나중에 도전', ha='center', fontsize=10, color=TEAL, weight='bold')
    # 레시피 포인트
    _data = [
        (2.5, 7.5, '이메일 분류', CORAL),
        (3.5, 6.5, '아침 브리핑', CORAL),
        (2.0, 6.0, '일정 관리', CORAL),
        (6.5, 7.5, '멀티에이전트', TEAL),
        (7.5, 8.0, 'DevOps 자동화', TEAL),
        (2.0, 2.5, '간단 알림', GOLD),
        (3.5, 3.0, '쇼핑 리스트', GOLD),
        (6.5, 3.5, '콘텐츠 파이프라인', EMERALD),
        (7.5, 4.0, 'CRM 자동화', EMERALD),
    ]
    for _x, _y, _label, _color in _data:
        ax.plot(_x, _y, 'o', color=_color, markersize=14, zorder=5)
        ax.text(_x, _y - 0.5, _label, ha='center', fontsize=9, color=GRAY_700, zorder=6)
    save_fig(fig, 8)

    # ── 그림 9: 오픈클로 커뮤니케이션 자동화 흐름도 ──
    create_flow_chart(9, "오픈클로 커뮤니케이션 자동화 흐름",
        ["이메일·슬랙\n채널 감지", "중요도\nAI 분류", "긴급/중요\n우선 알림", "초안\n자동 생성", "승인 후\n발송"],
        "모든 채널을 하나로 통합, 중요한 것만 사람이 확인")

    # ── 그림 10: 오픈클로 지식 관리 파이프라인 ──
    create_flow_chart(10, "오픈클로 지식 관리 파이프라인",
        ["정보 수집\n(링크·PDF·메모)", "자동 태깅\n및 분류", "메모리\n장기 저장", "연관 정보\n자동 연결", "필요 시\n즉시 검색"],
        "쌓일수록 똑똑해지는 개인 지식베이스")

    # ── 그림 11: 오픈클로 콘텐츠 제작 워크플로우 ──
    create_flow_chart(11, "오픈클로 콘텐츠 제작 워크플로우",
        ["주제·키워드\n입력", "리서치\n자동 수집", "초안\n생성", "브랜드 톤\n검수", "채널별\n포맷 변환"],
        "블로그 1개 → SNS·뉴스레터·영상 스크립트 동시 생성")

    # ── 그림 12: 오픈클로 DevOps 자동화 구조도 ──
    create_flow_chart(12, "오픈클로 DevOps 자동화 구조도",
        ["코드 배포\n이벤트", "Heartbeat\n상태 감지", "이상 탐지\n→ 알림", "자동 롤백\n또는 에스컬레이션", "슬랙 리포트\n자동 발송"],
        "밤새 서버 감시, 개발자는 편히 자도 된다")

    # ── 그림 13: 오픈클로 영업·마케팅 자동화 흐름 ──
    create_flow_chart(13, "오픈클로 영업·마케팅 자동화 흐름",
        ["리드\n수신", "자동 자격\n검증", "맞춤 초안\n생성", "승인 후\n발송", "CRM\n자동 기록"],
        "첫 응대 2분 이내, 전환율 40% 향상")

    # ── 그림 14: 오픈클로 생활 자동화 시나리오 ──
    create_card_grid(14, "오픈클로 생활 자동화: 일상에서 바로 쓰는 레시피",
        [("공과금\n기한 관리", "마감일 임박\n자동 알림"),
         ("쇼핑 리스트\n자동화", "냉장고 재료\n기반 추천"),
         ("건강 리마인더", "물 마시기·운동\n루틴 알림"),
         ("여행 준비\n체크리스트", "출발 전 필수\n항목 자동 생성"),
         ("독서 관리\n시스템", "읽은 책 기록\n다음 책 추천"),
         ("가계 분석\n리포트", "지출 패턴\n월별 요약")])

    # ── 그림 15: 오픈클로 고급 설정 구조 ──
    create_pyramid(15, "오픈클로 자동화 단계별 성숙도 피라미드",
        [("Lv.1 알림", "조건 감지 → 사용자에게 알림만"),
         ("Lv.2 초안+확인", "초안 생성 → 사람이 검토 후 실행"),
         ("Lv.3 완전 자동", "100번 성공 후 자동 실행 승인")])

    # ── 그림 16: 오픈클로 트러블슈팅 판단 흐름도 ──
    create_flow_chart(16, "오픈클로 트러블슈팅: 문제 유형별 판단 흐름",
        ["이상 증상\n발생", "스킬 연결\n문제?", "메모리/세션\n문제?", "비용 폭주\n문제?", "보안 문제?"],
        "진단 4단계: 스킬 → 메모리 → 비용 → 보안 순서로 점검")

    # ── 그림 17: 오픈클로 확장 연결 구조도 ──
    create_card_grid(17, "오픈클로 스킬 생태계: 연결 가능한 외부 서비스",
        [("커뮤니케이션", "Gmail·Outlook\n슬랙·텔레그램"),
         ("일정·업무", "Google Calendar\nNotion·Asana"),
         ("개발·코드", "GitHub·Jira\nLinear·CI/CD"),
         ("데이터·분석", "Google Sheets\n데이터베이스 API"),
         ("커스텀 API", "사내 시스템\n자체 서비스"),
         ("AI·모델", "GPT-4·Claude\nGemini·Llama")])

    # ── 그림 18: 오픈클로 팀·기업 운영 아키텍처 ──
    create_card_grid(18, "오픈클로 팀·기업 운영 아키텍처",
        [("라우터\n에이전트", "요청 분류 후\n전담 에이전트 배분"),
         ("이메일\n전담 에이전트", "커뮤니케이션\n채널 담당"),
         ("리서치\n전담 에이전트", "정보 수집·분석\n전담"),
         ("콘텐츠\n전담 에이전트", "작성·편집\n파이프라인"),
         ("모니터링\n에이전트", "전체 시스템\n감시·보고"),
         ("공유\n메모리", "팀 전체 맥락\n중앙 저장소")])

    # ── 그림 19: 이메일 자동 분류 및 알림 흐름 ──
    create_flow_chart(19, "이메일 자동 분류 및 알림 흐름",
        ["새 메일\n수신", "발신자·주제\n중요도 분류", "긴급/VIP\n즉시 알림", "일반 메일\n일괄 요약", "스팸\n자동 필터"],
        "받은 편지함 34건 → 액션 필요 3건으로 압축")

    # ── 그림 20: 링크 수집→지식베이스 정리 파이프라인 ──
    create_flow_chart(20, "링크 수집에서 지식베이스 정리까지",
        ["링크·PDF\n수집", "자동 읽기\n요약 생성", "태그·카테고리\n자동 분류", "메모리\n장기 저장", "키워드\n즉시 검색"],
        "'그때 봤던 그 글' → 언제든 3초 만에 검색")

    # ── 그림 21: 유튜브 기획→스크립트 생성 흐름 ──
    create_flow_chart(21, "유튜브 콘텐츠 기획에서 스크립트까지",
        ["키워드\n리서치", "경쟁 영상\n분석", "구성안\n자동 생성", "스크립트\n초안 작성", "썸네일\n문구 추천"],
        "아이디어 → 촬영 준비 완료까지 30분")

    # ── 그림 22: DevOps 배포 모니터링 자동화 ──
    create_flow_chart(22, "DevOps 배포 모니터링 자동화",
        ["배포 완료\n이벤트", "Heartbeat\n상태 체크", "오류율\n임계 초과?", "자동 롤백\n실행", "팀 슬랙\n알림 발송"],
        "사람이 없어도 서버는 스스로 지킨다")

    # ── 그림 23: CRM 자동 업데이트 흐름 ──
    create_flow_chart(23, "CRM 자동 업데이트: 통화에서 기록까지",
        ["고객 통화\n또는 미팅", "AI 통화 요약\n생성", "CRM 필드\n자동 입력", "다음 액션\n자동 생성", "담당자\n알림"],
        "통화 끝나자마자 CRM 업데이트, 수기 입력 0분")

    # ── 그림 24: 공과금·기한 관리 알림 시스템 ──
    create_flow_chart(24, "공과금·기한 관리 자동화 시스템",
        ["캘린더\n기한 감지", "7일 전\n1차 알림", "3일 전\n2차 알림", "당일\n최종 알림", "완료 확인\n후 종료"],
        "놓친 기한은 더 이상 없다")

    # ── 그림 25: 멀티에이전트 협업 아키텍처 ──
    fig, ax = plt.subplots(1, 1, figsize=(12, 9))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 9)
    ax.axis('off')
    fig.patch.set_facecolor(BG)
    _title(ax, 6, 8.5, '멀티에이전트 협업 아키텍처', fontsize=16)
    # 중앙 라우터
    _shadow_box(ax, 4.5, 5.8, 3, 1.2, NAVY_DARK)
    ax.text(6, 6.4, '라우터 에이전트\n(오케스트레이터)', ha='center', va='center', fontsize=12, color=WHITE, weight='bold', zorder=5)
    # 전담 에이전트
    _agents = [
        (1.0, 3.0, '이메일\n에이전트', STEEL),
        (3.5, 3.0, '리서치\n에이전트', TEAL),
        (6.0, 3.0, '콘텐츠\n에이전트', GOLD),
        (8.5, 3.0, '모니터링\n에이전트', CORAL),
    ]
    for _ax_pos, _ay_pos, _label, _color in _agents:
        _shadow_box(ax, _ax_pos, _ay_pos, 2.2, 1.0, _color)
        ax.text(_ax_pos + 1.1, _ay_pos + 0.5, _label, ha='center', va='center', fontsize=11, color=WHITE, weight='bold', zorder=5)
        add_arrow(ax, 6, 5.8, _ax_pos + 1.1, _ay_pos + 1.0, GRAY_400)
    # 공유 메모리
    _shadow_box(ax, 4.0, 0.8, 4.0, 1.0, EMERALD)
    ax.text(6, 1.3, '공유 메모리 (팀 전체 맥락)', ha='center', va='center', fontsize=12, color=WHITE, weight='bold', zorder=5)
    for _ax_pos, _, _, _ in _agents:
        add_arrow(ax, _ax_pos + 1.1, 3.0, 6, 1.8, GRAY_300)
    _subtitle(ax, 6, 0.3, '에이전트별 역할 분리 → 스위스 아미 나이프 함정 방지')
    save_fig(fig, 25)

    # ── 그림 26: 아침 브리핑 데이터 집계 흐름 ──
    create_flow_chart(26, "아침 브리핑 데이터 집계 흐름",
        ["이메일\n확인", "캘린더\n일정 수집", "슬랙\n알림 정리", "뉴스\n3줄 요약", "브리핑\n리포트 전송"],
        "5개 앱을 1개 알림으로 통합, 오전 루틴 50분 절약")

    # ── 그림 27: 백업 스케줄 모니터링 루프 ──
    create_cycle(27, "백업 스케줄 모니터링 루프",
        [("Cron 실행\n(매일 새벽 2시)", "백업 예약"),
         ("백업 완료\n확인", "Heartbeat 감지"),
         ("실패 시\n재실행·알림", "에스컬레이션")],
        center_text="자동\n백업")

    # ── 그림 28: 다채널 캠페인 성과 통합 구조 ──
    create_flow_chart(28, "다채널 캠페인 성과 통합 구조",
        ["채널별\n데이터 수집", "KPI\n자동 계산", "채널 간\n비교 분석", "인사이트\n자동 추출", "임원 리포트\n자동 발송"],
        "SNS·이메일·검색 광고 성과를 한 곳에서 통합")

    # ── 그림 29: 쇼핑 리스트 자동화 흐름 ──
    create_flow_chart(29, "쇼핑 리스트 자동화 흐름",
        ["냉장고 재료\n현황 파악", "레시피\n추천", "부족 재료\n리스트 생성", "마트 카테고리별\n자동 정렬", "쇼핑 완료\n재고 업데이트"],
        "식재료 관리부터 장 보기까지 완전 자동화")

    # ── 그림 30: 오픈클로 활용 여정 타임라인 ──
    create_timeline(30, "오픈클로 활용 여정: 첫 설정부터 전문가까지",
        [("Day 1", "첫 에이전트\n생성 완료"),
         ("Day 7", "Cron 아침\n브리핑 시작"),
         ("Day 30", "레시피 5개\n운영 중"),
         ("3개월", "멀티에이전트\n시스템 구축"),
         ("6개월", "팀 전체\n자동화 완성")])


    print("=" * 50)
    print(f"30개 그림 생성 완료! → {IMG_DIR}")
    print("=" * 50)


if __name__ == '__main__':
    main()

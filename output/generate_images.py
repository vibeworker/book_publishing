#!/usr/bin/env python3
"""
40개 그림을 McKinsey 스타일로 생성 — 프로페셔널, 고급스러운 디자인
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
BASE_DIR = "/Users/jaydenkang/Desktop/New Projects/20260321_노트북LM 책쓰기"
IMG_DIR = os.path.join(BASE_DIR, "output", "images")
os.makedirs(IMG_DIR, exist_ok=True)

# 폰트 등록
font_path = os.path.join(BASE_DIR, "font", "Pretendard-Regular.otf")
bold_path = os.path.join(BASE_DIR, "font", "Pretendard-Bold.otf")
fm.fontManager.addfont(font_path)
fm.fontManager.addfont(bold_path)
plt.rcParams['font.family'] = 'Pretendard'
plt.rcParams['axes.unicode_minus'] = False

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

print("=" * 50)
print("그림 생성 시작 (40개) — McKinsey Style")
print("=" * 50)

# ── 그림 1: 이 책의 구성 가이드맵 (세로 레이아웃) ──
fig, ax = plt.subplots(1, 1, figsize=(11, 13))
ax.set_xlim(0, 10)
ax.set_ylim(1.5, 14)
ax.axis('off')
fig.patch.set_facecolor(BG)
_title(ax, 5, 13.5, '이 책의 구성 가이드맵', fontsize=20)

_sections = [
    ('프롤로그', '일하는 방식, 노트북LM 이전과 이후로 나뉩니다', PURPLE),
    ('제1부', '고수는 이렇게 씁니다 (4명의 실전 사례)', NAVY),
    ('제2부', '오늘 점심, 딱 한 번만 따라 하세요 (시작 가이드)', STEEL),
    ('제3부', '분석과 검증의 기술 (활용법 01~05)', TEAL),
    ('제4부', '혼자 소화하는 기술 (활용법 06~08)', NAVY_MED),
    ('제5부', '남에게 보여주는 기술 (활용법 09~11)', GOLD),
    ('제6부', '월요일 아침부터 바로 쓰는 실전 시나리오 (활용법 12~16)', CORAL),
    ('제7부', '나에서 팀으로, 도구에서 시스템으로 (활용법 17~20)', EMERALD),
    ('에필로그', '지금 노트북을 여십시오', PURPLE),
    ('부록', '프롬프트 템플릿, FAQ, 업데이트 가이드', GRAY_500),
]
_bh, _gap = 0.7, 0.45
_sy = 12.5
for _i, (_label, _desc, _color) in enumerate(_sections):
    _y = _sy - _i * (_bh + _gap)
    _shadow_box(ax, 0.5, _y, 2.2, _bh, _color)
    ax.text(1.6, _y + _bh / 2, _label, ha='center', va='center',
            fontsize=13, color=WHITE, weight='bold', zorder=5)
    ax.text(3.2, _y + _bh / 2, _desc, ha='left', va='center',
            fontsize=11, color=GRAY_700, zorder=5)
    if _i < len(_sections) - 1:
        _arrow_top = _y - 0.03
        _arrow_bottom = _y - _gap + 0.03
        ax.annotate('', xy=(1.6, _arrow_bottom), xytext=(1.6, _arrow_top),
                    arrowprops=dict(arrowstyle='->', color=GOLD, lw=2.5,
                                   mutation_scale=15), zorder=1)
save_fig(fig, 1)

# ── 그림 2: Before/After 팀장의 하루 ──
create_comparison(2, "팀장의 하루: 노트북LM 사용 전 vs 사용 후",
    "노트북LM 없이", [
        "8:47  메일에서 보고서 200p 수신",
        "9:00  Ctrl+F로 키워드 검색 반복",
        "10:30 엑셀에 요점 수기 정리",
        "12:00 점심 건너뛰고 계속 읽기",
        "15:00 요약 작성 시작",
        "17:30 퇴근 포기, 야근 돌입",
    ],
    "노트북LM 활용", [
        "8:47  메일에서 보고서 200p 수신",
        "8:50  PDF를 노트북LM에 업로드",
        "8:52  '우리 팀 관련 부분만 정리해줘'",
        "8:57  핵심 요약 노트 저장 완료",
        "9:00  팀 회의에서 브리핑",
        "9:30  다른 업무 시작, 정시 퇴근",
    ])

# ── 그림 3~5: 플로우차트 ──
create_flow_chart(3, "세 개 보고서가 하나의 비교표로",
    ["영업팀\n보고서\n(48p)", "마케팅팀\n보고서\n(35p)", "개발팀\n보고서\n(62p)", "노트북LM\n교차 비교", "통합\n비교표"],
    "145페이지를 직접 읽지 않고, 5분 만에 핵심 비교 완료")

create_flow_chart(4, "회의 녹음에서 액션 아이템까지",
    ["75분 회의\n녹음(MP3)", "노트북LM\n업로드", "AI 분석\n(음성→텍스트)", "회의록\n자동 생성", "액션 아이템\n표 추출"],
    "회의 끝나고 5분이면 담당자별 할 일이 정리된다")

create_flow_chart(5, "설문 데이터에서 인사이트까지",
    ["서술형 응답\n387건", "PDF 변환\n소스 업로드", "감정 분석\n패턴 추출", "상위 불만\n5개 도출", "인사이트\n보고서"],
    "이틀 걸리던 분석이 30분으로 줄어든다")

# ── 그림 6: 벤 다이어그램 ──
create_venn_like(6, "ChatGPT vs Perplexity vs 노트북LM",
    [("ChatGPT", "인터넷 전체\n학습 데이터"),
     ("Perplexity", "실시간\n웹 검색"),
     ("노트북LM", "내가 올린\n자료만")])

# ── 그림 7: 세 도구 역할 분담 ──
create_card_grid(7, "세 도구의 역할 분담: 경쟁이 아니라 팀플레이",
    [("ChatGPT", "창의적 글쓰기\n아이디어 발상\n코드 생성"),
     ("Perplexity", "최신 정보 검색\n실시간 팩트체크\n출처 인용"),
     ("노트북LM", "내 자료 분석\n환각 최소화\n멀티미디어 변환")])

# ── 그림 8: 플랜별 피라미드 ──
create_pyramid(8, "노트북LM 플랜별 핵심 기능",
    [("Free", "노트북 100개, 소스 50개, Audio 3개/일"),
     ("Plus ($19.99)", "노트북 200개, 소스 100개, 확대된 한도"),
     ("Pro ($49.99)", "노트북 500개, 소스 300개, Deep Research"),
     ("Ultra ($249.99)", "소스 600개, Cinematic Video, 워터마크 제거")])

# ── 그림 9: 가입 3단계 ──
create_flow_chart(9, "노트북LM 시작하기: 3단계",
    ["Google 계정\n로그인", "notebooklm.google\n접속", "새 노트북\n만들기"],
    "1분이면 충분하다")

# ── 그림 10: 인터페이스 3구역 ──
create_ui_mock(10, "노트북LM 인터페이스: 세 구역",
    [("소스 패널", ["PDF 보고서.pdf", "경쟁사 분석.pdf", "회의 녹음.mp3", "시장 조사.url", "+ 소스 추가"]),
     ("채팅 패널", ["AI: 안녕하세요!", "나: 이 보고서의 핵심 3가지는?", "AI: 1. 시장 규모 확대...", "AI: 2. 경쟁 심화...", "AI: 3. 신기술 도입..."]),
     ("스튜디오 패널", ["Audio Overview", "Video Overview", "슬라이드", "인포그래픽", "마인드맵"])])

# ── 그림 11: 소스 유형 카드 ──
create_card_grid(11, "노트북LM이 읽을 수 있는 10가지 소스",
    [("PDF", "보고서, 논문, 제안서"),
     ("YouTube", "세미나, 경쟁사 발표"),
     ("오디오", "회의 녹음, 인터뷰"),
     ("Google Docs", "팀 공유 문서\n(자동 동기화)"),
     ("Google Slides", "발표 자료 분석"),
     ("Google Sheets", "데이터, 설문, 수치"),
     ("웹 URL", "기사, 블로그, 레퍼런스"),
     ("이미지", "차트, 다이어그램"),
     ("EPUB", "전자책 분석"),
     (".docx", "Word 문서")])

# ── 그림 12: 소스 → 첫 질문 → 결과 ──
create_flow_chart(12, "소스 업로드에서 첫 결과까지",
    ["소스 추가\n클릭", "PDF\n업로드", "첫 질문\n입력", "AI 답변\n확인", "노트\n저장"],
    "10분이면 첫 결과물을 손에 쥔다")

# ── 그림 13: 소스-채팅-노트 순환 ──
create_cycle(13, "소스, 채팅, 노트의 순환 구조",
    [("소스", "냉장고 재료"),
     ("채팅", "요리사와 대화"),
     ("노트", "완성된 레시피")],
    center_text="노트북LM")

# ── 그림 14: 교차 분석 비교 ──
create_comparison(14, "2개 비교 vs 5개 이상 교차 분석",
    "2개 소스 비교", [
        "보고서 A의 핵심 주장",
        "보고서 B의 핵심 주장",
        "일치하는 부분",
        "차이나는 부분",
    ],
    "5개 이상 교차 분석", [
        "공통 키워드 추출",
        "빈도 기반 패턴 발견",
        "소스 간 상충 지점 식별",
        "종합 인사이트 도출",
    ])

# ── 그림 15~18: 플로우차트 ──
create_flow_chart(15, "노트를 소스로 재활용하는 2차 분석",
    ["경쟁사 A\n분석 노트", "경쟁사 B\n분석 노트", "경쟁사 C\n분석 노트", "새 노트북에\n소스로 업로드", "종합 전략\n보고서"],
    "분석의 분석, 인사이트를 쌓아 올리는 기법")

create_card_grid(16, "같은 소스, 다른 맞춤 지시 = 다른 결과",
    [("마케팅 컨설턴트", "전략적 관점에서\n시장 기회를 분석"),
     ("초등학생 설명", "쉬운 말로\n비유를 곁들여 설명"),
     ("표 중심 정리", "모든 답변을\n표와 글머리로 구조화"),
     ("임원 브리핑", "핵심만 3줄로\n숫자 근거 포함")])

create_flow_chart(17, "환각 잡기: 출처 번호 클릭으로 원문 확인",
    ["AI 답변\n읽기", "출처 번호\n[1] 클릭", "원문\n해당 위치\n이동", "내용\n대조 확인"],
    "출처를 확인하는 습관이 신뢰를 지킨다")

create_flow_chart(18, "딥 리서치(Deep Research) 전체 플로우",
    ["사용자\n질문 입력", "리서치 계획\n자동 수립", "수백 개\n웹사이트\n탐색", "최대 50개\n소스 수집", "상세 보고서\n자동 생성"],
    "소스 밖 정보까지 확장하는 유일한 기능")

# ── 그림 19: 오디오 오버뷰 ──
create_card_grid(19, "오디오 오버뷰(Audio Overview) 4가지 형식",
    [("Deep Dive", "6~15분\n포괄적 토론"),
     ("Brief", "1~2분\n간결한 개요"),
     ("Study Guide", "학습 포인트\n정리 중심"),
     ("Custom", "맞춤 지시로\n원하는 형식")])

# ── 그림 20: 비디오 오버뷰 ──
create_ui_mock(20, "비디오 오버뷰(Video Overview) 재생 화면",
    [("비디오 컨트롤", ["재생/일시정지", "진행 바", "볼륨 조절", "전체 화면"]),
     ("영상 콘텐츠", ["슬라이드 형태의 시각 자료", "차트와 키워드 하이라이트", "AI 내레이션 음성", "자동 장면 전환"]),
     ("하단 정보", ["AI 내레이션 자막", "출처 표시", "챕터 구분", "다운로드 옵션"])])

# ── 그림 21: Video vs Cinematic ──
create_comparison(21, "비디오 오버뷰 vs 시네마틱 비디오",
    "Video Overview (기본)", [
        "슬라이드 전환 방식",
        "텍스트 + 간단한 시각 자료",
        "모든 유료 플랜 사용 가능",
        "빠른 생성 속도",
    ],
    "Cinematic Video (2026)", [
        "완전 애니메이션 장면 전환",
        "Gemini 3 + Veo 3 활용",
        "Ultra 플랜 전용($249.99)",
        "영화 같은 시각 표현",
    ])

# ── 그림 22: 맞춤 지시 4종 비교 ──
create_card_grid(22, "같은 소스, 4가지 맞춤 지시 = 4가지 결과",
    [("경영진 브리핑", "핵심 수치 3개\n전략적 시사점 중심"),
     ("팀원 교육용", "단계별 설명\n실습 예시 포함"),
     ("신입 온보딩", "기초 용어 설명\n쉬운 비유 사용"),
     ("고객 설명용", "전문 용어 제거\n혜택 중심 서술")])

# ── 그림 23: 마인드맵 예시 (맥킨지 스타일) ──
fig, ax = plt.subplots(1, 1, figsize=(11, 8))
ax.set_xlim(-6.5, 6.5)
ax.set_ylim(-5.5, 6.5)
ax.axis('off')
fig.patch.set_facecolor(BG)
_title(ax, 0, 6, "마인드맵: 복잡한 보고서를 한 장의 지도로", fontsize=16)

mc_colors = [STEEL, CORAL, EMERALD, GOLD, PURPLE]
branches = [("시장 규모", 3.5, 3.8), ("경쟁사 동향", -4, 3), ("소비자 트렌드", 4.5, -0.3),
            ("기술 변화", -3.8, -2), ("위험 요소", 0, -3.8)]

# 선 (도형 아래)
for i, (label, bx, by) in enumerate(branches):
    ax.plot([0, bx], [0.8, by], color=GRAY_300, lw=2.5, zorder=1, solid_capstyle='round')

# 가지 노드
for i, (label, bx, by) in enumerate(branches):
    _shadow_box(ax, bx - 1.3, by - 0.5, 2.6, 1.0, mc_colors[i], zorder=3)
    ax.text(bx, by, label, ha='center', va='center',
            fontsize=12, color=WHITE, weight='bold', zorder=5)

# 중심 노드
_shadow_box(ax, -1.6, 0, 3.2, 1.6, NAVY_DARK, zorder=4)
ax.text(0, 0.8, "시장분석\n보고서", ha='center', va='center',
        fontsize=14, color=WHITE, weight='bold', zorder=6)

_subtitle(ax, 0, -5, "중심 주제에서 핵심 가지로, 한눈에 구조를 파악한다")
save_fig(fig, 23)

# ── 그림 24: 마인드맵 2차 분석 ──
create_flow_chart(24, "마인드맵 기반 2차 분석 워크플로우",
    ["소스 3개\n업로드", "마인드맵\n생성", "공통 키워드\n추출", "관심 가지\n심화 분석", "교차 비교\n보고서"],
    "숲을 본 다음 나무를 본다")

# ── 그림 25: 플래시카드 모킹 ──
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={'wspace': 0.15})
fig.patch.set_facecolor(BG)
fig.suptitle("플래시카드 학습 화면", fontsize=16, color=NAVY_DARK, weight='bold', y=0.97)

# 앞면 (질문)
ax1.set_xlim(0, 10); ax1.set_ylim(0, 8); ax1.axis('off')
ax1.add_patch(FancyBboxPatch((0.3, 0.3), 9.4, 7.4, boxstyle="round,pad=0.2",
                               facecolor=WHITE, edgecolor=NAVY, linewidth=2))
ax1.add_patch(FancyBboxPatch((0.3, 6.2), 9.4, 1.5, boxstyle="round,pad=0.2",
                               facecolor=NAVY, edgecolor='none'))
ax1.text(5, 6.95, "QUESTION", fontsize=14, ha='center', color=WHITE, weight='bold')
ax1.text(5, 3.8, "노트북LM의\n소스 기반 설계란?", ha='center', va='center',
         fontsize=13, color=NAVY_DARK, weight='bold')
ax1.add_patch(FancyBboxPatch((1.2, 0.8), 3.2, 1.2, boxstyle="round,pad=0.1",
                               facecolor=EMERALD, edgecolor='none'))
ax1.text(2.8, 1.4, "Got it", ha='center', va='center', fontsize=11, color=WHITE, weight='bold')
ax1.add_patch(FancyBboxPatch((5.6, 0.8), 3.2, 1.2, boxstyle="round,pad=0.1",
                               facecolor=CORAL, edgecolor='none'))
ax1.text(7.2, 1.4, "Missed it", ha='center', va='center', fontsize=11, color=WHITE, weight='bold')

# 뒷면 (답변)
ax2.set_xlim(0, 10); ax2.set_ylim(0, 8); ax2.axis('off')
ax2.add_patch(FancyBboxPatch((0.3, 0.3), 9.4, 7.4, boxstyle="round,pad=0.2",
                               facecolor=BG_SUBTLE, edgecolor=TEAL, linewidth=2))
ax2.add_patch(FancyBboxPatch((0.3, 6.2), 9.4, 1.5, boxstyle="round,pad=0.2",
                               facecolor=TEAL, edgecolor='none'))
ax2.text(5, 6.95, "ANSWER", fontsize=14, ha='center', color=WHITE, weight='bold')
ax2.text(5, 3.5, "사용자가 업로드한 소스만\n참조하여 답변을 생성하는\n설계 방식. 환각을 최소화하고\n출처 추적이 가능하다.",
         ha='center', va='center', fontsize=12, color=GRAY_700, linespacing=1.6)
plt.tight_layout(rect=[0, 0, 1, 0.93])
save_fig(fig, 25)

# ── 그림 26: 퀴즈 모킹 ──
fig, ax = plt.subplots(1, 1, figsize=(9, 6))
ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis('off')
fig.patch.set_facecolor(BG)
ax.add_patch(FancyBboxPatch((0.3, 0.3), 9.4, 9.4, boxstyle="round,pad=0.2",
                              facecolor=WHITE, edgecolor=GRAY_200, linewidth=1.5))
# 헤더
ax.add_patch(FancyBboxPatch((0.3, 8.2), 9.4, 1.5, boxstyle="round,pad=0.2",
                              facecolor=NAVY, edgecolor='none'))
ax.text(5, 8.95, "QUIZ", fontsize=16, ha='center', color=WHITE, weight='bold')
ax.text(5, 7.3, "다음 중 노트북LM의 소스 기반 설계\n원칙에 해당하는 것은?",
        ha='center', va='center', fontsize=11, color=NAVY_DARK, weight='bold')

options = ["A. 인터넷 전체를 검색하여 답변한다",
           "B. 사용자가 올린 소스만 참조하여 답변한다",
           "C. 학습 데이터를 기반으로 창작한다",
           "D. 실시간 웹 크롤링으로 답변한다"]
for i, opt in enumerate(options):
    y = 5.8 - i * 1.2
    is_correct = (i == 1)
    bg = EMERALD if is_correct else GRAY_100
    tc = WHITE if is_correct else GRAY_700
    ax.add_patch(FancyBboxPatch((1.2, y - 0.4), 7.6, 0.8, boxstyle="round,pad=0.1",
                                  facecolor=bg, edgecolor=GRAY_200 if not is_correct else 'none',
                                  linewidth=0.5))
    ax.text(5, y, opt, ha='center', va='center', fontsize=10, color=tc,
            weight='bold' if is_correct else 'normal')
save_fig(fig, 26)

# ── 그림 27: 맥킨지 스타일 슬라이드 레이아웃 ──
fig, ax = plt.subplots(1, 1, figsize=(12, 7))
ax.set_xlim(0, 16); ax.set_ylim(0, 11); ax.axis('off')
fig.patch.set_facecolor(BG)
_title(ax, 8, 10.5, "맥킨지 스타일 슬라이드 레이아웃")

# 슬라이드 프레임 (그림자)
ax.add_patch(FancyBboxPatch((1.1, 0.4), 14, 9, boxstyle="round,pad=0.05",
                              facecolor='#00000008', edgecolor='none'))
ax.add_patch(FancyBboxPatch((1, 0.5), 14, 9, boxstyle="round,pad=0.05",
                              facecolor=WHITE, edgecolor=GRAY_300, linewidth=1.5))
# 상단 15% — 헤드라인
ax.add_patch(patches.Rectangle((1, 8.2), 14, 1.3, facecolor=NAVY_DARK, edgecolor='none'))
ax.text(8, 8.85, "국내 SaaS 시장은 전년 대비 23% 성장, 2027년까지 연평균 19% 성장 전망",
        ha='center', va='center', fontsize=9, color=WHITE, weight='bold')
ax.text(15.5, 8.85, "15%", ha='center', va='center', fontsize=8, color=GOLD, weight='bold')

# 중앙 70%
ax.add_patch(FancyBboxPatch((1.5, 1.8), 6.2, 6, boxstyle="round,pad=0.1",
                              facecolor=BG_SUBTLE, edgecolor=GRAY_200, linewidth=0.5))
ax.text(4.6, 4.8, "[차트 영역]\n막대 그래프", ha='center', va='center', fontsize=10, color=GRAY_400)
ax.add_patch(FancyBboxPatch((8.2, 1.8), 6.3, 6, boxstyle="round,pad=0.1",
                              facecolor=BG_SUBTLE, edgecolor=GRAY_200, linewidth=0.5))
ax.text(11.35, 6.2, "핵심 수치:", ha='center', va='center', fontsize=10, color=NAVY_DARK, weight='bold')
ax.text(11.35, 4.5, "  2025년 시장 규모: 4.2조 원\n  2026년 예상: 5.2조 원 (+23%)\n  연평균 성장률: 19%",
        ha='center', va='center', fontsize=9, color=GRAY_700, linespacing=1.6)
ax.text(15.5, 4.8, "70%", ha='center', va='center', fontsize=8, color=GOLD, weight='bold')

# 하단 15%
ax.add_patch(patches.Rectangle((1, 0.5), 14, 1.3, facecolor=GRAY_100, edgecolor='none'))
ax.text(2.2, 1.15, "출처: 한국소프트웨어산업협회, 2026", fontsize=8, color=GRAY_500)
ax.text(14, 1.15, "12", fontsize=8, ha='right', color=GRAY_500)
ax.text(15.5, 1.15, "15%", ha='center', va='center', fontsize=8, color=GOLD, weight='bold')
save_fig(fig, 27)

# ── 그림 28: 3단계 레이어링 프롬프트 ──
create_flow_chart(28, "3단계 레이어링 프롬프트 워크플로우",
    ["1단계\n구조 잡기\n(헤드라인)", "2단계\n상세 채우기\n(근거/데이터)", "3단계\n시각화\n(슬라이드 생성)"],
    "구조에서 상세로, 상세에서 시각화로")

# ── 그림 29: 인포그래픽 Before/After ──
create_comparison(29, "인포그래픽 사용 전 / 사용 후",
    "텍스트 나열", [
        "매출 12.3억 원",
        "신규 고객 47명",
        "이탈률 3.2%",
        "NPS 67점",
    ],
    "인포그래픽", [
        "매출 막대그래프 + 증감 화살표",
        "고객 아이콘 47개 시각화",
        "이탈률 원형 차트",
        "NPS 게이지 차트",
    ])

# ── 그림 30~35: 플로우차트 ──
create_flow_chart(30, "\"표 먼저, 글 나중에\" 워크플로우",
    ["소스\n업로드", "데이터표\n생성", "노트로\n저장", "보고서\n초안 요청", "최종\n편집"],
    "정리된 생각은 보고서가 된다")

create_flow_chart(31, "CSPO 프롬프트 공식",
    ["맥락\n(Context)\n나는 누구인가", "상황\n(Situation)\n지금 무엇을 하는가", "목적\n(Purpose)\n무엇을 원하는가", "출력 형식\n(Output)\n어떤 형태로"],
    "이 네 가지를 넣으면 답이 달라진다")

create_flow_chart(32, "회의 녹음에서 후속 조치까지",
    ["녹음\n시작", "노트북LM\n업로드", "3단계\n프롬프트", "액션 아이템\n표 생성", "후속 메일\n자동 작성"],
    "회의가 끝나면, AI가 정리를 시작한다")

create_flow_chart(33, "경쟁사 분석 전체 워크플로우",
    ["소스 수집\n(IR, 뉴스\n블로그)", "개별\n분석", "교차\n비교표", "전략\n인사이트\n도출", "딥 리서치로\n최신 동향\n추가"],
    "비교에서 전략까지, 한 번의 흐름으로")

create_flow_chart(34, "고객 피드백 분석 프로세스",
    ["데이터 수집\n(설문, 리뷰\nCS, NPS)", "감성 분석\n(긍정/부정)", "불만 분류\n(TOP 5)", "강점 확인\n패턴 발견", "인사이트\n보고서"],
    "100개의 피드백에서 패턴을 찾는다")

create_flow_chart(35, "신입 온보딩 지식베이스 구축",
    ["사내 규정\n매뉴얼\nFAQ 업로드", "맞춤 지시\n설정", "팀 AI 비서\n구축", "플래시카드\n퀴즈 생성", "노트북\n공유 설정"],
    "한 번 가르치면, 100번 물어도 된다")

# ── 그림 36: 주간 워크플로우 ──
create_timeline(36, "주간 업무 워크플로우",
    [("소스 업데이트", "5분\n최신 자료 교체"),
     ("분석 질문", "10분\n핵심 인사이트 추출"),
     ("산출물 생성", "5분\n슬라이드/표 자동 생성"),
     ("최종 검토", "5분\n팩트체크 확인")])

# ── 그림 37: 팀 도입 저항과 대응 ──
create_card_grid(37, "팀 도입 시 흔한 저항 4가지와 대응법",
    [("\"또 새 도구야?\"", "강요 없이 결과를 보여준다\n직접 써본 사례 공유"),
     ("\"보안은 괜찮아?\"", "Google 데이터 정책 설명\n모델 학습에 미사용"),
     ("\"AI 잘 모르는데\"", "5분 데모로 시작\n어려운 건 나중에"),
     ("\"지금도 잘 하는데\"", "시간 절감 수치 제시\n사용 전/사용 후 비교")])

# ── 그림 38: AI 도구 선택 플로우차트 ──
fig, ax = plt.subplots(1, 1, figsize=(13, 8))
ax.set_xlim(-0.5, 13); ax.set_ylim(-0.5, 9); ax.axis('off')
fig.patch.set_facecolor(BG)
_title(ax, 6.25, 8.5, "AI 도구 선택 의사결정 플로우")

# 박스 크기
_bw, _bh = 3.2, 1.0
# 열 중심 좌표
_c1, _c2, _c3 = 1.6, 6.25, 10.9
# 행 Y 좌표
_y_start = 6.5
_y_question = 4.2
_y_answer = 1.8

# 시작 박스
add_rounded_box(ax, 6.25 - _bw/2, _y_start, _bw, _bh, "이 작업에\n어떤 AI를 쓸까?", NAVY_DARK, WHITE, 12)

# 분기 1: 내 자료를 분석해야 하나?
add_rounded_box(ax, _c1 - _bw/2, _y_question, _bw, _bh, "내 자료를\n분석해야 하나?", GOLD, WHITE, 11)
add_arrow(ax, 6.25, _y_start, _c1, _y_question + _bh, GRAY_400)

# Yes → 노트북LM
add_rounded_box(ax, _c1 - _bw/2, _y_answer, _bw, _bh, "노트북LM", TEAL, WHITE, 13)
ax.text(_c1, _y_question - 0.35, "Yes", fontsize=11, ha='center', color=EMERALD, weight='bold')
add_arrow(ax, _c1, _y_question, _c1, _y_answer + _bh, EMERALD)

# No → 분기 2: 최신 정보가 필요한가?
add_rounded_box(ax, _c2 - _bw/2, _y_question, _bw, _bh, "최신 정보가\n필요한가?", GOLD, WHITE, 11)
ax.text((_c1 + _bw/2 + _c2 - _bw/2) / 2, _y_question + _bh/2 + 0.3, "No", fontsize=11, ha='center', color=CORAL, weight='bold')
add_arrow(ax, _c1 + _bw/2, _y_question + _bh/2, _c2 - _bw/2, _y_question + _bh/2, CORAL)

# Yes → Perplexity
add_rounded_box(ax, _c2 - _bw/2, _y_answer, _bw, _bh, "Perplexity", STEEL, WHITE, 13)
ax.text(_c2, _y_question - 0.35, "Yes", fontsize=11, ha='center', color=EMERALD, weight='bold')
add_arrow(ax, _c2, _y_question, _c2, _y_answer + _bh, EMERALD)

# No → 분기 3: 창의적 생성이 필요한가?
add_rounded_box(ax, _c3 - _bw/2, _y_question, _bw, _bh, "창의적 생성이\n필요한가?", GOLD, WHITE, 11)
ax.text((_c2 + _bw/2 + _c3 - _bw/2) / 2, _y_question + _bh/2 + 0.3, "No", fontsize=11, ha='center', color=CORAL, weight='bold')
add_arrow(ax, _c2 + _bw/2, _y_question + _bh/2, _c3 - _bw/2, _y_question + _bh/2, CORAL)

# Yes → ChatGPT
add_rounded_box(ax, _c3 - _bw/2, _y_answer, _bw, _bh, "ChatGPT", CORAL, WHITE, 13)
ax.text(_c3, _y_question - 0.35, "Yes", fontsize=11, ha='center', color=EMERALD, weight='bold')
add_arrow(ax, _c3, _y_question, _c3, _y_answer + _bh, EMERALD)

# 하단 안내
_subtitle(ax, 6.25, 0.3, "핵심: 내 자료 분석 = 노트북LM, 최신 검색 = Perplexity, 창의적 생성 = ChatGPT")
save_fig(fig, 38)

# ── 그림 39: 일주일 루틴 ──
create_timeline(39, "팀장의 노트북LM 일주일 루틴",
    [("월", "주간 보고\n자료 분석"),
     ("화", "회의록 정리\n액션 아이템"),
     ("수", "경쟁사/시장\n동향 분석"),
     ("목", "팀 보고서\n초안 작성"),
     ("금", "주간 리뷰\n다음 주 준비")])

# ── 그림 40: 30분 데모 스크립트 ──
create_timeline(40, "팀에 처음 소개할 때: 30분 데모 스크립트",
    [("0~5분", "왜 노트북LM\n인가?"),
     ("5~15분", "함께\n해보기"),
     ("15~25분", "우리 팀\n적용 시나리오"),
     ("25~30분", "Q&A")])

print("=" * 50)
print(f"40개 그림 생성 완료! → {IMG_DIR}")
print("=" * 50)

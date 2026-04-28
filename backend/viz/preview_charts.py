"""
대시보드 미리보기용 차트 생성 (조장이 한 번 실행)
- 팀원 C가 본격 작업하기 전에 골격에 들어갈 샘플 차트 4종 생성
- 출력: web/images/01~04 .png
"""
import sys
from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"
OUT = ROOT / "web" / "images"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.alpha"] = 0.25

PALETTE = ["#6c5ce7", "#ff7eb6", "#00cec9", "#fdcb6e", "#e17055", "#74b9ff", "#a29bfe"]


def chart_01_overview():
    df = pd.read_csv(DATA / "trend_raw.csv")
    df["period"] = pd.to_datetime(df["period"])
    plt.figure(figsize=(11, 5.5))
    sns.lineplot(data=df, x="period", y="ratio", hue="keyword",
                 marker="o", linewidth=2.2, palette=PALETTE[:7])
    plt.title("7개 SNS 유행 음식 - 월별 검색 트렌드", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel(""); plt.ylabel("검색 상대 비율")
    plt.legend(title="", loc="upper left", bbox_to_anchor=(1.01, 1), fontsize=9)
    plt.tight_layout()
    plt.savefig(OUT / "01_overview.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("✅ 01_overview.png")


def chart_02_age_heatmap():
    df = pd.read_csv(DATA / "trend_age.csv")
    pivot = df.groupby(["keyword", "age"])["ratio"].mean().reset_index()
    mat = pivot.pivot(index="keyword", columns="age", values="ratio")
    age_order = ["10대", "20대", "30대", "40대", "50대 이상"]
    mat = mat[age_order]
    plt.figure(figsize=(9, 5))
    sns.heatmap(mat, annot=True, fmt=".2f", cmap="RdPu",
                cbar_kws={"label": "평균 검색 비율"}, linewidths=0.4)
    plt.title("키워드별 연령대 검색 강도", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel(""); plt.ylabel("")
    plt.tight_layout()
    plt.savefig(OUT / "02_age_heatmap.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("✅ 02_age_heatmap.png")


def chart_03_gender():
    df = pd.read_csv(DATA / "trend_gender.csv")
    summary = df.groupby(["keyword", "gender"])["ratio"].mean().reset_index()
    plt.figure(figsize=(10, 5))
    sns.barplot(data=summary, x="keyword", y="ratio", hue="gender",
                palette={"남성": "#74b9ff", "여성": "#ff7eb6"})
    plt.title("키워드별 성별 검색 비중 (평균)", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel(""); plt.ylabel("평균 검색 비율")
    plt.legend(title="")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(OUT / "03_gender.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("✅ 03_gender.png")


def chart_04_device():
    df = pd.read_csv(DATA / "trend_device.csv")
    summary = df.groupby(["keyword", "device"])["ratio"].mean().reset_index()
    plt.figure(figsize=(10, 5))
    sns.barplot(data=summary, x="keyword", y="ratio", hue="device",
                palette={"모바일": "#6c5ce7", "PC": "#fdcb6e"})
    plt.title("모바일 vs PC - 키워드별 검색 비중", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel(""); plt.ylabel("평균 검색 비율")
    plt.legend(title="")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(OUT / "04_device.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("✅ 04_device.png")


if __name__ == "__main__":
    chart_01_overview()
    chart_02_age_heatmap()
    chart_03_gender()
    chart_04_device()
    print("─" * 40)
    print("미리보기 차트 4개 생성 완료")

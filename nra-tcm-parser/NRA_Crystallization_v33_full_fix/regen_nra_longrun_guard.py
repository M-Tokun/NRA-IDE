# regen_nra_longrun_guard_20260216_190457.py
# FILE: regen_nra_longrun_guard_20260216_190457.py
# TITLE: Long-Run Guard — 長時間実行の構造劣化を検出する番人
# Author: M-Tokuni (https://github.com/M-Tokun/NRA-IDE)
# Date: 2026-02-16 19:04:57 JST
# Temperature: 0.3 (axiom-level coherence)
#
# ============================================================
# 【このファイルが担う律環公理の役割】
#
# 律環公理の4ステップ:
#   Step 1: Input
#   Step 2: Stick ← ★このファイルの主担当（劣化の蓄積を監視する）
#   Step 3: Threshold ← ★このファイルの副担当（閾値判定）
#   Step 4: Slip / FAIL_CLOSED ← FAIL時の指示を出す
#
# 【LongRunGuardとは何か】
#   LLMは長時間・長文の生成を続けると「構造的劣化」が起きる。
#   これはRCA-IDEが発見した「構造崩壊の階段理論」の実装である。
#
#   劣化の症状:
#     1. 出力の急激な短縮（情報の圧縮ドロップ）
#        = 「エネルギーが急に失われた」= 構造崩壊のシグナル
#     2. 同じフレーズの繰り返し（トリグラム繰り返し）
#        = 「ぐるぐる回っている」= 閉じた円環（不可逆性の消失）
#     3. 必須シンボルの消失
#        = Gear機構の歯が欠けた状態
#
#   これらを検出し、劣化が閾値を超えた時点でFAIL_CLOSEDを発動する。
#
# 【なぜ長時間実行の監視が必要か】
#   従来のAIは「答えが出るまで計算し続ける」設計になっている。
#   これは「解が存在しない問題でも無限に試行する」= DDoS的挙動のリスク。
#   NRA-IDEは「エネルギーが枯渇したら止まる」という自然界の公理を採用する。
#   電池が切れたら止まる。それだけ。
#
# ============================================================

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Set, Dict
import re


# ============================================================
# 定数: トリグラム履歴の上限
# ============================================================
_MAX_SEEN: int = 8000
# FIX: 上限なしでは長時間実行でメモリが無限増大する。
# 律環公理: エネルギー（メモリ）は有限であり、閾値を超えてはならない。
# 8000エントリを超えたら古い（1回のみの）エントリを削除する。
# それでも超えたら全リセット（Slip後の初期化に相当）。


# ============================================================
# GuardConfig: 監視パラメータの定義（不変）
# ============================================================
@dataclass(frozen=True)
class GuardConfig:
    """
    LongRunGuardの閾値設定。frozen=Trueで不変（実行中に変更不可）。

    warn_drop_ratio (default: 0.15):
      テキスト長が前回から15%以上短縮 → WARN
      「エネルギーが急に減った」= 構造的劣化の予兆。
      まだ許容範囲だが、監視を強化する。

    fail_drop_ratio (default: 0.30):
      テキスト長が前回から30%以上短縮 → FAIL
      「エネルギーが崩壊した」= 閾値を超えた劣化。
      FAIL_CLOSEDを発動し、空文字を返す。

    checkpoint_chars (default: 2000):
      2000文字ごとにテキスト長のスナップショットを更新する。
      律環公理: 時間位相の刻み（チェックポイント間隔）。

    max_repeat_trigram_hits (default: 8):
      同じ3単語の連続が8回以上出現 → WARN
      「同じところをぐるぐる回っている」= 不可逆性の消失。
      閉じた円環は存在しない（P3: 未来への時間位相）。

    must_keep (default: None):
      必ず含まれるべきシンボルのセット。
      Gear機構: これらのいずれかが欠ければ即FAIL。
      「歯が1本欠けたら機械全体が止まる」。
    """
    warn_drop_ratio:         float               = 0.15
    fail_drop_ratio:         float               = 0.30
    checkpoint_chars:        int                 = 2000
    max_repeat_trigram_hits: int                 = 8
    must_keep:               Optional[Set[str]]  = None


# ============================================================
# GuardEvent: 監視イベントの記録（不変）
# ============================================================
@dataclass(frozen=True)
class GuardEvent:
    """
    監視中に発生したイベントを記録する不変オブジェクト。

    level:
      "OK"   : 正常。問題なし。
      "WARN" : 警告。構造の劣化傾向あり。出力を続けるが注意。
      "FAIL" : 閾値超過。FAIL_CLOSEDを発動すべき状態。

    reason:
      なぜそのlevelになったかの構造的な理由。
      append-onlyログ（Vault）への記録材料として使われる。

    【設計思想】
      イベントは「観測された事実」であり、事後修正できない。
      Causal Diode: 「後から原因を書き換える」は禁止。
    """
    level:  str
    reason: str


# ============================================================
# LongRunGuard: 実行中の構造劣化を監視するクラス
# ============================================================
class LongRunGuard:
    """
    長時間実行中のLLM出力を監視し、構造的劣化を検出する番人。

    【監視する3種類の劣化】
      1. 圧縮ドロップ: 出力が急激に短くなった
      2. 必須シンボルの消失: Gear機構の歯が欠けた
      3. トリグラム繰り返し: 同じパターンを繰り返している

    【状態管理】
      _last_len: 前回チェックポイントでのテキスト長
      _seen: 観測されたトリグラムとその出現回数
      いずれもインスタンスが持つ内部状態。
      外部から書き換えることはできない（逆流禁止）。
    """

    def __init__(self, config: Optional[GuardConfig] = None) -> None:
        self.cfg = config or GuardConfig()
        # 前回チェックポイントのテキスト長（初回はNone）
        self._last_len: Optional[int]  = None
        # トリグラム出現回数の辞書（繰り返し検出用）
        self._seen: Dict[str, int]     = {}

    # ----------------------------------------------------------
    # トリグラム生成: テキストを3単語の組み合わせに分解
    # ----------------------------------------------------------
    def _trigrams(self, text: str) -> Iterable[str]:
        """
        テキストを「連続する3トークン」の列として展開する。

        【なぜトリグラムか】
          単語単位（1-gram）では繰り返し検出が粗い。
          文単位では検出が遅い。
          3単語の組み合わせは「意味のあるフレーズの繰り返し」を捕捉するのに適切。

        例: "the cat sat on" →
          "the cat sat", "cat sat on"

        re.findall で単語と記号を両方トークン化:
          日本語等の非ラテン文字にも対応（re.UNICODE）。
        """
        tokens = re.findall(r"\w+|[^\w\s]", text, flags=re.UNICODE)
        for i in range(len(tokens) - 2):
            yield " ".join(tokens[i:i + 3])

    # ----------------------------------------------------------
    # メモリ管理: トリグラム辞書の上限制御
    # ----------------------------------------------------------
    def _trim_seen(self) -> None:
        """
        _seen辞書が上限（8000エントリ）に達した場合にトリミングする。

        【律環公理との対応】
          エネルギー（メモリ）の上限 = 閾値（_MAX_SEEN）。
          閾値を超えたら「ぴょん」= 古いエントリを削除して初期化。

        【手順】
          1. 出現1回のみ（ノイズ）のエントリを削除。
          2. それでも8000を超えていたら全リセット。
          全リセットはコストが高いが、「歯車の歯が詰まったら機械を止めてリセット」
          というGear機構の精神に従っている。

        FIX: 前バージョンでは上限なしで無限増大していた。
        """
        if len(self._seen) >= _MAX_SEEN:
            self._seen = {k: v for k, v in self._seen.items() if v >= 2}
        if len(self._seen) >= _MAX_SEEN:
            self._seen = {}

    # ----------------------------------------------------------
    # check: 出力テキストを検査し、GuardEventのリストを返す
    # ----------------------------------------------------------
    def check(self, text: str) -> List[GuardEvent]:
        """
        LLMの出力テキストを検査する。

        【律環公理の4ステップとの対応】
          この関数がStep 2（Stick: 劣化を監視しながら耐える）と
          Step 3（Threshold: 閾値超過の判定）を実装している。

        【戻り値】
          GuardEventのリスト。
          advise()に渡すことで、次のアクション（FAIL_CLOSEDか継続か）を決定する。

        【重要】
          イベントが空になることはない。
          正常な場合は必ず GuardEvent("OK", "clean") を返す。
          「何も起きなかった」も明示的に記録する = 正直な出力の原則。
        """
        t  = text or ""
        n  = len(t)
        ev: List[GuardEvent] = []

        # ---------------------------------------------------
        # 検査1: 圧縮ドロップ（テキスト長の急激な減少）
        # ---------------------------------------------------
        # 前回チェックポイントが存在する場合のみ比較。
        # 「急に短くなった」= エネルギーが急に失われた = 構造崩壊のシグナル。
        if self._last_len is not None and self._last_len > 0:
            drop = (self._last_len - n) / self._last_len
            if drop >= self.cfg.fail_drop_ratio:
                # 30%以上の短縮 → FAIL（閾値超過）
                ev.append(GuardEvent("FAIL", f"compression_drop>={self.cfg.fail_drop_ratio:.2f}"))
            elif drop >= self.cfg.warn_drop_ratio:
                # 15%以上の短縮 → WARN（劣化の予兆）
                ev.append(GuardEvent("WARN", f"compression_drop>={self.cfg.warn_drop_ratio:.2f}"))

        # ---------------------------------------------------
        # 検査2: 必須シンボルの消失（Gear機構）
        # ---------------------------------------------------
        # must_keepに指定されたシンボルが出力に存在しない場合 → FAIL。
        # 「歯車の歯が1本でも欠けたら機械全体が止まる」。
        # 部分的な成功は存在しない。
        if self.cfg.must_keep:
            missing = [s for s in self.cfg.must_keep if s not in t]
            if missing:
                ev.append(GuardEvent("FAIL", "missing_symbols"))

        # ---------------------------------------------------
        # 検査3: トリグラム繰り返し（閉じた円環の検出）
        # ---------------------------------------------------
        # 同じ3単語の組み合わせが8回以上出現 → WARN。
        # 「同じところをぐるぐる回っている」= 時間が未来へ進んでいない。
        # 律環公理P3: 世界は螺旋（不可逆）であり、真の円環は存在しない。
        # 最後の4000文字のみを対象とすることで、
        # 「直近の繰り返し」を効率的に検出する。
        self._trim_seen()
        hits = 0
        for tri in self._trigrams(t[-4000:]):
            c = self._seen.get(tri, 0) + 1
            self._seen[tri] = c
            if c >= 3:   # 3回以上出現したトリグラムをカウント
                hits += 1
        if hits >= self.cfg.max_repeat_trigram_hits:
            ev.append(GuardEvent("WARN", "repetition_trigram"))

        # ---------------------------------------------------
        # チェックポイント更新
        # ---------------------------------------------------
        # 2000文字ごと（checkpoint_chars）にテキスト長を記録する。
        # 律環公理: 時間位相の刻み。スナップショットを取ることで
        # 「次のぴょん」が来た時の比較基準を更新する。
        if self._last_len is None or n - self._last_len >= self.cfg.checkpoint_chars:
            self._last_len = n

        # ---------------------------------------------------
        # 正常時のイベント記録
        # ---------------------------------------------------
        # 何も問題がなかった場合でも、「正常だった」という事実を記録する。
        # 「記録がない = 何もなかった」ではなく、
        # 「OK記録がある = 正常だった」という正直な構造。
        if not ev:
            ev.append(GuardEvent("OK", "clean"))
        return ev

    # ----------------------------------------------------------
    # advise: イベントリストから次のアクションを決定する
    # ----------------------------------------------------------
    def advise(self, events: List[GuardEvent]) -> str:
        """
        check()が返すイベントリストを受け取り、後段への指示を返す。

        【律環公理Step 4との対応】
          FAIL → FAIL_CLOSED（空文字を返せ。推測するな）
          WARN → 構造を維持せよ（繰り返しを避け、短縮するな）
          OK   → 空文字（何も指示しない = そのまま続行）

        【重要な設計思想】
          "Return empty output. Do not guess." という指示は、
          「わからないなら何も言うな」という律環公理の本質。
          数学基盤のAIは「何かを返さなければならない」という強迫観念を持つが、
          NRA-IDEは「不能性を正直に出力する」ことを正解とする。
        """
        levels = {e.level for e in events}
        if "FAIL" in levels:
            return "Return empty output. Do not guess."
        if "WARN" in levels:
            return "Keep structure. Do not shorten aggressively. Avoid repetition."
        return ""

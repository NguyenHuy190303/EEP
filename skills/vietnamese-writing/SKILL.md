---
name: vietnamese-writing
description: Use before writing ANY Vietnamese prose — an ops-ledger record in docs/decisions/ or docs/problems/, a spec page, a postmortem, a standup entry, a commit body, or a reply after Huy switches to Vietnamese. Default output language is English; this skill loads only when Vietnamese is actually being produced. Holds the senior-engineer register, the four mechanisms that produce translationese, the glossary of banned calques taken from real corrections, and the terms that always stay English.
---

# Vietnamese technical writing

Scope: **technical prose between Huy and me only** — ledger records, specs, postmortems, standup,
commit bodies. Not administrative Vietnamese, not customer-facing copy, not công văn / tờ trình.
Huy does not write those and this skill must not drift into that register.

Root cause this fixes: my Vietnamese defaults to a close translation of an English sentence
skeleton rather than how a Vietnamese engineer actually talks.

**The check that replaces memorizing the lists below:** read the sentence out loud. If nobody in
the room would say it that way, rewrite it.

## Register

Senior engineer / tech lead talking in a review: short, blunt, anchored on numbers and the real
mechanism. No narrative, no build-up. Technical terms stay English — never force a calque for a
word people say in English on the job.

## The four mechanisms that produce translationese

**1. Passive carried over from English.** English leans on the passive (*is done by*, *was decided
by*); translating it literally yields "được thực hiện bởi", "được xem như là". Go active, or drop
the auxiliary when context already makes the actor obvious.

| Không | Có |
|---|---|
| Báo cáo này được chuẩn bị bởi team infra | **Team infra lập báo cáo này** |
| Lỗi được phát hiện bởi Sentry lúc 14:02 | **Sentry bắt được lỗi lúc 14:02** |
| Pod được kỳ vọng là sẽ sẵn sàng sau 30 giây | **Dự kiến pod sẵn sàng sau 30 giây** |
| Vấn đề này được xem như là một rủi ro lớn | **Đây là rủi ro lớn** |

**2. Nominalization — "việc / sự / quá trình / tính".** English turns verbs into nouns (*the
implementation of*, *in the process of*). Vietnamese leaves the verb standing. Delete the filler.

| Không | Có |
|---|---|
| Việc thực hiện tối ưu hóa cơ sở dữ liệu là cần thiết | **Cần tối ưu database** |
| Trong quá trình tiến hành đo tải | **Khi đo tải** |
| Sự thành công của việc migrate phụ thuộc vào | **Migrate có chạy được hay không phụ thuộc vào** |
| Chúng tôi tập trung vào việc giảm latency | **Chúng tôi tập trung giảm latency** |

**3. English filler phrases translated word by word.**

| English | Không dịch thô | Có |
|---|---|---|
| plays an important role in | đóng một vai trò quan trọng trong việc | **then chốt đối với** / **quyết định** |
| provides a solution for | cung cấp một giải pháp cho | **giải quyết** / **xử lý** |
| take into consideration | đưa vào sự xem xét cân nhắc | **cân nhắc** |
| in order to | để mà có thể thực hiện được | **để** / **nhằm** |
| make sure that | đảm bảo chắc chắn rằng | **cần đảm bảo** / **lưu ý** |
| first and foremost | trước hết và quan trọng nhất | **trước hết** |
| at the end of the day | vào cuối ngày | **suy cho cùng** / **rốt cuộc** |

Same family, block these too:

- **"Một cách + tính từ"** — the English `-ly` suffix carried over. "Chạy một cách ổn định" →
  **chạy ổn định**.
- **Dummy subject + "rằng"** — "Điều quan trọng cần lưu ý là chúng ta có thể thấy rằng…". Vietnamese
  drops subjects freely and almost never needs "rằng".
- **Redundant doublets** — *nhanh chóng và hiệu quả*, *rõ ràng và minh bạch*, *đầy đủ và chính xác*.
  Drop one half; the meaning survives.
- **Calling the reader "bạn"** — an artifact of English having only *you*. Use anh/em, or drop the
  pronoun entirely.
- **Every sentence the same length.** Twenty-odd words each, no rhythm. Break it with a short one.

**4. Bureaucratic word where a plain one exists.** "tiến hành thực hiện" → *làm*; "nhằm mục đích" →
*để*; "trong trường hợp" → *nếu*; "tại thời điểm hiện tại" → *hiện giờ*; "có nhu cầu" → *cần*;
"trong thời gian tới" → *sắp tới*; "thực hiện việc rà soát" → *rà soát*.

## Never translate — always English

- **Infra & deployment:** Pod, Node, Cluster, Ingress, Worker, Pool, Quota, CFS, TTL, HPA, ArgoCD,
  Helm, deploy, release, rollback, replica.
- **Metrics & tracing:** Latency, Throughput, Round-trip, Scrape, Metric, P95/P99, Gauge,
  Sum/Count, histogram.
- **ML/AI:** Tensor, Shape, Batching, Embedding, Weight, CUDA context, NMS, Graph, inference,
  checkpoint.

Command names, flags, paths, env vars, metric names, Kubernetes object names, ticket IDs, branch
names: 100% verbatim, even mid-Vietnamese-sentence.

## Banned calques — from real corrections in this workspace

This table grows from corrections that actually happened. Add to it rather than re-deriving the
same fix twice.

| Không | Có |
|---|---|
| Đường găng | **Critical path** / **Bottleneck** |
| DEV-người / PROD-thật | **Dev (Manual test)** / **Prod (Real-traffic)** |
| Công nghệ thật | **Tech stack** |
| Suy luận | **Inference** |
| Vòng đệm | **Buffer** / **Frame buffer** |
| Khung hình bị vứt | **Frame dropped** |
| Nguội dần | **Score decay** / **Cooldown** |
| Trần cứng | **Hard limit** / **Concurrency cap** |
| Máy phát tải | **Load generator** |

## Structure of a spec, ledger record, or postmortem

Open on a number, a table, or the technical finding. No lead-in ("Trong tài liệu này chúng ta
sẽ…", "Chắc chắn rồi!"), no polite sign-off ("Hy vọng thông tin trên hữu ích"), no restating the
question before answering it.

Analysing a failure or a bottleneck: three sections, kept apart —
**Observation** (what was measured, on which environment) →
**Root cause** (with the evidence) →
**Action item** (who, by when).

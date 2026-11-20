## 11. Two-week study plan
## 11. Kế hoạch học hai tuần

The plan follows the blueprint weights (Domain 2 first, then Domain 1) and ends with timed simulations. Adjust the order to your weakest domains. **(Strategy)**
Kế hoạch bám theo tỷ trọng blueprint (Domain 2 trước, rồi Domain 1) và kết thúc bằng các bài mô phỏng có giới hạn thời gian. Hãy đổi thứ tự theo domain yếu nhất của bạn. **(Chiến lược)**

| Day / Ngày | Focus / Trọng tâm | Output / Kết quả |
|---|---|---|
| 1 | Section 0 + Domain 2: reliability engineering, stop_reason handling, retries, circuit breakers / Mục 0 + Domain 2: độ tin cậy, xử lý stop_reason, retry, circuit breaker | Can classify any failure (429, 529, length, refusal, context window) and name its handling / Phân loại được mọi loại lỗi và nêu cách xử lý |
| 2 | Domain 2: throughput, Batches, MCP in production, change management, retrieval and grounding / Domain 2: throughput, Batches, MCP production, quản lý thay đổi, retrieval và grounding | Diagnose a retrieval failure stage by stage / Chẩn đoán lỗi retrieval theo từng giai đoạn |
| 3 | Domain 1: multi-agent orchestration, durable execution / Domain 1: điều phối đa agent, durable execution | Decide workflow vs agent vs multi-agent with reasons / Chọn workflow, agent hay multi-agent kèm lý do |
| 4 | Domain 1: architecture selection, context and memory architecture / Domain 1: chọn kiến trúc, kiến trúc context và memory | Pick a context policy for a long-running agent / Chọn chính sách context cho agent chạy lâu |
| 5 | Domain 3 + Domain 4: telemetry, SLIs/SLOs, trace analysis, diagnosis, incident response / Domain 3 + 4: telemetry, SLI/SLO, phân tích trace, chẩn đoán, xử lý sự cố | Draw a trace/metric plan for one agent; walk through an incident / Vẽ kế hoạch trace/metric cho một agent; đi qua một sự cố |
| 6 | Domain 5: eval design, LLM-as-judge calibration, online measurement / Domain 5: thiết kế eval, hiệu chỉnh LLM-as-judge, đo online | Explain why a judge is not trusted yet and how to calibrate it / Giải thích vì sao judge chưa đáng tin và cách hiệu chỉnh |
| 7 | Domain 7: guardrails, threat defense, identity and secrets / Domain 7: guardrail, phòng thủ mối đe dọa, danh tính và secret | Apply "remove a leg of the trifecta" to three scenarios / Áp dụng "gỡ một mắt xích của bộ ba rủi ro" vào ba tình huống |
| 8 | Domain 6 + Domain 8: cost and latency; fleets, code review, unattended agents, org config / Domain 6 + 8: chi phí và latency; fleet, code review, agent không giám sát, cấu hình tổ chức | Compute a cache break-even; design a shadow-mode review rollout / Tính điểm hòa vốn của cache; thiết kế triển khai review ở shadow mode |
| 9 | Interactive Quiz by domain: Domains 2, 1, 7 / Quiz theo domain: 2, 1, 7 | Review every miss in the Explanatory Study / Xem lại mọi câu sai trong Explanatory Study |
| 10 | Interactive Quiz by domain: Domains 3, 4, 5, 6, 8 / Quiz theo domain: 3, 4, 5, 6, 8 | Note the Golden Rules you keep missing / Ghi lại các Golden Rule hay sai |
| 11 | **Exam Simulation #1** (120 min) / **Mô phỏng thi #1** (120 phút) | Read every wrong and flagged item; update weak-domain notes / Đọc lại mọi câu sai và câu flag; cập nhật ghi chú domain yếu |
| 12 | Re-read Sections 9 and 10 (traps and Golden Rules); do the hands-on checklist below / Đọc lại Mục 9 và 10 (bẫy và Golden Rules); làm checklist thực hành bên dưới | Can state each Golden Rule and its typical distractor / Nêu được từng Golden Rule và đáp án nhiễu điển hình |
| 13 | **Exam Simulation #2**, then targeted review / **Mô phỏng thi #2**, rồi ôn mục tiêu | Readiness check / Kiểm tra mức sẵn sàng |
| 14 | Light review; logistics: ID name matches registration, reschedule windows, quiet room for OnVUE / Ôn nhẹ; thủ tục: tên trên ID khớp đăng ký, thời hạn đổi lịch, phòng yên tĩnh cho OnVUE | Rest / Nghỉ ngơi |

### Hands-on checklist (from the official "How to Prepare")
### Checklist thực hành (theo mục "How to Prepare" của exam guide chính thức)
The Exam Guide recommends operating **at least one tool-using Claude agent in production** with the following. If you cannot, build a small one and practise each item. **(Doc)**
Exam Guide khuyến nghị vận hành **ít nhất một agent Claude dùng tool trên production** với các thành phần dưới đây. Nếu chưa có, hãy dựng một agent nhỏ và thực hành từng mục. **(Doc)**

- [ ] Distributed tracing and cost telemetry (tokens including cache read/creation, request-id) / Distributed tracing và telemetry chi phí (token gồm cache read/creation, request-id)
- [ ] SLIs and SLOs with alerts (TTFT, total latency, error classes, cost per task, quality) / SLI và SLO kèm cảnh báo (TTFT, tổng latency, các loại lỗi, chi phí mỗi task, chất lượng)
- [ ] An evaluation suite that gates releases (golden set + regression suite in CI) / Bộ eval làm cổng phát hành (golden set + regression suite trong CI)
- [ ] Layered guardrails (input/output filters, deterministic blocks for irreversible actions, approval gates, sandbox) / Guardrail nhiều lớp (lọc input/output, chặn tất định cho hành động không đảo ngược, approval gate, sandbox)
- [ ] An incident-response and postmortem practice that feeds new regression evals / Quy trình xử lý sự cố và postmortem có đưa kết quả vào regression eval mới
- [ ] A fallback design that separates rate limits, refusals and context-window stops / Thiết kế fallback tách riêng rate limit, refusal và hết context window
- [ ] A calibrated LLM-as-judge (agreement with human labels measured) / LLM-as-judge đã hiệu chỉnh (đo độ khớp với nhãn của con người)
- [ ] A context and memory policy for a long-running agent / Chính sách context và memory cho agent chạy lâu
- [ ] A red-team exercise against a tool-using agent that reads untrusted content / Bài red-team cho agent dùng tool có đọc nội dung không tin cậy
- [ ] Parallel coding agents on isolated worktrees, plus an unattended run with caps / Agent lập trình song song trên worktree cô lập, cùng một lần chạy không giám sát có giới hạn

# CCDV-P Study Guide — Bilingual (English / Tiếng Việt)

**Claude Certified Developer – Professional (exam code CCDVP) · Exam Guide v1.0, effective November 2026**
**Chứng chỉ Claude Certified Developer – Professional (mã thi CCDVP) · Exam Guide v1.0, hiệu lực tháng 11/2026**

> **Independent study material, not affiliated with or endorsed by Anthropic.** Exam facts in Section 0 and the domain blueprint come from the official *Claude Certified Developer – Professional Exam Guide v1.0* (PDF published by Anthropic, Nov 2026). Technical facts in the modules were researched from Anthropic's public documentation and other sources on **2026-11-20** and are tagged **(Doc)** = supported by official documentation, **(Interp)** = interpretation / widely used practice, **(Unverified)** = could not be confirmed, **(3rd party)** = non-Anthropic source. Product behaviour, limits and prices change quickly: re-check the current documentation before relying on any number.
>
> **Tài liệu tự học độc lập, không liên kết hay được Anthropic bảo trợ.** Thông tin kỳ thi ở Mục 0 và blueprint domain lấy từ *Exam Guide v1.0 chính thức* (PDF do Anthropic phát hành, 11/2026). Các fact kỹ thuật trong module được research từ tài liệu công khai của Anthropic và nguồn khác vào **20/11/2026**, gắn nhãn **(Doc)** = có trong tài liệu chính thức, **(Interp)** = diễn giải / thực hành phổ biến, **(Unverified)** = chưa xác minh được, **(3rd party)** = nguồn ngoài Anthropic. Hành vi sản phẩm, giới hạn và giá thay đổi nhanh: hãy kiểm tra lại tài liệu hiện hành trước khi dựa vào bất kỳ con số nào.

## How to use this pack
## Cách dùng bộ tài liệu này

| File | Purpose / Mục đích |
|---|---|
| `CCDV-P_Study_Guide.md` | This guide: exam facts, 8 domain modules, cross-domain traps, 30 Golden Rules, study plan. / Tài liệu này: thông tin kỳ thi, 8 module domain, bẫy liên domain, 30 Golden Rules, kế hoạch học. |
| `CCDV-P_Interactive_Quiz.html` | Practice by question, instant feedback, filter by domain. / Luyện từng câu, phản hồi ngay, lọc theo domain. |
| `CCDV-P_Exam_Simulation.html` | Timed 120-minute simulation, flag and navigate, domain breakdown at the end. / Mô phỏng thi 120 phút, đánh dấu câu và điều hướng, thống kê theo domain khi nộp bài. |
| `CCDV-P_Explanatory_Interactive_Study.html` | Pick an answer, then flip to see the exam pattern, why each wrong option fails and the Golden Rules triggered. / Chọn đáp án rồi lật xem exam pattern, vì sao các đáp án sai thua và Golden Rule liên quan. |

**Recommended order / Thứ tự khuyến nghị:** read Section 0 and the module of your weakest domain → attempt the Explanatory Study for that domain → Quiz by domain → at least two Exam Simulations in the last week.
Đọc Mục 0 và module của domain yếu nhất → làm Explanatory Study cho domain đó → Quiz theo domain → ít nhất hai lần Exam Simulation trong tuần cuối.

## 0. Exam at a glance
## 0. Tổng quan kỳ thi

- **Positioning:** Foundations asks *"can you build it?"*; Professional asks ***"can you run it?"*** The candidate is accountable for reliability, quality, cost and safety of **live** Claude systems and has operated at least one tool-using agent in production. The Developer – Foundations scope is **assumed knowledge**.
- **Định vị:** Foundations hỏi *"bạn có xây được không?"*; Professional hỏi ***"bạn có vận hành được không?"*** Thí sinh chịu trách nhiệm về độ tin cậy, chất lượng, chi phí và an toàn của hệ thống Claude **đang chạy thật** và đã vận hành ít nhất một agent dùng tool trên production. Phạm vi Developer – Foundations được coi là **kiến thức nền**.

- **Format:** **70 items (60 scored + 10 unscored, unscored items are not identified)**, scenario-based **multiple-choice and multiple-response** (each item states how many answers to select), **120 minutes**, proctored (online via OnVUE or test center, through Pearson VUE), **US$175** per attempt, **no prerequisite** (Developer – Foundations recommended).
- **Hình thức:** **70 câu (60 tính điểm + 10 không tính điểm, câu không tính điểm không được đánh dấu)**, câu tình huống **multiple-choice và multiple-response** (mỗi câu ghi rõ chọn mấy đáp án), **120 phút**, có giám thị (online qua OnVUE hoặc tại test center của Pearson VUE), **US$175** mỗi lần thi, **không có điều kiện tiên quyết** (khuyến nghị có Developer – Foundations).

- **Scoring:** criterion-referenced, scaled **100–1,000, pass at 720** (a fixed standard, not a curve and **not "72% correct"**). The score report shows percent-correct per domain, but **only the overall scaled score decides pass/fail**. Don't compute your score mid-exam; the safe plan is broad coverage of every objective.
- **Chấm điểm:** criterion-referenced, thang **100–1.000, đậu ở 720** (chuẩn cố định, không chấm theo đường cong và **không phải "đúng 72%"**). Báo cáo điểm có phần trăm đúng theo domain nhưng **chỉ tổng điểm quy đổi quyết định đậu/rớt**. Đừng tính điểm giữa chừng; cách an toàn là phủ đủ mọi objective.

- **Timing:** about **1 min 43 s per item** (120 min ÷ 70). Because 10 items are unscored and unmarked, **give every item full effort**. Read the last sentence and the *number of answers to select* first, underline constraints, **eliminate options that violate a hard constraint**, then compare the survivors on the stated priority (cause vs symptom, prevention vs detection, deterministic vs probabilistic). Stuck after ~2 minutes: pick the best guess, flag, move on **(Strategy)**.
- **Thời gian:** khoảng **1 phút 43 giây mỗi câu** (120 phút ÷ 70). Vì có 10 câu không tính điểm và không được đánh dấu, **hãy làm hết sức cho mọi câu**. Đọc câu cuối và *số đáp án cần chọn* trước, gạch chân ràng buộc, **loại phương án vi phạm ràng buộc cứng**, rồi so các phương án còn lại theo ưu tiên đã nêu (nguyên nhân hay triệu chứng, ngăn chặn hay phát hiện, tất định hay xác suất). Kẹt quá ~2 phút: chọn tạm, flag, đi tiếp **(Chiến lược)**.

- **Retakes & renewal:** wait **14 → 30 → 90 days** after the 1st/2nd/3rd failed attempt, **max 4 attempts per rolling 12 months**, each retake pays the fee. Valid **12 months**; on-time renewal is a **free, non-proctored assessment** on the Partner Academy; a lapsed credential means a full paid retake, and Anthropic may require the full exam if content changes significantly.
- **Thi lại & gia hạn:** chờ **14 → 30 → 90 ngày** sau lần rớt thứ 1/2/3, **tối đa 4 lần trong 12 tháng cuốn chiếu**, mỗi lần thi lại đều tính phí. Hiệu lực **12 tháng**; gia hạn đúng hạn là bài đánh giá **miễn phí, không giám thị** trên Partner Academy; để hết hạn = thi lại toàn bộ có phí, và Anthropic có thể yêu cầu thi lại toàn bộ nếu nội dung thay đổi đáng kể.

- **Logistics:** register on the Anthropic Partner Academy, then continue to Pearson. Reschedule or cancel **online exams up to 1 hour** and **test-center exams up to 48 hours** before the appointment, otherwise the fee is forfeited. The **name on the government photo ID must match the registration exactly**. Exam content is confidential (NDA): do not capture, copy or disclose any live exam content.
- **Thủ tục:** đăng ký trên Anthropic Partner Academy rồi chuyển sang Pearson. Đổi hoặc hủy lịch **thi online trước tối đa 1 giờ** và **thi tại test center trước 48 giờ**, nếu muộn hơn sẽ mất phí. **Tên trên giấy tờ có ảnh phải khớp chính xác với tên đăng ký.** Nội dung đề thi là bí mật (NDA): không chụp, sao chép hay tiết lộ bất kỳ nội dung đề thi thật nào.

### Blueprint (official) / Blueprint (chính thức)

| # | Domain | Weight | ≈ scored items of 60 |
|---|---|---|---|
| 1 | Advanced Agent Architecture and Orchestration | 17% | ~10 |
| **2** | **Production Integration, Reliability, and Knowledge Grounding** | **20% (largest / lớn nhất)** | **~12** |
| 3 | Observability and Production Monitoring | 12% | ~7 |
| 4 | Advanced Debugging and Incident Response | 10% | ~6 |
| 5 | Evaluation Engineering and Quality Assurance | 12% | ~7 |
| 6 | Cost and Latency Optimization at Scale | 8% | ~5 |
| 7 | Runtime Guardrails and Production Security | 11% | ~7 |
| 8 | Agent Fleet Operations for Software Delivery | 10% | ~6 |

- **Reading the weights:** they are the approximate share of **scored** items per domain, so expect cross-domain items where several constraints must hold at once. Domains 1 and 2 together are **37%**.
- **Cách đọc tỷ trọng:** là tỷ lệ xấp xỉ của các câu **tính điểm** theo domain, nên sẽ có câu liên domain phải thỏa nhiều ràng buộc cùng lúc. Domain 1 và 2 cộng lại chiếm **37%**.

### What the exam is not / Kỳ thi không phải là gì
- It is **not** a coding or lab exam: items test **design, diagnosis and operating decisions** in production scenarios, usually with four plausible fixes where the right one addresses the **cause** and the distractors address **symptoms**.
- Đây **không** phải bài thi code hay lab: các câu kiểm tra **quyết định thiết kế, chẩn đoán và vận hành** trong tình huống production, thường có bốn cách sửa nghe đều hợp lý, trong đó đáp án đúng xử lý **nguyên nhân** còn các đáp án nhiễu xử lý **triệu chứng**.

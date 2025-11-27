import dash
from dash import html, dcc
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import numpy as np

dash.register_page(__name__, path="/story", name="Data Storytelling")

# =============================
# LOAD DATA
# =============================
df = pd.read_excel("data/data0979_enriched.xlsx")
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.month
df["Year"] = df["Date"].dt.year

# =============================
# FIGURES (10 PLOTS)
# =============================

# 1. Histogram
fig_ch1_hist = px.histogram(
    df,
    x="Total_Order_Demand",
    nbins=50,
    title="Histogram of Total_Order_Demand",
    color_discrete_sequence=["#003f7f"],
)
fig_ch1_hist.update_layout(template="plotly_white")

# 2. Boxplot
fig_ch1_box = px.box(
    df,
    y="Total_Order_Demand",
    title="Boxplot of Total_Order_Demand",
    color_discrete_sequence=["#001f3f"],
)
fig_ch1_box.update_layout(template="plotly_white")

# 3. Daily demand over time
fig_ch2 = px.line(
    df,
    x="Date",
    y="Total_Order_Demand",
    title="Daily Demand Over Time",
    color_discrete_sequence=["#001f3f"],
)
fig_ch2.update_layout(template="plotly_white")

# 4. Demand by Promotion (boxplot)
fig_ch3 = px.box(
    df,
    x="Promotion",
    y="Total_Order_Demand",
    title="Demand by Promotion",
    color="Promotion",
    color_discrete_sequence=["#001f3f", "#003f7f"],
)
fig_ch3.update_layout(template="plotly_white")

# 5–8. Seasonal lines: Winter, Spring, Summer, Autumn
fig_winter = px.line(
    df[df["Season"] == "Winter"],
    x="Date",
    y="Total_Order_Demand",
    title="Winter (Dec–Jan–Feb)",
    color_discrete_sequence=["#5DADE2"],
)
fig_winter.update_layout(template="plotly_white")

fig_spring = px.line(
    df[df["Season"] == "Spring"],
    x="Date",
    y="Total_Order_Demand",
    title="Spring (Mar–Apr–May)",
    color_discrete_sequence=["#58D68D"],
)
fig_spring.update_layout(template="plotly_white")

fig_summer = px.line(
    df[df["Season"] == "Summer"],
    x="Date",
    y="Total_Order_Demand",
    title="Summer (Jun–Jul–Aug)",
    color_discrete_sequence=["#F4D03F"],
)
fig_summer.update_layout(template="plotly_white")

fig_autumn = px.line(
    df[df["Season"] == "Autumn"],
    x="Date",
    y="Total_Order_Demand",
    title="Autumn (Sep–Oct–Nov)",
    color_discrete_sequence=["#EB984E"],
)
fig_autumn.update_layout(template="plotly_white")

# 9. Monthly mean
monthly_mean = df.groupby("Month")["Total_Order_Demand"].mean().reset_index()
fig_ch5 = px.line(
    monthly_mean,
    x="Month",
    y="Total_Order_Demand",
    markers=True,
    title="Mean Total Order Demand by Month",
    color_discrete_sequence=["#7D3C98"],
)
fig_ch5.update_layout(template="plotly_white", xaxis=dict(dtick=1))

# 10. Correlation matrix
corr = df[["Total_Order_Demand", "Order_Count", "Holiday", "Black_Friday", "Promotion"]].corr()
fig_ch6 = ff.create_annotated_heatmap(
    z=corr.values,
    x=list(corr.columns),
    y=list(corr.index),
    colorscale="PuBu",
    showscale=True,
)
fig_ch6.update_layout(title="Correlation Matrix", template="plotly_white")

# =============================
# FULL STORY TEXT (6 CHAPTERS)
# =============================

chapter1_text = """
Một sáng đẹp trời ở **Cloud Town**, Cinnamoroll đang nhâm nhi cacao nóng thì *bịch!* –  
một vật gì đó rơi từ trên… **Excel** xuống.

Đó là một chiếc **đồng hồ thời gian** màu vàng nhạt, bên trong quay tít những con số `2012 → 2016`.

Chiếc đồng hồ thì thầm:

> “Tớ giữ bí mật của **Product_0979**.  
> 5 năm lịch sử nhu cầu, đầy biến động, đầy những câu chuyện chưa kể…  
> Cinnamoroll, cậu giúp tớ kể lại nhé?”

Và **VỤT!**  
Hai bạn bị hút vào **Time Series World** – thế giới nơi:

- dữ liệu trở thành **phong cảnh**  
- *demand* trở thành **thời tiết**  
- *spikes* trở thành **pháo hoa**

Cinnamoroll nhìn thấy một “**dòng sông**” màu xanh kéo dài 5 năm.  
Nhưng không phải dòng sông hiền hòa. Nó:

- khi thì phẳng lì như tờ giấy (*demand = 0*)
- khi thì dồn dập như bão biển
- khi thì dâng cao như thủy triều (*spike 10.000–20.000*)
- khi thì bùng nổ như lễ hội ánh sáng

Cinnamoroll chớp mắt:

> “Ơ!? Sao trông giống đồ thị… **stress của BA cuối kỳ** quá vậy?”

Chiếc đồng hồ cười:

> “Welcome to **B2B Bulk Order World**,  
> nơi nhu cầu không đi theo *trend*… mà theo **EVENTS**.”

Và thế là **hành trình bắt đầu**.  """


chapter2_text = """
Gió nhẹ thổi trên những đám mây pastel.  
Cinnamoroll ngồi trên chiếc cloud mềm như bông, hai tai dài đung đưa theo gió,  
nhìn xuống bầu trời **Demandland** bên dưới.

Thật lạ.

Một vùng trời rộng lớn… nhưng **im lặng**.  
Không có pháo hoa dữ liệu.  
Không có cột sáng.  
Không có tín hiệu.  
Chỉ là những con số **0** trải dài bất tận, như cỏ phủ sương sớm.

Cinnamoroll nghiêng đầu:

> “Sao… chẳng có ai mua gì hết vậy?  
> Hay là hệ thống bị lỗi?”

Chiếc đồng hồ bật cười:

> “Không phải lỗi đâu bé.  
> Trong suốt 5 năm, gần **40% số ngày** đều như vậy đó.  
> Đây là bản chất của thị trường **B2B Bulk Order**.”

Cinna tròn mắt:

> “Ý là… không mua gì mới là… **bình thường**?”

Đồng hồ gật đầu:

> “Đúng. Trong B2B, khách hàng **không mua từng ngày**,  
> họ mua *khi cần*, và mua **theo lô lớn**.  
> Thế nên những ngày không mua gì chiếm số lượng rất lớn.”

Cinnamoroll mở sổ tay pastel, bắt đầu ghi:

- “**Demand = Zero-Inflated.**”
- “**Không đơn ≠ lỗi**, mà là **tín hiệu**.”
- “**B2B không giống FMCG.**”
- “**Baseline gần như = 0.**”

Và rồi bạn nhìn rõ hơn:

- 🌫️ Những ngày *Demand = 0* nằm rải rác như sương mù, kéo dài hàng tuần  
- 🌫️ Đôi khi cả tháng chỉ có vài ngày sáng nhẹ  
- 🌫️ Và khi một ngày có ánh sáng mạnh, thì đó không phải bất thường – mà là **đặc trưng** của thị trường

Cinnamoroll bỗng hiểu:

> “Vậy hóa ra dữ liệu không ồn ào là một dạng câu chuyện…  
> Là những tháng mà thị trường đang thở chậm, nghỉ ngơi,  
> chuẩn bị cho những đợt mua lớn sau đó.”

#### 📌 INSIGHT BUSINESS

- Không thể đặt KPI theo hướng **“doanh thu đều hằng ngày”**  
- B2B hoạt động theo:
  - **dự án**
  - **ngân sách**
  - **quý**
  - **năm tài chính**
  - **event**
- Doanh nghiệp phải đo hiệu quả **theo sự kiện**, không phải **theo thời gian thuần tuý**

#### 📌 INSIGHT BUSINESS ANALYST

Dữ liệu quá nhiều số 0 khiến BA phải:
- ✔ tránh dùng mô hình yêu cầu **Gaussian**  
- ✔ dùng **metrics** phù hợp (*MAE tốt hơn MSE* trong bối cảnh nhiều outlier/zero)

#### 📌 INSIGHT SUPPLY CHAIN

Không thể lên kế hoạch **nhập hàng đều đặn**.

Mô hình tồn kho phải chuyển sang dạng:

- ✔ “**sẵn sàng cho đột biến**” thay vì “bơm đều mỗi ngày”

Nếu:

- Dự trữ đều → **tồn kho cao**  
- Không chuẩn bị trước event → **hết hàng ngay lập tức**

Cinnamoroll nhắm mắt lại, cảm nhận sự im lặng kinh tế của bầu trời Demandland.  
Và bạn mỉm cười:

> “**Im lặng cũng là dữ liệu.  
> Im lặng kể câu chuyện về cách thị trường vận hành.**”

"""


chapter3_text = """
Một tối trời trong, Cinnamoroll đang nằm trên đám mây nhìn sao.

Bất chợt…

> **BOOM!!!**

Một cột sáng xanh lam rực rỡ bắn lên tận đỉnh trời Demandland.

Cinnamoroll nhảy dựng lên:

> “CÁI GÌ VẬY!?  
> Nó tăng gấp **hai mươi lần** luôn á!?”

Rồi **BOOM BOOM BOOM!**  
Những ánh sáng khác nối tiếp nhau như trời đang tổ chức **lễ hội pháo hoa**.

Chiếc đồng hồ bật cười:

> “Đó đó! Chính là những ngày **spike demand**!”

Cinna nghiêng tai:

> “Vì sao? Vì… người ta đột nhiên thích mua nhiều hả?”

Chiếc đồng hồ khẽ vỗ đầu bạn nhỏ:

> “Không đâu, mọi **spike** đều có lý do.  
> Đó là: **Promotion – Clearance – Black Friday – Bulk Order – Budget Flush.**”


#### 💥 CÁC LOẠI *SPIKE* Ở DEMANDLAND

##### ⭐ 1. Spike do **Promotion**

Khi công ty tung ra chương trình khuyến mãi,  
*demand* “nhảy lên” như Cinnamoroll vừa uống cà phê espresso:

- **Promotion days** tăng nhu cầu gấp *3–10 lần*  
- Tương quan với Demand ~ **0.89** – cực mạnh  
- Là **tín hiệu mạnh nhất** trong toàn dataset  

Đồng hồ nói:

> “**Promotion** chính là người bạn **tâm giao** của *Demand*.”

---

##### ⭐ 2. Spike do **Bulk Order** (khách doanh nghiệp lớn)

- Một khách B2B đặt 1 đơn = bằng **cả tuần bán lẻ**  
- Spike đến từ **dự án**, không đến từ nhu cầu tiêu dùng lẻ tẻ

Cinna nhìn thấy một “**con rồng đơn hàng**” khổng lồ bay qua trời:

> “Ơ cái đơn hàng đó to như… **máy bay** luôn!?”

---

##### ⭐ 3. Spike do **Black Friday**

- Đỉnh màu vàng rực rỡ, sáng nhất trong tất cả các spike  
- Nhu cầu tăng gấp **3 lần** so với ngày lễ thông thường  
- Là sự kiện **không thể bỏ qua**

---

##### ⭐ 4. Spike do **Clearance cuối quý**

- Thường xuất hiện tháng **9** và tháng **12**

---

##### ⭐ 5. Spike do **Budget Flush** (xả ngân sách cuối năm)

- Doanh nghiệp cố gắng **tiêu hết ngân sách** trước khi năm tài chính kết thúc

---

Cinnamoroll ôm chiếc đồng hồ:

> “Vậy thị trường này không phải tăng tự nhiên…  
> mà tăng nhờ **sự kiện** đúng không?”

Đồng hồ gật mạnh:

> “Đúng vậy, Cinna.  
> Đây là thị trường **event-driven**,  
> nghĩa là mô hình **Time Series thuần tuý** không thể hiểu nếu không có **event features**.”


#### 📌 INSIGHT BUSINESS

- Đầu tư vào **Promotion** → hiệu quả **rõ rệt**  
- Nếu giảm ngân sách marketing → doanh thu có thể **rơi tự do**  
- ROI cao nhất khi tập trung vào:
  - **Black Friday**
  - **End-of-quarter sales**
  - **Mid-year campaign**

#### 📌 INSIGHT BUSINESS ANALYST

BA phải phân tích:

- **Promotion uplift**
- **Incremental sales**
- **Spike attribution**

*Spike* = tín hiệu để:

- phân khúc **khách hàng lớn**  
- làm **Key Account Analysis**

#### 📌 INSIGHT SUPPLY CHAIN

- Phải **dự trữ trước spike 2–4 tuần**  
- Nếu không → **out-of-stock** → mất revenue  
- Sau spike phải chuẩn bị:
  - **replenishment**
  - **logistics turnaround**

Cinnamoroll viết đầy một trang:

> “**Spike ≠ lỗi.  
> Spike = tín hiệu của những ngày quan trọng nhất năm.**”
"""


chapter4_text = """
Cinnamoroll đeo chiếc đồng hồ và bay lên cao hơn nữa.

Lần này bạn đi qua từng **mùa**, và mỗi mùa trong Demandland có **tính cách riêng**.


#### ❄️ WINTER — Mùa Ngân Sách & Sương Mờ

Winter xuất hiện với chiếc khăn len, tuyết nhẹ rơi:

> “Ta là Winter.  
> Ta không mạnh như Autumn,  
> nhưng **tháng 12** của ta… lúc nào cũng bùng cháy.”

**Đặc điểm Winter:**

- Tháng **12**: spike do **budget flush**  
- Tháng **1–2**: thị trường ngủ đông, cực ít đơn  
- Dao động “lúc rất cao, lúc rất thấp”

**INSIGHT BUSINESS:**

- Doanh thu **tháng 12** rất quan trọng  
- Jan–Feb có thể **focus on retention** (giữ khách, chăm sóc)

**INSIGHT SUPPLY CHAIN:**

- Chuẩn bị kho mạnh cho **tháng 12**  
- Giảm OPEX (chi phí vận hành) ở **tháng 1–2**

#### 🌸 SPRING — Mùa Ngủ Quên & Baseline Yếu

Spring ngáp dài trên đám mây pastel:

> “Tớ mệt. Tớ muốn ngủ thêm một chút…”

**Đặc điểm Spring:**

- Mùa **yếu nhất**  
- Gần như toàn bộ demand = 0  
- Không có chu kỳ mạnh  
- Spike cực kỳ hiếm

**INSIGHT BUSINESS:**

- Không nên tập trung chạy **chiến dịch lớn**  
- Ưu tiên **bảo trì hệ thống**, cải thiện nội lực

**INSIGHT SUPPLY CHAIN:**

Thời điểm hoàn hảo cho:

- bảo trì kho  
- tối ưu vận hành  
- tinh chỉnh logistics

#### ☀️ SUMMER — Mùa Hồi Sinh Nhẹ & Dao Động Dịu

Summer nhảy nhót trên nắng vàng:

> “Tớ không bùng nổ nhưng tớ **tươi mới**!”

**Đặc điểm Summer:**

- Spike **tầm trung**  
- Nhu cầu **tăng nhẹ**  
- Là mùa **chuẩn bị cho Autumn**


#### 🍂🔥 AUTUMN — Mùa Bùng Nổ, Lễ Hội & Doanh Thu Đỉnh

Autumn xoay vòng trong lá vàng, tỏa ánh sáng vàng rực:

> “Xin chào, tớ là mùa của **tất cả mọi thứ**.”

**Đặc điểm Autumn:**

- **Peak demand**  
- Spike **dày nhất**  
- Spike **cao nhất**  
- Gom: **Black Friday + Q3–Q4 buying**

**INSIGHT BUSINESS:**

- 50–70% doanh thu năm có thể nằm ở **Autumn**  
- Chiến lược bán hàng phải **dồn lực tối đa** vào mùa này

**INSIGHT SUPPLY CHAIN:**

- **Full-stock**  
- **Workforce tăng cường**  
- **Logistics chạy công suất tối đa**


Cinnamoroll ghi chú:

> “**Mùa không phải chỉ là thời gian.  
> Mùa là mô hình hành vi.**”

"""


chapter5_text = """
/// Trên cao hơn nữa, Cinna nhìn xuống **“Rainbow Curve”** – biểu đồ demand theo **tháng**.

Mỗi tháng như một **nhân vật**:

- **Tháng 3–4**: buồn bã → baseline thấp  
- **Tháng 5–7**: hồi phục → nhẹ nhàng  
- **Tháng 9–11**: bùng nổ → *peak*  
- **Tháng 12**: dư âm cuối năm → vẫn mạnh


#### 📌 INSIGHT BUSINESS

- **Peak trung bình** = tháng **10**  
- **Bottom** = tháng **4**  

→ Chiến lược:

- Đầu tư chiến dịch mạnh vào **Q4 (đặc biệt tháng 10)**  
- Q2 (nhất là tháng 4) → phù hợp với chương trình **nhẹ nhàng, tối ưu chi phí**

#### 📌 INSIGHT SUPPLY CHAIN

- **Q4** = căng nhất (nhiều demand, nhiều spike)  
- **Q2** = nhẹ nhất (phù hợp bảo trì, tái cấu trúc vận hành)

Cinnamoroll vẽ một chiếc cầu vồng lên notebook:

> “**Monthly demand** giống một vòng cung –  
> đỉnh nằm ở **Q4**.”

"""


chapter6_text = """
Trong một khu rừng dữ liệu, Cinna gặp một tấm gương tròn lớn – **Correlation Matrix**.

Tấm gương nói:

> “Tớ sẽ cho cậu biết **ai là bạn của ai**.”

Và rồi từng mối quan hệ hiện ra:

- **Promotion ♥ Demand**: 0.89  
- **Order Count ↗ Demand**: 0.53  
- **Holiday & Black Friday → ≈ 0** do tần suất nhỏ  

**Promotion** có sức mạnh vượt trội.

#### 📌 INSIGHT BUSINESS

- Tăng ngân sách **promotion** = tăng doanh thu **lớn**  
- Chạy promo đúng mùa (**Autumn**) → hiệu quả **x3**


#### 📌 INSIGHT BA (Business Analyst)

Không được:

- bỏ biến **Promotion** trong mô hình  
- suy luận **Holiday** không quan trọng chỉ vì **low correlation**  
  → vì tần suất ít nhưng *impact* có thể **rất lớn** theo event


#### 📌 INSIGHT SUPPLY CHAIN

- Tăng demand trong ngày có **promotion** phải được **dự báo chính xác**  
- Nếu không dự báo:
  - → **thiếu hàng**  
  - → **tổn thất lớn** cả doanh thu lẫn uy tín


Cinnamoroll mỉm cười trước tấm gương:

> “Hóa ra dữ liệu có những **mối quan hệ vô hình**…  
> chỉ cần biết nhìn, chúng sẽ hiện rõ.”

"""


# =============================
# LAYOUT: COVER → CHAPTERS
# =============================

layout = html.Div(
    className="page fade-in",
    children=[

        # COVER IMAGE + TAGLINE
        html.Div(
            style={"textAlign": "center", "marginBottom": "30px"},
            children=[
                html.Img(
                    src="/assets/cinnamoroll_cover.png",
                    style={
                        "width": "60%",
                        "maxWidth": "500px",
                        "borderRadius": "20px",
                        "boxShadow": "0 4px 12px rgba(0,0,0,0.15)",
                        "marginBottom": "20px",
                    },
                ),
                html.H3(
                    "✨ Hiểu dữ liệu qua câu chuyện của Cinnamoroll nhé ✨",
                    style={
                        "fontFamily": "'Quicksand', sans-serif",
                        "fontSize": "22px",
                        "color": "#6b6ba3",
                        "marginTop": "10px",
                        "marginBottom": "40px",
                        "fontWeight": "600",
                    },
                ),
            ],
        ),

        html.H2(
            "📖 Data Storytelling - kể chuyện qua dữ liệu cùng Cinnamoroll nhé!",
            className="section-title",
        ),

        # ========== CHƯƠNG 1 ==========
        html.H3("CHƯƠNG 1 — Cinnamoroll & Chiếc Đồng Hồ Thời Gian", className="story-title"),
        dcc.Graph(figure=fig_ch1_hist, className="chart-box"),
        dcc.Graph(figure=fig_ch1_box, className="chart-box"),
        html.Div(
            className="story-block",
            children=[dcc.Markdown(chapter1_text)],
        ),

        # ========== CHƯƠNG 2 ==========
        html.H3("CHƯƠNG 2 — Những Ngày Im Lặng Trên Bầu Trời Demand", className="story-title"),
        dcc.Graph(figure=fig_ch2, className="chart-box"),
        html.Div(
            className="story-block",
            children=[dcc.Markdown(chapter2_text)],
        ),

        # ========== CHƯƠNG 3 ==========
        html.H3("CHƯƠNG 3 — Hội Chợ Promotion & Các Cụm Bắn Vọt", className="story-title"),
        dcc.Graph(figure=fig_ch3, className="chart-box"),
        html.Div(
            className="story-block",
            children=[dcc.Markdown(chapter3_text)],
        ),

        # ========== CHƯƠNG 4 ==========
        html.H3("CHƯƠNG 4 — Hành Trình Qua 4 Mùa Demand", className="story-title"),
        dcc.Graph(figure=fig_winter, className="chart-box"),
        dcc.Graph(figure=fig_spring, className="chart-box"),
        dcc.Graph(figure=fig_summer, className="chart-box"),
        dcc.Graph(figure=fig_autumn, className="chart-box"),
        html.Div(
            className="story-block",
            children=[dcc.Markdown(chapter4_text)],
        ),

        # ========== CHƯƠNG 5 ==========
        html.H3("CHƯƠNG 5 — Cầu Vồng 12 Tháng", className="story-title"),
        dcc.Graph(figure=fig_ch5, className="chart-box"),
        html.Div(
            className="story-block",
            children=[dcc.Markdown(chapter5_text)],
        ),

        # ========== CHƯƠNG 6 ==========
        html.H3(" CHƯƠNG 6 — Cinnamoroll Gặp Correlation Matrix", className="story-title"),
        dcc.Graph(figure=fig_ch6, className="chart-box"),
        html.Div(
            className="story-block",
            children=[dcc.Markdown(chapter6_text)],
        ),
    ],
)


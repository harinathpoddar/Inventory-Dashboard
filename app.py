import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Product Inventory & Analytics Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# USER AUTHENTICATION (EXCEL/CSV BASED)
# ---------------------------------------------------------
USER_DATA_FILE = "users.csv"

def load_users():
    if os.path.exists(USER_DATA_FILE):
        return pd.read_csv(USER_DATA_FILE)
    else:
        # Default Admin Account
        df_users = pd.DataFrame([{"username": "admin", "password": "123", "email": "admin@example.com"}])
        df_users.to_csv(USER_DATA_FILE, index=False)
        return df_users

def save_user(username, password, email):
    df_users = load_users()
    new_user = pd.DataFrame([{"username": username, "password": password, "email": email}])
    df_users = pd.concat([df_users, new_user], ignore_index=True)
    df_users.to_csv(USER_DATA_FILE, index=False)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = ""

# ---------------------------------------------------------
# CUSTOM STYLING (GOLDEN YELLOW, SKY BLUE & RESPONSIVE)
# ---------------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #E0F7FA 0%, #FFFDE7 50%, #FFFFFF 100%);
        color: #1A252C;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #00B4DB 0%, #0083B0 70%, #F4C430 100%) !important;
        border-right: None;
    }

    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] .stMarkdown h1, 
    [data-testid="stSidebar"] .stMarkdown h2, 
    [data-testid="stSidebar"] .stMarkdown h3,
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] span {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }

    .stTextInput input, .stNumberInput input, .stSelectbox > div {
        background-color: #FFFFFF !important;
        color: #004D40 !important;
        border: 2px solid #00B4DB !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    /* Sidebar Header / Title Style */
[data-testid="stSidebar"] h1 {
    font-family: 'Arial', sans-serif !important; /* Font style change karein */
    font-size: 20px !important;                 /* Font size change karein */
    color: #FFFFFF !important;                  /* Font color change karein */
    font-weight: bold !important;
}

    .main-header {
        background: linear-gradient(135deg, #0083B0 0%, #00B4DB 50%, #FFD700 100%);
        padding: 25px;
        border-radius: 16px;
        box-shadow: 0 8px 25px rgba(0, 180, 219, 0.3);
        margin-bottom: 25px;
        text-align: center;
    }
    .main-header h1 {
        color: #FFFFFF !important;
        font-weight: 900;
        font-size: 2.3rem;
        margin: 0;
        letter-spacing: 0.5px;
    }
    .main-header p {
        color: #FFFDE7 !important;
        font-size: 1.1rem;
        margin-top: 8px;
        margin-bottom: 0;
        font-weight: 600;
    }

    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #FFFFFF 0%, #E0F7FA 100%) !important;
        border: 2px solid #FFD700 !important;
        padding: 16px !important;
        border-radius: 14px !important;
        box-shadow: 0 6px 18px rgba(0, 180, 219, 0.15) !important;
    }
    div[data-testid="metric-container"] label {
        color: #006064 !important;
        font-size: 0.9rem !important;
        font-weight: 800 !important;
    }
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #0083B0 !important;
        font-size: 1.8rem !important;
        font-weight: 900 !important;
    }

    .section-title {
        color: #006064;
        font-size: 1.35rem;
        font-weight: 800;
        margin-top: 25px;
        margin-bottom: 15px;
        border-left: 6px solid #FFD700;
        padding-left: 12px;
        background: linear-gradient(90deg, rgba(255, 215, 0, 0.15) 0%, rgba(255,255,255,0) 100%);
        border-radius: 4px;
    }

    .alert-title {
        color: #D32F2F;
        font-size: 1.35rem;
        font-weight: 800;
        margin-top: 25px;
        margin-bottom: 15px;
        border-left: 6px solid #D32F2F;
        padding-left: 12px;
        background: linear-gradient(90deg, rgba(211, 47, 47, 0.1) 0%, rgba(255,255,255,0) 100%);
        border-radius: 4px;
    }

    .stButton > button {
        background: linear-gradient(90deg, #FFD700 0%, #FFA000 100%) !important;
        color: #004D40 !important;
        border: None !important;
        border-radius: 8px;
        font-weight: 800;
        padding: 12px 24px;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
    }

    .footer-container {
        background: linear-gradient(135deg, #0083B0 0%, #00B4DB 50%, #FFD700 100%);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        color: #FFFFFF;
        margin-top: 35px;
        box-shadow: 0 6px 20px rgba(0, 131, 176, 0.25);
    }
    .footer-container h3 {
        margin: 0;
        font-size: 1.2rem;
        font-weight: 800;
        color: #FFFFFF !important;
    }
    .footer-container p {
        margin: 6px 0 0 0;
        font-size: 1rem;
        font-weight: 600;
        color: #FFFDE7 !important;
    }

    @media only screen and (max-width: 768px) {
        .block-container {
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
            padding-top: 1rem !important;
        }
        .main-header {
            padding: 18px !important;
        }
        .main-header h1 {
            font-size: 1.5rem !important;
        }
        .main-header p {
            font-size: 0.85rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# LOGIN & REGISTER SCREEN
# ---------------------------------------------------------
if not st.session_state.logged_in:
    st.markdown("""
    <div class="main-header">
        <h1>📦 Inventory Management System</h1>
        <p>Please Login or Register to Access the Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

        with tab1:
            st.subheader("Login to Account")
            login_user = st.text_input("Username", key="login_user")
            login_pass = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login"):
                df_users = load_users()
                match = df_users[(df_users['username'] == login_user) & (df_users['password'].astype(str) == login_pass)]
                if not match.empty:
                    st.session_state.logged_in = True
                    st.session_state.user = login_user
                    st.success(f"Welcome {login_user}!")
                    st.rerun()
                else:
                    st.error("Invalid Username or Password!")

        with tab2:
            st.subheader("Create New Account")
            reg_user = st.text_input("New Username", key="reg_user")
            reg_email = st.text_input("Email", key="reg_email")
            reg_pass = st.text_input("New Password", type="password", key="reg_pass")
            if st.button("Register"):
                if reg_user and reg_pass and reg_email:
                    df_users = load_users()
                    if reg_user in df_users['username'].values:
                        st.warning("Username already exists! Choose another.")
                    else:
                        save_user(reg_user, reg_pass, reg_email)
                        st.success("Account Created Successfully! Please Go to Login Tab.")
                else:
                    st.error("Please fill all fields.")

else:
    # ---------------------------------------------------------
    # MAIN DASHBOARD (ACCESSIBLE AFTER LOGIN)
    # ---------------------------------------------------------
    @st.cache_data
    def load_initial_data():
        np.random.seed(42)
        products = [
            "Wireless Optical Mouse", "Mechanical Keyboard RGB", "USB-C Fast Charger 65W",
            "Gaming Headset 7.1", "Full HD Webcam 1080p", "Bluetooth Speaker Portable",
            "External Hard Drive 1TB", "NVMe SSD 512GB", "Smartwatch Fitness Tracker",
            "Ergonomic Desk Chair", "LED Monitor 24-inch", "Dual-Band Wi-Fi Router",
            "Power Bank 20000mAh", "Laptop Cooling Pad", "Graphic Drawing Tablet",
            "Wireless Earbuds ANC", "Smart LED Desk Lamp", "HDMI Cable 4K 2m",
            "Vertical Ergonomic Mouse", "Microphone Condenser Kit"
        ]
        data = []
        for i, p in enumerate(products, 101):
            rec = np.random.randint(50, 200)
            sold = np.random.randint(10, rec)
            curr = rec - sold
            price = np.random.choice([499, 899, 1299, 1799, 2499, 4499, 8999])
            reorder = np.random.randint(10, 40)
            data.append({
                "Product Code": f"PRD-{i}",
                "Product Name": p,
                "Category": np.random.choice(["Peripherals", "Accessories", "Storage", "Audio", "Monitors"]),
                "Stock Received": rec,
                "Stock Sold": sold,
                "Current Stock": curr,
                "Price": price,
                "Inventory Value": curr * price,
                "Reorder Level": reorder
            })
        
        df_init = pd.DataFrame(data)
        df_init.index = range(1, len(df_init) + 1)
        return df_init

    if 'inventory_df' not in st.session_state:
        st.session_state.inventory_df = load_initial_data()

    df = st.session_state.inventory_df
    df.index = range(1, len(df) + 1)

    # SIDEBAR FORM
    with st.sidebar:
        st.title("📥 Stock Management")
        st.write(f"Logged in as: **{st.session_state.user}**")
        
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user = ""
            st.rerun()
            
        st.markdown("---")
        
        with st.form("stock_form", clear_on_submit=True):
            prod_name = st.text_input("Product Name", placeholder="e.g. Wireless Mouse")
            prod_code = st.text_input("Product Code", placeholder="e.g. PRD-101")
            category = st.selectbox("Category", ["Peripherals", "Accessories", "Storage", "Audio", "Monitors"])
            stock_rec = st.number_input("Stock Received", min_value=0, step=1, value=0)
            stock_sold = st.number_input("Stock Sold", min_value=0, step=1, value=0)
            price_unit = st.number_input("Price per Unit (₹)", min_value=0.0, step=10.0, value=0.0)
            reorder_lvl = st.number_input("Reorder Level", min_value=0, step=1, value=10)
            
            submit_btn = st.form_submit_button("💾 Save Record")
            
            if submit_btn:
                if prod_name and prod_code:
                    curr_stk = stock_rec - stock_sold
                    new_data = {
                        "Product Code": prod_code,
                        "Product Name": prod_name,
                        "Category": category,
                        "Stock Received": stock_rec,
                        "Stock Sold": stock_sold,
                        "Current Stock": curr_stk,
                        "Price": price_unit,
                        "Inventory Value": curr_stk * price_unit,
                        "Reorder Level": reorder_lvl
                    }
                    st.session_state.inventory_df = pd.concat([st.session_state.inventory_df, pd.DataFrame([new_data])], ignore_index=True)
                    st.session_state.inventory_df.index = range(1, len(st.session_state.inventory_df) + 1)
                    st.success(f"Added {prod_name} successfully!")
                    st.rerun()
                else:
                    st.error("Please enter Product Name & Code.")

    # HEADER BANNER
    st.markdown("""
    <div class="main-header">
        <h1>📦 Product Inventory & Stock Analytics</h1>
        <p>Real-Time Interactive Business Intelligence Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    # EXECUTIVE OVERVIEW
    st.markdown('<div class="section-title">📊 Executive Overview</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    total_products = len(df)
    total_stock = df["Current Stock"].sum()
    total_valuation = df["Inventory Value"].sum()
    low_stock_df = df[df["Current Stock"] <= df["Reorder Level"]]
    low_stock_count = len(low_stock_df)

    col1.metric("Total Unique Items", f"{total_products}")
    col2.metric("Total Units in Stock", f"{total_stock:,} Units")
    col3.metric("Total Inventory Valuation", f"₹{total_valuation:,.2f}")
    col4.metric("Low Stock Alerts", f"{low_stock_count}", delta_color="inverse")

    st.markdown("---")

    # VISUAL ANALYTICS DASHBOARD
    st.markdown('<div class="section-title">📈 Visual Analytics Dashboard</div>', unsafe_allow_html=True)

    chart_theme = "plotly_white"
    color_sequence = ["#0083B0", "#00B4DB", "#FFD700", "#E6B800", "#FF8F00"]

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=df["Product Name"][:10],
            y=df["Current Stock"][:10],
            name="Current Stock",
            marker_color="#00B4DB"
        ))
        fig1.add_trace(go.Scatter(
            x=df["Product Name"][:10],
            y=df["Reorder Level"][:10],
            name="Reorder Level",
            mode="lines+markers",
            line=dict(color="#FF8F00", width=3, dash="dot")
        ))
        fig1.update_layout(
            title="<b>Stock Levels vs. Reorder Threshold (Top 10)</b>",
            template=chart_theme,
            autosize=True,
            paper_bgcolor='rgba(255,255,255,0.7)',
            plot_bgcolor='rgba(255,255,255,0.7)',
            height=320,
            margin=dict(l=10, r=10, t=40, b=40),
            font=dict(color="#004D40")
        )
        st.plotly_chart(fig1, use_container_width=True)

    with chart_col2:
        cat_df = df.groupby("Category")["Inventory Value"].sum().reset_index()
        fig2 = px.pie(
            cat_df, 
            values="Inventory Value", 
            names="Category",
            title="<b>Valuation Share by Category</b>",
            hole=0.4,
            color_discrete_sequence=color_sequence,
            template=chart_theme
        )
        fig2.update_layout(
            autosize=True,
            paper_bgcolor='rgba(255,255,255,0.7)',
            plot_bgcolor='rgba(255,255,255,0.7)',
            height=320,
            margin=dict(l=10, r=10, t=40, b=40),
            font=dict(color="#004D40")
        )
        st.plotly_chart(fig2, use_container_width=True)

    chart_col3, chart_col4 = st.columns(2)

    with chart_col3:
        fig3 = px.scatter(
            df,
            x="Stock Received",
            y="Stock Sold",
            size="Current Stock",
            color="Category",
            hover_name="Product Name",
            title="<b>Sales Velocity (Received vs Sold)</b>",
            template=chart_theme,
            color_discrete_sequence=color_sequence
        )
        fig3.update_layout(
            autosize=True,
            paper_bgcolor='rgba(255,255,255,0.7)',
            plot_bgcolor='rgba(255,255,255,0.7)',
            height=320,
            margin=dict(l=10, r=10, t=40, b=40),
            font=dict(color="#004D40")
        )
        st.plotly_chart(fig3, use_container_width=True)

    with chart_col4:
        top_val_df = df.sort_values(by="Inventory Value", ascending=True).tail(8)
        fig4 = px.bar(
            top_val_df,
            x="Inventory Value",
            y="Product Name",
            orientation="h",
            title="<b>Top 8 Highest Valuation Products (₹)</b>",
            color="Inventory Value",
            color_continuous_scale=["#E0F7FA", "#00B4DB", "#0083B0"],
            template=chart_theme
        )
        fig4.update_layout(
            autosize=True,
            paper_bgcolor='rgba(255,255,255,0.7)',
            plot_bgcolor='rgba(255,255,255,0.7)',
            height=320,
            margin=dict(l=10, r=10, t=40, b=40),
            coloraxis_showscale=False,
            font=dict(color="#004D40")
        )
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    # LOW STOCK REPORT SECTION
    st.markdown('<div class="alert-title">⚠️ Low Stock Alert & Reorder Report</div>', unsafe_allow_html=True)

    if not low_stock_df.empty:
        st.warning(f"Attention: **{len(low_stock_df)} products** are currently at or below their reorder threshold.")
        
        low_stock_display = low_stock_df.copy()
        low_stock_display.index = range(1, len(low_stock_display) + 1)
        
        st.dataframe(
            low_stock_display.style.format({
                "Price": "₹{:,.2f}",
                "Inventory Value": "₹{:,.2f}",
                "Stock Received": "{:,}",
                "Stock Sold": "{:,}",
                "Current Stock": "{:,}",
                "Reorder Level": "{:,}"
            }),
            use_container_width=True,
            height=220
        )
    else:
        st.success("All products have healthy inventory levels.")

    st.markdown("---")

    # MASTER DATA RECORDS TABLE
    st.markdown('<div class="section-title">📋 Complete Inventory Master Records</div>', unsafe_allow_html=True)

    st.dataframe(
        df.style.format({
            "Price": "₹{:,.2f}",
            "Inventory Value": "₹{:,.2f}",
            "Stock Received": "{:,}",
            "Stock Sold": "{:,}",
            "Current Stock": "{:,}"
        }),
        use_container_width=True,
        height=350
    )

    # DEVELOPER DETAILS FOOTER
    st.markdown("""
    <div class="footer-container">
        <h3>👨‍💻 System Designed & Developed By</h3>
        <p><b>Harinath Poddar</b> | 📧 Email: <a href="mailto:harinathpoddar154@gmail.com" style="color: #FFD700; text-decoration: underline;">harinathpoddar154@gmail.com</a></p>
    </div>
    """, unsafe_allow_html=True)

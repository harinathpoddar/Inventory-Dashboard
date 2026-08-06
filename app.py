import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

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
# CUSTOM STYLING
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Main Background Light Gradient */
    .stApp {
        background: linear-gradient(135deg, #E0F7FA 0%, #FFFDE7 50%, #FFFFFF 100%);
        color: #1A252C;
    }

    /* Sidebar Gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #00B4DB 0%, #0083B0 35%, #F4C430 100%) !important;
        border-right: None;
    }
    
    /* Sidebar Header / Title Style */
    [data-testid="stSidebar"] h1 {
        font-family: 'Arial', sans-serif !important;
        font-size: 22px !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
    }

    /* Sidebar Text & Label Visibility */
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

    /* Form Inputs styling */
    .stTextInput input, .stNumberInput input, .stSelectbox > div {
        background-color: #FFFFFF !important;
        color: #004D40 !important;
        border: 2px solid #00B4DB !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    /* Main Header Banner */
    .main-header {
        background: linear-gradient(135deg, #0083B0 0%, #00B4DB 35%, #FFD700 100%);
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0 8px 25px rgba(0, 180, 219, 0.3);
        margin-bottom: 30px;
        text-align: center;
    }
    .main-header h1 {
        color: #FFFFFF !important;
        font-weight: 900;
        font-size: 2.5rem;
        margin: 0;
        letter-spacing: 0.5px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .main-header p {
        color: #FFFDE7 !important;
        font-size: 1.15rem;
        margin-top: 8px;
        margin-bottom: 0;
        font-weight: 600;
    }

    /* Metric Cards Styling */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #FFFFFF 0%, #E0F7FA 100%) !important;
        border: 2px solid #FFD700 !important;
        padding: 20px !important;
        border-radius: 14px !important;
        box-shadow: 0 6px 18px rgba(0, 180, 219, 0.15) !important;
    }
    div[data-testid="metric-container"] label {
        color: #006064 !important;
        font-size: 0.95rem !important;
        font-weight: 800 !important;
    }
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #0083B0 !important;
        font-size: 2.1rem !important;
        font-weight: 900 !important;
    }

    /* Section Titles */
    .section-title {
        color: #006064;
        font-size: 1.45rem;
        font-weight: 800;
        margin-top: 30px;
        margin-bottom: 20px;
        border-left: 6px solid #FFD700;
        padding-left: 14px;
        background: linear-gradient(90deg, rgba(255, 215, 0, 0.15) 0%, rgba(255,255,255,0) 100%);
        border-radius: 4px;
    }

    /* Alert Title for Low Stock Section */
    .alert-title {
        color: #D32F2F;
        font-size: 1.45rem;
        font-weight: 800;
        margin-top: 30px;
        margin-bottom: 20px;
        border-left: 6px solid #D32F2F;
        padding-left: 14px;
        background: linear-gradient(90deg, rgba(211, 47, 47, 0.1) 0%, rgba(255,255,255,0) 100%);
        border-radius: 4px;
    }

    /* Save Button Gradient */
    .stButton > button {
        background: linear-gradient(90deg, #FFD700 0%, #FFA000 100%) !important;
        color: #004D40 !important;
        border: None !important;
        border-radius: 8px;
        font-weight: 800;
        padding: 10px 20px;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #FFC107 0%, #FF8F00 100%) !important;
        transform: translateY(-2px);
    }

    /* Developer Footer Details Banner */
    .footer-container {
        background: linear-gradient(135deg, #0083B0 0%, #00B4DB 50%, #FFD700 100%);
        padding: 22px;
        border-radius: 12px;
        text-align: center;
        color: #FFFFFF;
        margin-top: 40px;
        box-shadow: 0 6px 20px rgba(0, 131, 176, 0.25);
    }
    .footer-container h3 {
        margin: 0;
        font-size: 1.3rem;
        font-weight: 800;
        color: #FFFFFF !important;
    }
    .footer-container p {
        margin: 6px 0 0 0;
        font-size: 1.05rem;
        font-weight: 600;
        color: #FFFDE7 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# AUTHENTICATION & USER SYSTEM INITIALIZATION
# ---------------------------------------------------------
if 'users' not in st.session_state:
    st.session_state.users = {"admin": "admin123"}  # Default admin user

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# ---------------------------------------------------------
# SAMPLE DATA INITIALIZATION
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
        price = float(np.random.choice([499, 899, 1299, 1799, 2499, 4499, 8999]))
        reorder = np.random.randint(10, 40)
        data.append({
            "Product Code": f"PRD-{i}",
            "Product Name": p,
            "Category": np.random.choice(["Peripherals", "Accessories", "Storage", "Audio", "Monitors"]),
            "Stock Received": int(rec),
            "Stock Sold": int(sold),
            "Current Stock": int(curr),
            "Price": price,
            "Inventory Value": float(curr * price),
            "Reorder Level": int(reorder)
        })
    
    df_init = pd.DataFrame(data)
    df_init.index = range(1, len(df_init) + 1)
    return df_init

if 'inventory_df' not in st.session_state:
    st.session_state.inventory_df = load_initial_data()

# ---------------------------------------------------------
# LOGIN & REGISTER VIEW (If user is not logged in)
# ---------------------------------------------------------
if not st.session_state.logged_in:
    st.markdown("""
    <div class="main-header">
        <h1>🔐 Stock Management Portal</h1>
        <p>Please Login or Register to Access the Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab_login, tab_reg = st.tabs(["🔑 Login", "📝 Register"])
        
        with tab_login:
            st.subheader("Login to your Account")
            login_user = st.text_input("Username", key="l_user")
            login_pass = st.text_input("Password", type="password", key="l_pass")
            if st.button("Login"):
                if login_user in st.session_state.users and st.session_state.users[login_user] == login_pass:
                    st.session_state.logged_in = True
                    st.session_state.user_name = login_user
                    st.success("Login Successful!")
                    st.rerun()
                else:
                    st.error("Invalid Username or Password.")
                    
        with tab_reg:
            st.subheader("Create a New Account")
            reg_user = st.text_input("Choose Username", key="r_user")
            reg_pass = st.text_input("Choose Password", type="password", key="r_pass")
            reg_confirm = st.text_input("Confirm Password", type="password", key="r_conf")
            if st.button("Register"):
                if reg_user in st.session_state.users:
                    st.warning("Username already exists!")
                elif reg_pass != reg_confirm:
                    st.error("Passwords do not match.")
                elif reg_user == "" or reg_pass == "":
                    st.error("Please fill all fields.")
                else:
                    st.session_state.users[reg_user] = reg_pass
                    st.success("Registration Successful! Please switch to Login tab.")

# ---------------------------------------------------------
# MAIN APPLICATION VIEW (If user is logged in)
# ---------------------------------------------------------
else:
    df = st.session_state.inventory_df

    # ---------------------------------------------------------
    # SIDEBAR CONTROL
    # ---------------------------------------------------------
    with st.sidebar:
        st.title("📥 Stock Management")
        st.write(f"Logged in as: **{st.session_state.user_name}**")
        
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user_name = ""
            st.rerun()

        st.markdown("---")
        
        tab_add, tab_manage = st.tabs(["➕ Add New", "⚙️ Update / Delete"])

        # TAB 1: ADD NEW RECORD
        with tab_add:
            st.subheader("Add Record")
            with st.form("add_stock_form", clear_on_submit=True):
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
                            "Stock Received": int(stock_rec),
                            "Stock Sold": int(stock_sold),
                            "Current Stock": int(curr_stk),
                            "Price": float(price_unit),
                            "Inventory Value": float(curr_stk * price_unit),
                            "Reorder Level": int(reorder_lvl)
                        }
                        st.session_state.inventory_df = pd.concat([st.session_state.inventory_df, pd.DataFrame([new_data])], ignore_index=True)
                        st.session_state.inventory_df.index = range(1, len(st.session_state.inventory_df) + 1)
                        st.success(f"Added {prod_name} successfully!")
                        st.rerun()
                    else:
                        st.error("Please enter Product Name & Code.")

        # TAB 2: UPDATE OR DELETE
        with tab_manage:
            st.subheader("Manage Existing Record")
            
            if not df.empty:
                selected_code = st.selectbox("Select Product Code", df["Product Code"].unique())
                selected_row = df[df["Product Code"] == selected_code].iloc[0]
                
                categories_list = ["Peripherals", "Accessories", "Storage", "Audio", "Monitors"]
                cat_index = categories_list.index(selected_row["Category"]) if selected_row["Category"] in categories_list else 0

                with st.form("update_delete_form"):
                    u_name = st.text_input("Product Name", value=selected_row["Product Name"])
                    u_category = st.selectbox("Category", categories_list, index=cat_index)
                    u_rec = st.number_input("Stock Received", min_value=0, step=1, value=int(selected_row["Stock Received"]))
                    u_sold = st.number_input("Stock Sold", min_value=0, step=1, value=int(selected_row["Stock Sold"]))
                    u_price = st.number_input("Price per Unit (₹)", min_value=0.0, step=10.0, value=float(selected_row["Price"]))
                    u_reorder = st.number_input("Reorder Level", min_value=0, step=1, value=int(selected_row["Reorder Level"]))

                    col_upd, col_del = st.columns(2)
                    update_btn = col_upd.form_submit_button("🔄 Update")
                    delete_btn = col_del.form_submit_button("🗑️ Delete")

                    # UPDATE LOGIC
                    if update_btn:
                        curr_stk = u_rec - u_sold
                        st.session_state.inventory_df.loc[st.session_state.inventory_df["Product Code"] == selected_code, [
                            "Product Name", "Category", "Stock Received", "Stock Sold", "Current Stock", "Price", "Inventory Value", "Reorder Level"
                        ]] = [
                            u_name, u_category, u_rec, u_sold, curr_stk, u_price, curr_stk * u_price, u_reorder
                        ]
                        st.success(f"{selected_code} Updated Successfully!")
                        st.rerun()

                    # DELETE LOGIC
                    if delete_btn:
                        st.session_state.inventory_df = st.session_state.inventory_df[st.session_state.inventory_df["Product Code"] != selected_code].reset_index(drop=True)
                        st.session_state.inventory_df.index = range(1, len(st.session_state.inventory_df) + 1)
                        st.success(f"{selected_code} Deleted Successfully!")
                        st.rerun()
            else:
                st.info("No records available.")

    # Reload df reference
    df = st.session_state.inventory_df

    # ---------------------------------------------------------
    # MAIN DASHBOARD CONTENT
    # ---------------------------------------------------------

    # Header Banner
    st.markdown("""
    <div class="main-header">
        <h1>📦 Product Inventory & Stock Analytics</h1>
        <p>Real-Time Interactive Business Intelligence Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    # Executive Key Metrics
    st.markdown('<div class="section-title">📊 Executive Overview</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    total_products = len(df)
    total_stock = df["Current Stock"].sum() if not df.empty else 0
    total_valuation = df["Inventory Value"].sum() if not df.empty else 0.0
    low_stock_df = df[df["Current Stock"] <= df["Reorder Level"]] if not df.empty else pd.DataFrame()
    low_stock_count = len(low_stock_df)

    col1.metric("Total Unique Items", f"{total_products}")
    col2.metric("Total Units in Stock", f"{total_stock:,} Units")
    col3.metric("Total Inventory Valuation", f"₹{total_valuation:,.2f}")
    col4.metric("Low Stock Alerts", f"{low_stock_count}", delta_color="inverse")

    st.markdown("---")

    # ---------------------------------------------------------
    # VISUAL ANALYTICS DASHBOARD
    # ---------------------------------------------------------
    st.markdown('<div class="section-title">📈 Visual Analytics Dashboard</div>', unsafe_allow_html=True)

    if not df.empty:
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
                paper_bgcolor='rgba(255,255,255,0.7)',
                plot_bgcolor='rgba(255,255,255,0.7)',
                height=380,
                margin=dict(l=20, r=20, t=50, b=50),
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
                paper_bgcolor='rgba(255,255,255,0.7)',
                plot_bgcolor='rgba(255,255,255,0.7)',
                height=380,
                margin=dict(l=20, r=20, t=50, b=50),
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
                paper_bgcolor='rgba(255,255,255,0.7)',
                plot_bgcolor='rgba(255,255,255,0.7)',
                height=380,
                margin=dict(l=20, r=20, t=50, b=50),
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
                paper_bgcolor='rgba(255,255,255,0.7)',
                plot_bgcolor='rgba(255,255,255,0.7)',
                height=380,
                margin=dict(l=20, r=20, t=50, b=50),
                coloraxis_showscale=False,
                font=dict(color="#004D40")
            )
            st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("No data available to display charts.")

    st.markdown("---")

    # ---------------------------------------------------------
    # LOW STOCK REPORT
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # MASTER DATA RECORDS TABLE
    # ---------------------------------------------------------
    st.markdown('<div class="section-title">📋 Complete Inventory Master Records</div>', unsafe_allow_html=True)

    if not df.empty:
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
    else:
        st.warning("No records in inventory.")

    # ---------------------------------------------------------
    # DEVELOPER DETAILS FOOTER
    # ---------------------------------------------------------
    st.markdown("""
    <div class="footer-container">
        <h3>👨‍💻 System Designed & Developed By</h3>
        <p><b>Harinath Poddar</b> | 📧 Email: <a href="mailto:harinathpoddar154@gmail.com" style="color: #FFD700; text-decoration: underline;">harinathpoddar154@gmail.com</a></p>
    </div>
    """, unsafe_allow_html=True)

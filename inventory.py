import streamlit as st
import pandas as pd


st.set_page_config(page_title="Titan Inventory Pro", layout="wide")

if 'inventory' not in st.session_state:
    st.session_state.inventory = []

LOW_STOCK_THRESHOLD = 5

st.title("Inventory Pro")

tab1, tab2 = st.tabs(["➕ Register Stock", "📊 Inventory Hub"])

#  TAB 1: REGISTRATION
with tab1:
    with st.form("reg_form", clear_on_submit=True):
        st.header("New Unit Entry")
        c1, c2 = st.columns(2)
        with c1:
            new_id = st.text_input("Unit ID", placeholder="Unique ID #")
            new_name = st.text_input("Unit Name", placeholder="Item Name")
        with c2:
            new_stock = st.number_input("Starting Quantity", min_value=0)
            new_price = st.number_input("Price ($)", min_value=0.0)

        if st.form_submit_button("Add to System"):
            if new_id and new_name:
                st.session_state.inventory.append({
                    "ID": new_id,
                    "Item": new_name,
                    "Stock": new_stock,
                    "Price": new_price
                })
                st.success(f"System Updated: {new_name} Registered.")
            else:
                st.error("Error: ID and Name are required fields.")

# --- TAB 2: HUB ---
with tab2:
    st.header("Management Console")

    # Calculation Logic
    low_stock_items = [i for i in st.session_state.inventory if i['Stock'] <= LOW_STOCK_THRESHOLD]
    total_val = sum(x['Stock'] * x['Price'] for x in st.session_state.inventory)

    # Top Level Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Items", len(st.session_state.inventory))

    if len(low_stock_items) > 0:
        m2.metric("Low Stock Alerts", len(low_stock_items), delta=f"{len(low_stock_items)} CRITICAL",
                  delta_color="inverse")
    else:
        m2.metric("Low Stock Alerts", 0, delta="All Clear")

    m3.metric("Total System Value", f"${total_val:,.2f}")

    if low_stock_items:
        st.error(
            f"⚠️ ALERT: {len(low_stock_items)} items are below the safety limit of {LOW_STOCK_THRESHOLD} units!")

    st.divider()

    # --- THE MANAGEMENT GRID ---
    st.subheader("🛠️ Live Inventory Management")
    st.info("Adjust stock levels directly. Updates are permanent and instant.")

    # Table Headers
    h1, h2, h3, h4 = st.columns([1, 2, 2, 1])
    h1.write("**Status**")
    h2.write("**Item Details**")
    h3.write("**Quantity Control**")
    h4.write("**Action**")

    # Management Rows
    for idx, item in enumerate(st.session_state.inventory):
        r1, r2, r3, r4 = st.columns([1, 2, 2, 1])

        # Column 1: Status Visual
        status_icon = "🔴" if item['Stock'] <= LOW_STOCK_THRESHOLD else "🟢"
        r1.write(status_icon)

        # Column 2: Name & ID
        r2.write(f"**{item['Item']}**  \n(ID: {item['ID']})")


        new_val = r3.number_input("Update",
                                  value=item['Stock'],
                                  key=f"num_{item['ID']}_{idx}",  # Unique key per item
                                  label_visibility="collapsed")
        item['Stock'] = new_val

        # Column 4: Delete Specific Item
        if r4.button("🗑️", key=f"del_{item['ID']}_{idx}"):
            st.session_state.inventory.pop(idx)
            st.rerun()

    st.divider()

    # --- GLOBAL SYSTEM ACTIONS ---
    st.subheader("⚠️ Danger Zone")
    col_purge, _ = st.columns([1, 3])

    if col_purge.button("CLEAR ALL DATA", type="primary", use_container_width=True):
        st.session_state.inventory = []
        st.rerun()

    with st.expander("View Raw Data Table"):
        if st.session_state.inventory:
            st.table(pd.DataFrame(st.session_state.inventory))
        else:
            st.write("No data available.")
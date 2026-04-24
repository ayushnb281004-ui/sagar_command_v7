# --- RELOAD CONTROLS ---
reload_col1, reload_col2 = st.columns([1, 5])
with reload_col1:
    if st.button("🔄 RELOAD DATA", use_container_width=True):
        st.rerun()

st.divider()
"""
Payment Dialog — Simulated secure checkout for paid events.
"""

import streamlit as st


@st.dialog("🎫 Secure Checkout")
def payment_dialog():
    """Simulated payment dialog for paid events."""
    from utils.i18n import t
    from state_manager import get_state
    import time, re

    ev = st.session_state.get("_payment_event")
    if not ev:
        st.error("No event selected.")
        return

    state = get_state()

    # Header
    st.markdown(f"### {ev['title']}")
    st.markdown(f"**{t('amount')}:** `{int(ev['price'])} TMT`")
    st.divider()

    # Form
    with st.form("payment_form"):
        card_number = st.text_input(t("card_number"), max_chars=16, placeholder="1234567812345678")
        c1, c2 = st.columns(2)
        with c1:
            expiry = st.text_input(t("expiry_date"), max_chars=5, placeholder="MM/YY")
        with c2:
            cvv = st.text_input(t("cvv"), max_chars=3, type="password", placeholder="123")
        cardholder = st.text_input(t("cardholder_name"), placeholder="JOHN DOE")

        st.markdown('<div class="pay-btn">', unsafe_allow_html=True)
        submitted = st.form_submit_button(
            f"💳 {t('pay_now')} — {int(ev['price'])} TMT",
            use_container_width=True,
            type="primary",
        )
        st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        # Validation
        errors = []
        card_clean = re.sub(r"\s", "", card_number)
        if not card_clean.isdigit() or len(card_clean) != 16:
            errors.append(t("invalid_card"))
        if not re.match(r"^(0[1-9]|1[0-2])/\d{2}$", expiry.strip()):
            errors.append(t("invalid_expiry"))
        cvv_clean = cvv.strip()
        if not cvv_clean.isdigit() or len(cvv_clean) != 3:
            errors.append(t("invalid_cvv"))
        if not cardholder.strip():
            errors.append(t("fill_required"))

        if errors:
            for e in errors:
                st.error(e)
            return

        # Processing simulation — fast, smooth steps
        with st.spinner(t("processing_payment")):
            bar = st.progress(0)
            for pct in range(0, 101, 5):
                time.sleep(0.06)
                bar.progress(pct)
            bar.progress(100)

        # Record transaction
        txn_id = state.payments.add_transaction(
            event_id=ev["id"],
            title=ev["title"],
            amount=ev["price"],
            name=cardholder.strip(),
            card_last4=card_clean[-4:],
        )
        state.sync_to_session_state()

        # Success screen
        st.balloons()
        st.success(f"🎉 {t('payment_successful')}")
        st.markdown(f"""
| | |
|---|---|
| **{t('transaction_id')}** | `{txn_id}` |
| **Event** | {ev['title']} |
| **{t('amount')}** | {int(ev['price'])} TMT |
| **Card** | •••• {card_clean[-4:]} |
""")
        if st.button(f"✅ {t('done')}", use_container_width=True, type="primary"):
            st.rerun()

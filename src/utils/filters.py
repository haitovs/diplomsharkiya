from datetime import datetime, timedelta


def filter_by_date(df, preset):
    """Filter DataFrame based on date preset: All, Today, This Week, This Month."""
    if df.empty or preset == "All":
        return df

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    if preset == "Today":
        return df[df["date_start"].dt.date == today.date()]
    elif preset == "This Week":
        return df[(df["date_start"] >= today) & (df["date_start"] < today + timedelta(days=7))]
    elif preset == "This Month":
        next_month = (today.replace(day=28) + timedelta(days=4)).replace(day=1)
        return df[(df["date_start"] >= today) & (df["date_start"] < next_month)]

    return df


def apply_filters(df, filters_state):
    """Apply all filters from state to DataFrame. Operates on views, avoids copies."""
    if df.empty:
        return df

    filtered = df

    # City
    if filters_state.city != "All Cities":
        filtered = filtered[filtered["city"] == filters_state.city]

    # Categories
    if filters_state.categories:
        filtered = filtered[filtered["category"].isin(filters_state.categories)]

    # Date
    filtered = filter_by_date(filtered, filters_state.date_preset)

    # Price
    if "price" in filtered.columns:
        filtered = filtered[filtered["price"] <= filters_state.max_price]

    # Search — combine into single mask operation
    if filters_state.search_query:
        q = filters_state.search_query.lower()
        mask = filtered["title"].str.lower().str.contains(q, na=False)
        if "venue" in filtered.columns:
            mask = mask | filtered["venue"].str.lower().str.contains(q, na=False)
        filtered = filtered[mask]

    return filtered

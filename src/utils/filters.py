import pandas as pd
from datetime import datetime, timedelta

def filter_by_date(df, preset):
    """
    Filter the DataFrame based on a date preset.
    Presets: "All", "Today", "This Week", "This Month"
    """
    if df.empty or preset == "All":
        return df
    
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    if preset == "Today":
        return df[df["date_start"].dt.date == today.date()]
    elif preset == "This Week":
        return df[(df["date_start"] >= today) & (df["date_start"] < today + timedelta(days=7))]
    elif preset == "This Month":
        # logic: start of today until the start of next month
        # simplistic "This Month" meaning next 30 days or actual calendar month? 
        # The original code used: next_month = (today.replace(day=28) + timedelta(days=4)).replace(day=1)
        # Let's keep the original logic for consistency.
        next_month = (today.replace(day=28) + timedelta(days=4)).replace(day=1)
        return df[(df["date_start"] >= today) & (df["date_start"] < next_month)]
        
    return df

def apply_filters(df, filters_state):
    """
    Apply all filters from the state object to the DataFrame.
    Expects filters_state to have: city, categories, date_preset, max_price, search_query
    """
    if df.empty:
        return df
        
    filtered = df.copy()
    
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
        
    # Search
    if filters_state.search_query:
        q = filters_state.search_query.lower()
        mask = pd.Series([False] * len(filtered), index=filtered.index)
        if "title" in filtered.columns:
            mask |= filtered["title"].str.lower().str.contains(q, na=False)
        if "venue" in filtered.columns:
            mask |= filtered["venue"].str.lower().str.contains(q, na=False)
        filtered = filtered[mask]
        
    return filtered

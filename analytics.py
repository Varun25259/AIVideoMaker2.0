def compute_basic_score(views, ctr, avg_view_duration):
    return views * (ctr/100.0) * (avg_view_duration/60.0)

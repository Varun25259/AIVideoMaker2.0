import random
HIGH_CPM_KEYWORDS = [
    'personal finance tips', 'stock market basics', 'how to invest in mutual funds',
    'ai tools for business', 'passive income ideas', 'insurance explained',
    'credit score tips', 'best side hustles 2025', 'small business marketing',
    'real estate investing basics'
]
def get_suggested_topics(n=10):
    random.shuffle(HIGH_CPM_KEYWORDS)
    return HIGH_CPM_KEYWORDS[:n]

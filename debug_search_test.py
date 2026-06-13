import sys
sys.path.insert(0, r'd:\chatbot\AI_Workspace')
from modules.web_search import search_google

print('TEST_CALL_START')
try:
    results = search_google('ipl winner 2026')
    print('RESULTS_LEN', len(results))
    for r in results:
        print(r.get('title'), '-', r.get('link'))
except Exception as e:
    print('ERROR', e)

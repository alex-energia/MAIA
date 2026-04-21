# -*- coding: utf-8 -*-
from duckduckgo_search import DDGS
import datetime

class ScoutCore:
    def execute_global_scout(self):
        results = []
        # Query forzando resultados de actualidad de infraestructura 2026
        query = 'energy infrastructure "under construction" 2026 "capacity MW" CEO'
        try:
            with DDGS() as ddgs:
                data = list(ddgs.text(query, max_results=8))
                for i, hit in enumerate(data):
                    results.append({
                        "id": f"2026-ACTUAL-{i}",
                        "title": hit['title'].upper(),
                        "body": hit['body'],
                        "link": hit['href'],
                        "date": datetime.datetime.now().strftime("%Y-%m-%d")
                    })
        except: pass
        return results

scout_engine = ScoutCore()

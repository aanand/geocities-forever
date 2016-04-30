NUM_URLS := 10

URLS_FILE := urls.txt
SELECTED_URLS_FILE := selected-urls.txt
DOWNLOAD_DIR := www.oocities.org
REWRITTEN_DIR := rewritten
CORPUS_FILE := corpus.html
CORPUS_RAW_FILE := corpus-raw.html

default: corpus

corpus:
	scripts/urls-to-ids < $(CORPUS_RAW_FILE) > $(CORPUS_FILE)

corpus-raw:
	grep -rL 'Index of' $(REWRITTEN_DIR) | xargs cat | scripts/fix-invalid-chars > $(CORPUS_RAW_FILE)

rewrite-embeds:
	scripts/rewrite-embeds $(DOWNLOAD_DIR) $(REWRITTEN_DIR)

scrape:
	while true; do scripts/scrape < $(SELECTED_URLS_FILE) && break; done

select-urls:
	cat $(URLS_FILE) | scripts/shuffle $(NUM_URLS) | sed -e 's/oocities.com/oocities.org/' > $(SELECTED_URLS_FILE)

clean:
	rm -rf $(CORPUS_FILE) $(DOWNLOAD_DIR) $(SELECTED_URLS_FILE)

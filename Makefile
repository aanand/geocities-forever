NUM_URLS := 10

URLS_FILE := urls.txt
SELECTED_URLS_FILE := selected-urls.txt
DOWNLOAD_DIR := www.oocities.org
REWRITTEN_DIR := rewritten
CORPUS_FILE := corpus.html
CORPUS_RAW_FILE := corpus-raw.html
SAMPLE_FILE := sample.html
SAMPLE_RAW_FILE := sample-raw.html

default: corpus

sample:
	python ids_to_urls.py < $(SAMPLE_RAW_FILE) > $(SAMPLE_FILE)

corpus:
	python urls_to_ids.py < $(CORPUS_RAW_FILE) > $(CORPUS_FILE)

corpus-raw:
	grep -rL 'Index of' $(REWRITTEN_DIR) | xargs cat > $(CORPUS_RAW_FILE)

rewrite-embeds:
	python rewrite_embeds.py $(DOWNLOAD_DIR) $(REWRITTEN_DIR)

scrape:
	while true; do python scrape.py < $(SELECTED_URLS_FILE) && break; done

select-urls:
	cat $(URLS_FILE) | python shuffle.py $(NUM_URLS) | sed -e 's/oocities.com/oocities.org/' > $(SELECTED_URLS_FILE)

clean:
	rm -rf $(CORPUS_FILE) $(DOWNLOAD_DIR) $(SELECTED_URLS_FILE)

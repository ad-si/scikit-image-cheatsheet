images/generated/%: generate-images.py _data/categories.yaml | images
	python3 $<

images/generated:
	mkdir -p images/generated

clean:
	rm -rf images/generated

.PHONY: all, clean

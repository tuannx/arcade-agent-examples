PY ?= python3
REPORTS = docs/reports

.PHONY: all synthetic adr011 adr014 sweeps clean

all: synthetic adr011 adr014 sweeps

$(REPORTS):
	mkdir -p $(REPORTS)

synthetic: $(REPORTS)
	$(PY) scenarios/synthetic-smells/run.py --out $(REPORTS)

adr011: $(REPORTS)
	$(PY) scenarios/adr-autopsy-011/run.py --out $(REPORTS)

adr014: $(REPORTS)
	$(PY) scenarios/adr-autopsy-014/run.py --out $(REPORTS)

sweeps: $(REPORTS)
	$(PY) scenarios/smell-sweeps/run.py --out $(REPORTS)

clean:
	rm -rf $(REPORTS)

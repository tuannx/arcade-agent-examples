PY ?= python3
REPORTS = docs/reports
PIN_TOOL = scenarios/analyzer_pin.py

.PHONY: all install check-pin synthetic adr011 adr014 sweeps corpus react33152 clean

all: synthetic adr011 adr014 sweeps corpus

install:
	$(PY) $(PIN_TOOL) install

check-pin:
	$(PY) $(PIN_TOOL) check-docs
	$(PY) $(PIN_TOOL) identity >/dev/null

$(REPORTS):
	mkdir -p $(REPORTS)

synthetic: check-pin $(REPORTS)
	$(PY) scenarios/synthetic-smells/run.py --out $(REPORTS)

adr011: check-pin $(REPORTS)
	$(PY) scenarios/adr-autopsy-011/run.py --out $(REPORTS)

adr014: check-pin $(REPORTS)
	$(PY) scenarios/adr-autopsy-014/run.py --out $(REPORTS)

sweeps: check-pin $(REPORTS)
	$(PY) scenarios/smell-sweeps/run.py --out $(REPORTS)

corpus: check-pin $(REPORTS)
	$(PY) scenarios/fork-corpus/run.py --out $(REPORTS)

react33152: check-pin $(REPORTS)
	$(PY) scenarios/pr-react-33152/run.py --out $(REPORTS)

clean:
	rm -rf $(REPORTS)

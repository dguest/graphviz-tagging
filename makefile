# graphviz generation
DOT_DIR    := dot
FIG_DIR    := figures
STRUCT_DIR := structs
DOT_PATHS  := $(wildcard $(DOT_DIR)/*.dot)

# add generated dot files
STRUCT_FILES := $(wildcard $(STRUCT_DIR)/*.txt)
GEN_FILES  := $(STRUCT_FILES:.txt=_gen.dot)
DOT_PATHS  += $(GEN_FILES)

BASE_FILES := $(notdir $(DOT_PATHS))
PDF_FILES  := $(addprefix $(FIG_DIR)/, $(BASE_FILES:%.dot=%.pdf))
EPS_FILES  := $(addprefix $(FIG_DIR)/, $(BASE_FILES:%.dot=%.eps))
PNG_FILES  := $(addprefix $(FIG_DIR)/, $(BASE_FILES:%.dot=%.png))
OUT_PATHS  := $(PDF_FILES) $(EPS_FILES) $(PNG_FILES)

.PHONEY: pdf png eps all

pdf: $(PDF_FILES)
png: $(PNG_FILES)
eps: $(EPS_FILES)

all: $(OUT_PATHS)

$(DOT_DIR)/%_gen.dot: $(STRUCT_DIR)/%.txt make-nn.py
	@./make-nn.py $(shell cat $<) > $@

$(FIG_DIR)/%.pdf: $(DOT_DIR)/%.dot
	@mkdir -p $(FIG_DIR)
	@echo making $@ from $^
	@dot -Tps2 $^ | ps2pdf - - > $@

$(FIG_DIR)/%.eps: $(DOT_DIR)/%.dot
	@mkdir -p $(FIG_DIR)
	@echo making $@ from $^
	@dot -Tps2 $^ | ps2eps > $@ 2> /dev/null

$(FIG_DIR)/%.png: $(DOT_DIR)/%.dot
	@mkdir -p $(FIG_DIR)
	@echo making $@ from $^
	@dot -Tpng $^ > $@

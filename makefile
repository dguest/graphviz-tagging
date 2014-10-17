# graphviz generation 
DOT_DIR    := dot
FIG_DIR    := figures
DOT_PATHS  := $(wildcard $(DOT_DIR)/*.dot)
BASE_FILES := $(notdir $(DOT_PATHS))
PDF_FILES  := $(BASE_FILES:%.dot=%.pdf)
EPS_FILES  := $(BASE_FILES:%.dot=%.eps)
OUT_PATHS  := $(addprefix $(FIG_DIR)/, $(PDF_FILES) $(EPS_FILES))

all: $(OUT_PATHS)

$(FIG_DIR)/%.pdf: $(DOT_DIR)/%.dot
	@mkdir -p $(FIG_DIR)
	@echo making $@ from $^
	@dot -Tps2 $^ | ps2pdf - - > $@

$(FIG_DIR)/%.eps: $(DOT_DIR)/%.dot
	@mkdir -p $(FIG_DIR)
	@echo making $@ from $^
	@dot -Tps2 $^ | ps2eps > $@ 2> /dev/null

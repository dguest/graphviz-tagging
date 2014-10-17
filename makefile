# graphviz generation 
DOT_DIR   := dot
FIG_DIR   := figures
DOT_FILES := $(wildcard $(DOT_DIR)/*.dot)
DOT_PDF   := $(DOT_FILES:$(DOT_DIR)/$(FIG_DIR)%.dot=%.pdf)

all: $(DOT_PDF)

$(FIG_DIR)/%.pdf: $(DOT_DIR)/%.dot
	@echo making $@ from $^
	@dot -Tps2 $^ | ps2pdf - - > $@

DAY := $(notdir $(shell pwd))

C_FILES := $(shell ls $(DAY).c)
C_EXEC := $(DAY)_c

JAVA_FILES := $(shell ls $(DAY).java)
JAVA_CLASS := $(shell echo $(DAY) | sed -e "s/^d/D/")

GO_FILES := $(shell ls $(DAY).go)
GO_EXEC := $(DAY)_go

RUST_FILES := $(shell ls $(DAY).rs)
RUST_EXEC := $(DAY)_rust

default: java go rust

c: $(C_FILES)
	gcc -o $(C_EXEC) $(C_FILES)
	./$(C_EXEC) > /dev/null
	time ./$(C_EXEC)

java: $(JAVA_FILES)
	javac $(JAVA_FILES)
	java $(JAVA_CLASS) > /dev/null
	time java $(JAVA_CLASS)

go: $(GO_FILES)
	go build -o $(GO_EXEC) $(GO_FILES)
	./$(GO_EXEC) > /dev/null
	time ./$(GO_EXEC)

rust: $(RUST_FILES)
	rustc -o $(RUST_EXEC) $(RUST_FILES)
	./$(RUST_EXEC) > /dev/null
	time ./$(RUST_EXEC)

clean:
	rm -f $(C_EXEC) *.class $(GO_EXEC) $(RUST_EXEC)

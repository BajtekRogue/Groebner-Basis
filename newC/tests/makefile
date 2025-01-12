CXX = g++
CXXFLAGS = -std=c++17 -isystem /usr/include/gtest -pthread -I../ -g
LDFLAGS = -lgtest -lgtest_main -L/usr/lib

# Directories
BUILD_DIR = build
EXEC_DIR = $(BUILD_DIR)/executables

# Source files and their corresponding object and executable files
TEST_SRCS = $(wildcard TEST_*.cpp)
TEST_OBJS = $(TEST_SRCS:%.cpp=$(BUILD_DIR)/%.o)
TEST_EXECS = $(TEST_SRCS:%.cpp=$(EXEC_DIR)/%)

# Default target
.PHONY: all
all: $(TEST_EXECS)

# Create build directories
$(BUILD_DIR) $(EXEC_DIR):
	mkdir -p $@

# Compile source files to object files
$(BUILD_DIR)/%.o: %.cpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Link object files to create executables
$(EXEC_DIR)/%: $(BUILD_DIR)/%.o | $(EXEC_DIR)
	$(CXX) $< $(LDFLAGS) -o $@

# Run all tests
.PHONY: run
run: $(TEST_EXECS)
	@for exec in $(TEST_EXECS); do \
		echo "\nRunning $$exec:"; \
		./$$exec || exit 1; \
	done

# Clean build artifacts
.PHONY: clean
clean:
	rm -rf $(BUILD_DIR)

# Show debug information
.PHONY: debug
debug:
	@echo "Test sources: $(TEST_SRCS)"
	@echo "Test objects: $(TEST_OBJS)"
	@echo "Test executables: $(TEST_EXECS)"
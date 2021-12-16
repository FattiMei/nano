CC = gcc


SRC_DIR = /home/pi/nano/3w_analysis/c/src
TEST_DIR = /home/pi/nano/3w_analysis/c/test

XYZ_DIR=/home/pi/nano/3w_files
CMP_DIR=/home/pi/nano/3w_analysis/regression_test
TO_GCODE_EXE=/home/pi/nano/3w_analysis/c/build/to_gcode.out

LINK_FLAGS = -lz -lnettle


build: aes.o memory_view.o XYZ3W.o


unittest: aes.o memory_view.o XYZ3W.o unity.o
	$(CC) -o test_memory_view.out $(TEST_DIR)/test_memory_view.c unity.o memory_view.o -I$(SRC_DIR) $(LINK_FLAGS) && ./test_memory_view.out
	$(CC) -o test_XYZ3W.out $(TEST_DIR)/test_XYZ3W.c unity.o aes.o memory_view.o XYZ3W.o -I$(SRC_DIR) $(LINK_FLAGS) && ./test_XYZ3W.out


regression_test: build to_gcode.o
	$(CC) -o to_gcode.out aes.o memory_view.o XYZ3W.o to_gcode.o -I$(SRC_DIR) $(LINK_FLAGS)
	bash convert_to_gcode.sh


aes.o:
	$(CC) -c $(SRC_DIR)/aes.c


memory_view.o:
	$(CC) -c $(SRC_DIR)/memory_view.c


XYZ3W.o:
	$(CC) -c $(SRC_DIR)/XYZ3W.c


to_gcode.o:
	$(CC) -c $(SRC_DIR)/to_gcode.c


unity.o:
	$(CC) -c $(TEST_DIR)/unity.c


.PHONY: clean

clean:
	rm -f *.o

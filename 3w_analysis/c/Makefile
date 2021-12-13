UNITY_DIR=./Unity/src/
CC=gcc
OFLAG=


unit_test:
	gcc -o test_memory_view.out $(UNITY_DIR)unity.c test_memory_view.c memory_view.c
	./test_memory_view.out
	gcc -o test_XYZ3W.out $(UNITY_DIR)unity.c test_XYZ3W.c XYZ3W.c memory_view.c aes.c -lz -lnettle
	./test_XYZ3W.out


regression_test:
	gcc -o to_gcode.out to_gcode.c XYZ3W.c memory_view.c aes.c -lz -lnettle

.PHONY: clean


clean:
	rm -f *.o

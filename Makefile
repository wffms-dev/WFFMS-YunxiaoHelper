.PHONY:clean

# TODO: 添加对Windows的支持

PYINSTALLER = pyinstaller
RM = rm
CP = cp

FLAGS = --onefile

TARGET_CLI = yunxiao
SOURCE_CLI = yunxiao.py

TARGET_GUI = gui_yunxiao
SOURCE_GUI = gui_yunxiao.py

target: $(TARGET_GUI) $(TARGET_CLI)
	echo "...done"
$(TARGET_CLI): ./dist/yunxiao
	$(CP) $^ .
$(TARGET_GUI): ./dist/gui_yunxiao
	$(CP) $^ .

./dist/yunxiao:
	$(PYINSTALLER) $(FLAGS) $(SOURCE_CLI)
./dist/gui_yunxiao:
	$(PYINSTALLER) $(FLAGS) $(SOURCE_GUI)
clean:
	$(RM) -rf build
	$(RM) -rf dist
	$(RM) *.spec
	$(RM) $(TARGET_GUI) $(TARGET_CLI)

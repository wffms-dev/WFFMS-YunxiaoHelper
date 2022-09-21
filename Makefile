.PHONY:clean

# TODO: 添加对Windows的支持

PYINSTALLER = pyinstaller
RM = rm
CP = cp

FLAGS = --onefile
TARGET = gui_yunxiao
SOURCE = gui_yunxiao.py

$(TARGET): ./dist/gui_yunxiao
	$(CP) $^ .
./dist/gui_yunxiao:
	$(PYINSTALLER) $(FLAGS) $(SOURCE)
clean:
	$(RM) -rf build
	$(RM) -rf dist
	$(RM) *.spec
	$(RM) $(TARGET)

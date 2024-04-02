.PHONY: all clean

all: icons.gresource

clean:
	$(RM) *.gresource

%.gresource: %.gresource.xml
	glib-compile-resources $<

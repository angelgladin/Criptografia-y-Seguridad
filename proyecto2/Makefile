.PHONY: all compile clean run

all:
	@echo "make compile"
	@echo "    Compila el proyecto"
	@echo "make clean"
	@echo "    Limpia el proyecto y elimina los archivos generados en el build."
	@echo "make run"
	@echo "    Ejecuta cifrado y descrifrado usando RSA	"


compile:
	@cd src && scalac Demo.scala

clean:
	@rm src/*.class 2> /dev/null || true

run:
	@cd src && scala Demo

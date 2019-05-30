.PHONY: all compile clean run

all:
	@echo "make compile"
	@echo "    Compila el proyecto"
	@echo "make clean"
	@echo "    Limpia el proyecto y elimina los archivos generados en el build."
	@echo "make run"
	@echo "    Ejecuta cifrado y descrifrado usando RSA	"


compile:
	@cd src && kotlinc ECM.kt -include-runtime -d ECM.jar

clean:
	@rm src/ECM.jar 2> /dev/null || true

run:
	@cd src && java -jar ECM.jar $(n) $(limit)

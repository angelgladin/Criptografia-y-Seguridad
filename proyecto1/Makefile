.PHONY: all prepare-env clean run

all:
	@echo "make prepare-env"
	@echo "    Prepara el entorno."
	@echo "    Se necesita ejecutar con sudo para instalar el manejador de paquetes de Python 3."
	@echo "make clean"
	@echo "    Limpia el proyecto y elimina los archivos generados en el build."
	@echo "make run"
	@echo "    Ejecuta el difrado de Hill"

prepare-env:
	@if ! [ -x "$(command -v pip3)" ] 2> /dev/null ; then \
		apt update; \
		apt install python3-pip -y ; \
	fi
	@pip3 install -r requirements.txt

clean:
	@rm -rf src/__pycache__ 2> /dev/null || true

run:
	@cd src && python3 hill.py3

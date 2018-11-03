output:
	python -m py_compile src/main.py src/editorSettings.py 
	mv src/__pycache__/main.cpython-36.pyc src/__pycache__/main.pyc && mv src/__pycache__/editorSettings.cpython-36.pyc src/__pycache__/editorSettings.pyc
	python src/__pycache__/main.pyc
	clear
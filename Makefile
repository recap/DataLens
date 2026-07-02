.PHONY: clean

clean-py:
	@find . \
		-not -path '*/[@.]*' -type f \
		\( \
			-name "__pycache__" -o \
			-name "*.pyc" -o \
			-name "*.pyo" -o \
			-name "*.pyd" -o \
			-name ".pytest_cache" -o \
			-name ".mypy_cache" -o \
			-name ".ruff_cache" -o \
			-name ".coverage" -o \
			-name "htmlcov" -o \
			-name ".tox" -o \
			-name ".nox" -o \
			-name "build" -o \
			-name "dist" -o \
			-name "*.egg-info" -o \
			-name ".ipynb_checkpoints" \
		\) \
	-exec rm -rf {} +

clean-notebook:
	@find . \
		-not -path '*/[@.]*' -type f \
		-name "*.ipynb" \
		-exec jupyter nbconvert \
        --ClearOutputPreprocessor.enabled=True \
        --inplace \
        {} \;

clean-checkpoints:
	@find . \
		-name ".ipynb_checkpoints" \
		-exec rm -rf {} +

clean: clean-py clean-notebook clean-checkpoints

.PHONY: help install dev test test-slow lint format figuras sobol-quick sobol-full clean caderno tudo

help:
	@echo "Comandos disponíveis:"
	@echo "  make install     · instala em modo desenvolvimento"
	@echo "  make dev         · instala + pre-commit hooks"
	@echo "  make test        · pytest rápido (sem 'slow')"
	@echo "  make test-slow   · pytest completo (inclui Sobol)"
	@echo "  make lint        · ruff check"
	@echo "  make format      · black + ruff format"
	@echo "  make figuras     · gera figuras do artigo"
	@echo "  make sobol-quick · varredura Sobol curta (validação)"
	@echo "  make sobol-full  · varredura Sobol completa (paper-grade)"
	@echo "  make caderno     · executa caderno via nbval"
	@echo "  make clean       · limpa caches e artefatos"

install:
	pip install -e .

dev:
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest -x -q -m "not slow" tests/

test-slow:
	pytest -v tests/

lint:
	ruff check src/ tests/ scripts/

format:
	black src/ tests/ scripts/
	ruff check --fix src/ tests/ scripts/

figuras:
	python scripts/gerar_figuras.py --out figuras/ --formato ambos

sobol-quick:
	python scripts/run_sobol_full.py --n-base 64 --jobs -1 --out results/sobol_quick.parquet

sobol-full:
	python scripts/run_sobol_full.py --n-base 1024 --jobs -1 --out results/sobol_full.parquet

caderno:
	pytest --nbval-lax notebooks/WaaS_caderno_v2.ipynb

clean:
	rm -rf build/ dist/ *.egg-info/
	rm -rf .pytest_cache/ .ruff_cache/ .coverage htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete

tudo: format lint test

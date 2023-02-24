include .env

export PYTHONPATH=$(CURDIR)

alembic_upgrade:
	alembic upgrade head
initial_data:
	cd fast_app && python initial_data.py
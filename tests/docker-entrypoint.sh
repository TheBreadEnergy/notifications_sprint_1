export PYTHONPATH=.
python3 functional/utils/wait_for_es.py \
&& python3 functional/utils/wait_for_redis.py \
&& pytest
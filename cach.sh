#!/bin/bash

user=$(whoami)
export HF_HOME="/goinfre/$user/huggingface_cache"
export TRANSFORMERS_CACHE="/goinfre/$user/huggingface_cache"
export UV_CACHE_DIR="/goinfre/$user/.uv-cache"

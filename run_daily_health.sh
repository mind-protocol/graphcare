#!/bin/bash
cd /home/mind-protocol/graphcare
python3 -m services.health_assessment.daily_check_runner 2>&1 | tee -a data/health_check.log

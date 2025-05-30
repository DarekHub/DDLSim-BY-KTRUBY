#!/bin/bash

cd ~/DDLSim-BY-KTRUBY
source venv/bin/activate

NOW=$(date +"%Y-%m-%d")
LOG_DIR="logs"
LOG_FILE="$LOG_DIR/ddlsim_${NOW}.log"
REPORT_FILE="$LOG_DIR/report_${NOW}.md"

mkdir -p $LOG_DIR

python auto_run_ddlsim.py > "$LOG_FILE"

echo "# DDLSim Daily Report - $NOW" > $REPORT_FILE
echo "" >> $REPORT_FILE
echo "## Training Log Summary" >> $REPORT_FILE
echo '```' >> $REPORT_FILE
tail -n 10 "$LOG_FILE" >> $REPORT_FILE
echo '```' >> $REPORT_FILE
echo "" >> $REPORT_FILE
echo "_Auto-generated on $(date) by $(hostname)_" >> $REPORT_FILE

git add logs/*.log
git add logs/*.md
git commit -m "Auto-update: daily logs and report - $NOW"
git push origin main

#! /bin/bash

xdg-open ./logo/Croaqcomt1.png
sleep 5
pkill eog

DATA_DIR=$1
PEAK=$2

rm -r ./data/$DATA_DIR; mkdir ./data/$DATA_DIR
cp -f ./template/dtmp.csv ./data/$DATA_DIR/trial1.csv

echo "Sample Measurement in Progress..."
CURRENT_POS=0 ## Initialize actuator position to 0
NSTEPS=50 ## Number of times the actuator will move sample
STEP_SIZE=250 ## The step size for the actuator to make
               ## The development was done with Actuonix P8-75-165-3-ST (Each 1 step is ~0.0018mm)
python CROAQ.py $CURRENT_POS $DATA_DIR $PEAK ## Take sample measurement. This is the empty cavity measurement
python updatePlot.py ./data/$DATA_DIR/trial1.csv &


while [ $CURRENT_POS -lt $NSTEPS ]
do
    echo "At position $CURRENT_POS"
    ticcmd --exit-safe-start --position-relative $STEP_SIZE ## Move the actuator by the STEP_SIZE
    CURRENT_POS=$((CURRENT_POS+1))
    sleep 5 ## Wait before executing next command to be sure the actuator has stopped moving
    python CROAQ.py $CURRENT_POS $DATA_DIR $PEAK
    ##CURRENT_POS=$((CURRENT_POS+1))
done

echo "Retracting $((CURRENT_POS*STEP_SIZE)) steps..."
ticcmd --exit-safe-start --position-relative -$((CURRENT_POS*STEP_SIZE))

echo "Sample Measurement Complete"

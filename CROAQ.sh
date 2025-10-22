#! /bin/bash

xdg-open ./logo/Croaqcomt1.png
sleep 5
pkill eog

DATA_DIR=$1
PEAK1=$2
PEAK2=$3
PEAK3=$4
PEAK4=$5
PEAK5=$6
PEAK6=$7
PEAK7=$8
PEAK8=$9

for PEAK in $PEAK1 $PEAK2 $PEAK3 $PEAK4 $PEAK5 $PEAK6 $PEAK7 $PEAK8
do
rm -r ./data/$DATA_DIR$PEAK; mkdir ./data/$DATA_DIR$PEAK
cp -f ./template/dtmp.csv ./data/$DATA_DIR$PEAK/trial1.csv

echo "Sample Measurement in Progress..."
CURRENT_POS=0 ## Initialize actuator position to 0
NSTEPS=74 ## Number of times the actuator will move sample
STEP_SIZE=150 ## The step size for the actuator to make
               ## The development was done with Actuonix P8-75-165-3-ST (Each 1 step is ~0.0018mm)
python CROAQ.py $CURRENT_POS $DATA_DIR$PEAK $PEAK ## Take sample measurement. This is the empty cavity measurement
sleep 10
python updatePlot.py ./data/$DATA_DIR$PEAK/trial1.csv &


while [ $CURRENT_POS -lt $NSTEPS ]
do
    echo "At position $CURRENT_POS"
    ticcmd --exit-safe-start --position-relative $STEP_SIZE ## Move the actuator by the STEP_SIZE
    CURRENT_POS=$((CURRENT_POS+1))
    sleep 8 ## Wait before executing next command to be sure the actuator has stopped moving
    python CROAQ.py $CURRENT_POS $DATA_DIR$PEAK $PEAK
    ##CURRENT_POS=$((CURRENT_POS+1))
done

echo "Retracting $((CURRENT_POS*STEP_SIZE)) steps..."
ticcmd --exit-safe-start --position-relative -$((CURRENT_POS*STEP_SIZE))

echo "Sample Measurement Complete"
sleep 900 ## Wait 5min for the actuator to fully retract

done

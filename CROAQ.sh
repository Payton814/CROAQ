#! /bin/bash


echo "Sample Measurement in Progress..."
CURRENT_POS=0 ## Initialize actuator position to 0
NSTEPS=3 ## Number of times the actuator will move sample
STEP_SIZE=500 ## The step size for the actuator to make
               ## The development was done with Actuonix P8-75-165-3-ST (Each 1 step is ~0.0018mm)
python CROAQ.py $CURRENT_POS ## Take sample measurement. This is the empty cavity measurement

while [ $CURRENT_POS -lt $NSTEPS ]
do
    ticcmd --exit-safe-start --position-relative $STEP_SIZE ## Move the actuator by the STEP_SIZE
    python CROAQ.py $CURRENT_POS
    CURRENT_POS=$((CURRENT_POS+1))
done

ticcmd --exit-safe-start --position-relative -$((CURRENT_POS*500))

echo "Sample Measurement Complete"

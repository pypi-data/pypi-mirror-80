#!/bin/sh

cat Test.xml | yasmine-cli --field=code --value=MIKE --level_station=*.ANMO \
  --schema_version 1.1 -o 1.xml

yasmine-cli --infiles=1.xml --field=latitude --value=33.77 --level_station=*.CCM \
  --schema_version 1.0 -o 2.xml

yasmine-cli --infiles=2.xml --field=operators --value=yml:yml/operators.yml --level_station=*.MIKE -o 3.xml
yasmine-cli --infiles=3.xml --field=operators[1] --value=yml:yml/operator.yml --level_station=*.MIKE -o 4.xml

exit 1

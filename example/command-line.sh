#!/bin/bash
python3 ../scripts_gen.py --template template.txt \
                          --save-to scripts \
                          --param "{'data':'datasets.txt', \
                                    'lambda':[`echo 0.{0..9}|sed -E 's/\s+/,/g'`], \
                                    'seed':[233,874]}" \
                          --format "{data}_lambda={lambda}_seed={seed}.sh" \
                          --delete

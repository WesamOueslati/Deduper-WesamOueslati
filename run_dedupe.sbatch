#!/bin/bash


#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --job-name=deduper
#SBATCH --output=slurm/out/dedupe_%j.out
#SBATCH --error=slurm/err/dedupe_%j.err

/usr/bin/time -v ./oueslati_deduper.py -u $1 -f $2 -o $3
# Deduper tests

## Case 1: No overlap (diff chr)
<p> 
The reads are on completely different chromosomes
</p>

### Example:
``` 
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	2	76814284	36	71M	*	0	0
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	11	76814284	36	71M	*	0	0
```

### Result
<p> 
Both reads are included in the output files because reads on different chromosomes cannot be PCR duplicates
</p>

``` 
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	2	76814284	36	71M	*	0	0
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	11	76814284	36	71M	*	0	0
```

## Case 2: No overlap (same chr)
<p> 
The reads are on the same chromosome but none of the bases overlap
</p>

### Example:
``` 
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	3	2000	36	71M	*	0	0
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	3	5000	36	71M	*	0	0
```

### Result
<p> 
Both reads are included in the output files because reads that map to completely different regions of a chromosome cannot be PCR duplicates
</p>

``` 
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	3	2000	36	71M	*	0	0
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	3	5000	36	71M	*	0	0
```


## Case 3: Different UMIs
<p> 
The unique molecular identifier is different between the two reads
</p>

### Example:
``` 
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	4	76814284	36	71M	*	0	0
NS500451:154:HWKTMBGXX:1:11101:24260:1121:TTCGCCTA	0	4	76814284	36	71M	*	0	0
```

### Result
<p> 
Both reads are included in the output files because reads that have different UMIs could not have originated from the same molecule and thus cannot be PCR duplicates.
</p>

``` 
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	4	76814284	36	71M	*	0	0
NS500451:154:HWKTMBGXX:1:11101:24260:1121:TTCGCCTA	0	4	76814284	36	71M	*	0	0
```

## Case 4: Different Strands
- The reads are located on different strands

### Example:
``` 
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	5	76814284	36	71M	*	0	0
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	16	5	76814284	36	71M	*	0	0
```

### Result
<p> 
Both reads are included in the output files because reads that map to different strands cannot be PCR duplicates.
</p>

``` 
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	5	76814284	36	71M	*	0	0
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	16	5	76814284	36	71M	*	0	0
```

## Case 5: Same UMI, same POS, only Ms present in CIGAR, Same strand
- The unique molecular identifier is the same for both entries.  
- Both enties have the same starting position, and there are no insertions, deletions or soft clipping present in the CIGAR string.
- Both reads are present on the same strand
- Both reads map to the same strand

### Example:
``` 
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	6	76814284	36	71M	*	0	0
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	6	76814284	36	71M	*	0	0
```

### Result
<p> 
Only one read is included (we choose the longer one since it contains more information) in the output file because these are very likely to be PCR duplicates
</p>

``` 
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	6	76814284	36	71M	*	0	0
```

## Case 6: Same UMI, diff POS/same POS but overlap present, only Ms and Ss present in CIGAR string, same strand
- Both molecules have the same UMI
- There is overlap between the two molecules.
- Both reads map to the same strand
- Soft clipping is present

### Example:
```
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	7	76814284	36	71M	*	0	0
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	7	76814286	36	2S70M	*	0	0
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	7	76814284	36	69M2S	*	0	0
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	7	76814286	36	4S69M	*	0	0
```

### Result
<p> 
Depends on where the soft clipping occurs and the calculated 5' start. Reads that have the same 5' start are considered duplicates.
</p>

``` 
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	7	76814286	36	2S70M	*	0	0
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	7	76814286	36	4S69M	*	0	0
```

## Case 7: Skipped regions/insertions/deletion in same pos/same strand reads (CIGARS align -> duplicates)
- Same UMI, same POS, only Ms, Ns present in CIGAR string, same strand
- Both molecules have the same UMI
- There is overlap between the two molecules.
- The starting position POS is the same
- Both reads map to the same strand
- Skipped regions and/or insertions and/or deletions are present


### Example:
```
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	8	76814284	36	2M2N2M	*	0	0
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	8	76814284	36	2M2N2I2D2M	*	0	0
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	8	76814284	36	2M3N2M	*	0	0
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	8	76814284	36	2M5N2D2M	*	0	0
```

### Result
<p> 
Insertions and deletions should be ignored, gaps should align
</p>

``` 
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	8	76814284	36	2M3N2M	*	0	0
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	8	76814284	36	2M5N2D2M	*	0	0
```

## Case 8: Multiple consecutive overlaps
- This tests whether we are checking all overlaps (potentially multiple duplicates per molecule and not just one)

### Example:
```
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	9	76814284	36	71M	*	0	0
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	9	76814289	36	71M	*	0	0
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	9	76814295	36	71M	*	0	0
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	9	76814305	36	71M	*	0	0
```

### Result
<p> 
These all have some overlap but their 5' positions don't align so they are not PCR duplicates.
</p>

``` 
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	9	76814284	36	71M	*	0	0
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	9	76814289	36	71M	*	0	0
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	9	76814295	36	71M	*	0	0
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	9	76814305	36	71M	*	0	0
```





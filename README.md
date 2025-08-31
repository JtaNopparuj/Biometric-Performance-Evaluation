# <div align="left">Biometric Performance Evaluation</div>

This repository evaluates biometric system performance by computing FAR, FRR, EER, and other metrics, and plots ROC, DET, and CMC curves. 

* The only required input is a folder containing the matching results for each candidate obtained from the matcher.

## <div align="left">**plot_genuine_imposter.py**</div>

Plot a genuine-imposter distribution

Example usage:
* Plot a Distribution
```python
python plot_genuine_imposter.py -m "C:\Users\Administrator\Documents\test\Matching"
```

* Plot a Distribution without normalization (Probability)
```python
python plot_genuine_imposter.py -m "C:\Users\Administrator\Documents\test\Matching" -norm 0
```

## <div align="left">**plot_FAR_FRR.py**</div>

Plot the FAR, FRR curves and EER

Example usage:
* Plot the FAR-FRR curve
```python
python plot_FAR_FRR.py -m "C:\Users\Administrator\Documents\test\Matching"
```

## <div align="left">**plot_DET.py**</div>

Plot the Detection Error Tradeoff (DET) curve

Example usage:
* Plot the DET curve 
```python
python plot_DET.py -m "C:\Users\Administrator\Documents\test\Matching" -log 0
```

* Plot the DET curve on a log scale
```python
python plot_DET.py -m "C:\Users\Administrator\Documents\test\Matching"
```

## <div align="left">**plot_ROC.py**</div>

Plot the Receiver Operating Characteristic (ROC) curve

Example usage:
* Plot the ROC curve 
```python
python plot_ROC.py -m "C:\Users\Administrator\Documents\test\Matching"
```

## <div align="left">**plot_ROC.py**</div>

Plot the Cumulative Match Characteristic (CMC) curve

Example usage:
* Plot the CMC curve with a maximum rank of 50
```python
python plot_CMC.py -m "C:\Users\Administrator\Documents\test\Matching" -maxr 50
```

* Plot the CMC curve and save the <code>rank.csv</code> file
```python
python plot_CMC.py -m "C:\Users\Administrator\Documents\test\Matching" -save 1
```

* Plot the CMC curve and save the <code>rank.csv</code> file to the specified directory
```python
python plot_CMC.py -m "C:\Users\Administrator\Documents\test\Matching" -save 1 -o "../output_file/algorithm1"
```

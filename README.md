# <div align="left">Biometric Performance Evaluation</div>

This repository evaluates biometric system performance by computing FAR, FRR, EER, and other metrics, and plots ROC, DET, and CMC curves. 

* The only required input is a folder containing the matching results for each candidate obtained from the matcher.

## <div align="left">**plot_genuine_imposter.py**</div>

Plot a genuine-imposter distribution

Example usage:
* Plot Distribution
```python
python plot_genuine_imposter.py -m "C:\Users\Administrator\Documents\test\Matching"
```

* Plot Distribution with normalization
```python
python plot_genuine_imposter.py -m "C:\Users\Administrator\Documents\test\Matching" -norm 0
```

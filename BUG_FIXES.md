# Bug Fixes From Walkthrough

This file tracks bugs, typos, and implementation issues found while translating `CollectionStrategy_Walkthrough.ipynb` into pure Python code.

## 1. Fixed `TiemCorrelations` Typo

### Original Issue

The walkthrough checked for:

```python
"TiemCorrelations"
```

instead of:

```python
"TimeCorrelations"
```

### What The Bug Did

The typo prevented the intended `TimeCorrelations` environment type from being handled correctly in `get_sample()`. If the environment used `TimeCorrelations`, the function could skip the intended stochastic sampling branch.

### Fix

Use the correct environment type name:

```python
"TimeCorrelations"
```

## 2. Fixed WaitingTime Boolean Logic

### Original Issue

The walkthrough used:

```python
if not (sample == 11) | (sample == 1):
```

### What The Bug Did

This expression depended on operator precedence between `not` and `|`. It could make the `WaitingTime` strategy leave the active state incorrectly when checking whether the latest sample was irrelevant.

### Fix

Add another pair of parentheses so the `not` applies to the entire relevancy check:

```python
if not ((sample == 11) | (sample == 1)):
```

## 3. Fixed Reversed Cost Assignment

### Original Issue

The walkthrough comments define:

```text
costs[0] = low-quality sample cost
costs[1] = high-quality sample cost
```

but the update logic assigned:

```python
strat.currentcost = strat.costs[0]  # active
strat.currentcost = strat.costs[1]  # passive
```

### What The Bug Did

The simulation recorded low cost during active/high-quality sampling and high cost during passive/low-quality sampling. This reversed the intended resource-cost behavior.

### Fix

Use the high-quality cost while active and the low-quality cost while passive:

```python
strat.currentcost = strat.costs[1]  # active
strat.currentcost = strat.costs[0]  # passive
```

## 4. Fixed `GenerateDataFromTime` Row Iteration

### Original Issue

The original helper iterated over the number of columns:

```python
for ii in np.arange(cols):
```

but each active time window is stored as a row:

```text
[start, end]
```

### What The Bug Did

The function could generate incomplete or incorrect preset data because it looped over the number of columns instead of the number of active windows.

### Fix

Iterate over rows:

```python
for ii in np.arange(rows):
```

## 5. Fixed `GenerateDataFromTime` Syntax Error

### Original Issue

The original notebook had a broken `if` statement:

```python
if data.size < Tmax
:    data = np.append(data, np.zeros(Tmax-data.size))
```

### What The Bug Did

This caused a syntax error, which meant the `GenerateDataFromTime` helper cell could not run.

### Fix

Put the colon at the end of the `if` statement:

```python
if data.size < Tmax:
    data = np.append(data, np.zeros(Tmax-data.size))
```

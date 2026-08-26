# 02_dataset_dictionary.md

## Target

* `diabetes` → diabetes indicator (0 = no diabetes, 1 = diabetes)

---

## Patient Profile

* `gender` → Male / Female
* `age` → age of the patient (years)
* `hypertension` → 0 = no hypertension, 1 = has hypertension
* `heart_disease` → 0 = no heart disease, 1 = has heart disease
* `smoking_history` → categorical (never, former, current, ever, not current, No Info)

---

## Clinical Measurements

* `bmi` → Body Mass Index (kg/m²)
* `HbA1c_level` → Hemoglobin A1c level (%)
* `blood_glucose_level` → Blood glucose level (mg/dL)

---

## Data Considerations

When working with this dataset, always check:

* Class imbalance in `diabetes` (diabetic patients are typically a minority)
* Missing or inconsistent values in `smoking_history` (e.g., "No Info")
* Outliers or extreme values in `bmi`, `HbA1c_level`, and `blood_glucose_level`
* Age distribution and potential age-related biases
* Feature scaling requirements for certain models

---

## Feature Types Summary

| Feature | Type | Notes |
|---|---|---|
| gender | Nominal categorical | Encode with N-1 dummies |
| age | Continuous numerical | May need binning for analysis |
| hypertension | Binary | Already numeric (0/1) |
| heart_disease | Binary | Already numeric (0/1) |
| smoking_history | Ordinal categorical | Has hierarchy: never < former < current |
| bmi | Continuous numerical | Check for outliers |
| HbA1c_level | Continuous numerical | Strong diabetes indicator |
| blood_glucose_level | Continuous numerical | Strong diabetes indicator |
| diabetes | Binary target | 0/1 |

---

## Modeling Notes

* `HbA1c_level` and `blood_glucose_level` are clinical measurements directly related to diabetes diagnosis — these will likely be strong predictors
* `bmi`, `age`, `hypertension`, and `heart_disease` are known risk factors
* `smoking_history` may have limited predictive power but should be explored
* Be careful with interpretation (correlation ≠ causation)
* Consider class imbalance when selecting metrics and thresholds

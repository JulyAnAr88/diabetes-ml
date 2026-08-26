# 07_task_bi.md

## Goal

Prepare outputs for business reporting.

---

## Deliverables

* Notebook: `notebooks/03_bi_reporting.ipynb`
* BI-ready tables in `reports/tables/`
* BI-ready figures in `reports/figures/`
* Executive summary in `reports/executive_summary.md`

---

## Required Outputs

* Diabetes prevalence summary
* Segment-level diabetes analysis
* High-risk patient list
* Model performance summary

At minimum, produce:

* one overall diabetes prevalence KPI table
* at least two segment-level diabetes tables
* at least two business-friendly figures
* one high-risk patient export for clinical follow-up
* one executive summary in plain business language

---

## Suggested Output Files

Tables in `reports/tables/`:

* `diabetes_prevalence_summary.csv`
* `diabetes_by_segment.csv`
* `model_metrics_summary.csv`
* `high_risk_patients.csv`
* `power_bi_master.csv` — single wide table for Power BI (one row per patient)

Figures in `reports/figures/`:

* `diabetes_overview.png`
* `diabetes_by_segment.png`

Executive summary:

* `reports/executive_summary.md`

---

## Requirements

* Business-friendly language
* Clear KPIs
* Clean, structured tables
* Consistent naming across tables, figures, and narrative
* Clear distinction between observed diabetes patterns and model predictions
* No overclaiming insights

---

## KPI Expectations

Include KPIs such as:

* overall diabetes prevalence rate
* patient counts by segment
* diabetes rate by segment
* model performance metrics used for business reporting
* count of high-risk patients based on model predictions

Use labels that are understandable for non-technical stakeholders.

---

## Segment Analysis

Include segment-level analysis for relevant health dimensions, for example:

* age bands
* BMI categories
* gender
* hypertension and heart disease status
* smoking history
* HbA1c level ranges
* blood glucose level ranges

Explain which segments appear to have higher diabetes prevalence and which findings are descriptive versus model-based.

---

## High-Risk Patient Export

The high-risk patient output should be ready for clinical or operational use.

Include:

* patient index or row identifier
* diabetes probability
* predicted class
* key health indicators useful for follow-up

Document the threshold used to define a patient as high risk.

---

## Executive Summary

The executive summary should be short, clear, and business-oriented.

Suggested sections:

* business objective
* key diabetes insights
* high-risk segments or patients
* model performance summary
* assumptions and limitations
* recommended next actions

---

## Notes

* Generate BI outputs from the BI/reporting notebook
* Separate descriptive vs model-based insights
* Focus on clarity
* Avoid causal claims unless they are explicitly supported
* State important assumptions, filters, and thresholds used in the outputs

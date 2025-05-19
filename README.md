# 🧬 data-harmonisation

This repository provides Python scripts and mapping files for **harmonizing clinical and research datasets** from multiple SPARCO sites to a **standardized data dictionary** defined by the **Sickle Africa Data Coordinating Center (SADaCC)**.

The harmonization process ensures consistent variable naming and structure across diverse site datasets, enabling large-scale analysis and cross-cohort research.

---

## 🌍 Background

The **Sickle in Africa Consortium** brings together multiple research and clinical centers across sub-Saharan Africa. Each center collects data using slightly different formats, variable names, and conventions. This repository provides tools to:

- Align variable names from multiple sites to the **SADaCC standard**.
- Ensure consistent formatting and data interpretation.
- Enable downstream epidemiological and genetic analyses on a harmonized dataset.

---

## 📁 Repository Structure

├── DataMigrationCodeFinal14April.py           
 #### Main script for harmonizing local datasets to SADaCC format


├── DataMigrationScriptFinal.py                
#### Alternate or experimental harmonization script


├── MappingFile1.tsv                            
#### Example mapping of local variable names to SADaCC standard


├── SADaCCVariables.tsv                         
#### Full dictionary of standardized SADaCC variable names


├── Sadacc_sparco_TEMPLATE_mapping_ver7b-....  
#### Template file to help sites build their own mappings





---

## 🛠️ Requirements

- **Python 3.6+**
- No external packages required; uses built-in Python modules such as:
  - `csv`
  - `os`
  - `sys`
  - `argparse` (if added)

Scripts are platform-independent and should run on Windows, macOS, or Linux.

---

## 🚀 Quick Start

### 🧪 Example: Harmonize a site dataset

To harmonize `SCDRegistry_DATA_2018-11-02_1657.csv` using your site’s mapping file:

```bash
python DataMigrationCodeFinal14April.py \
    SCDRegistry_DATA_2018-11-02_1657.csv \
    MappingFile1.tsv \
    SADaCCVariables.tsv


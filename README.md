# MiCM-summer-project

Analysis of 2D and 3D models of neural electrical activity in Parkinson’s disease

## Hierarchical clustering
### Objective:
Generate a hierarchically clustered heatmap showing how midbrain organoids generated from a synuclein triplication mutant line and a healthy control line are clustered based on their electrophysiological activity.

### Installation:
Dependencies:
- python 3.6+
- seaborn 0.11.1

Install seaborn:
`pip install seaborn`
Also included in Anaconda distribution
`conda install seaborn`

### Running the code:
download hierarchical.py
`python hierarchical.py`

### Output:
![Fig_2_Mut_vs_Con](https://user-images.githubusercontent.com/71605598/122827100-f405d780-d2b1-11eb-8510-56a367b2a518.png)


## Relevant readings:
### Electrophysiology
- M. Chiappalone, A. Novellino, I. Vajda, A. Vato, S. Martinoia, J. van Pelt. Burst detection algorithms for the analysis of spatio-temporal patterns in cortical networks of neurons. Neurocomputing. https://doi.org/10.1016/j.neucom.2004.10.094. 

- Cotterill E, Charlesworth P, Thomas CW, Paulsen O, Eglen SJ. A comparison of computational methods for detecting bursts in neuronal spike trains and their application to human stem cell-derived neuronal networks. J Neurophysiol. 2016 Aug 1;116(2):306-21. doi: 10.1152/jn.00093.2016. Epub 2016 Apr 20. PMID: 27098024; PMCID: PMC4969396. 

- Cotterill E, Eglen SJ. Burst Detection Methods. Adv Neurobiol. 2019;22:185-206. doi: 10.1007/978-3-030-11135-9_8. PMID: 31073937. 

- Izsak J, Seth H, Andersson M, Vizlin-Hodzic D, Theiss S, Hanse E, Ågren H, Funa K, Illes S. Robust Generation of Person-Specific, Synchronously Active Neuronal Networks Using Purely Isogenic Human iPSC-3D Neural Aggregate Cultures. Front Neurosci. 2019 Apr 24;13:351. doi: 10.3389/fnins.2019.00351. PMID: 31068774; PMCID: PMC6491690. 

- Pasquale V, Martinoia S, Chiappalone M. A self-adapting approach for the detection of bursts and network bursts in neuronal cultures. J Comput Neurosci. 2010 Aug;29(1-2):213-229. doi: 10.1007/s10827-009-0175-1. Epub 2009 Aug 8. PMID: 19669401. 

### Organoids
- Mohamed NV, Mathur M, da Silva RV et al. Generation of human midbrain organoids from induced pluripotent stem cells [version 1; peer review: 1 approved, 3 approved with reservations]. MNI Open Res 2019, 3:1 (https://doi.org/10.12688/mniopenres.12816.1) 

- NguyenVi Mohamed, Julien Sirois, Janani Ramamurthy, et al. Midbrain organoids with an SNCA gene triplication model key features of synucleinopathy. doi: https://doi.org/10.1101/2021.04.12.439480 

### Parkinson's Disease
- Klein C, Westenberger A. Genetics of Parkinson's disease. Cold Spring Harb Perspect Med. 2012 Jan;2(1):a008888. doi: 10.1101/cshperspect.a008888. PMID: 22315721; PMCID: PMC3253033. 

- Nimmrich V, Draguhn A, Axmacher N. Neuronal Network Oscillations in Neurodegenerative Diseases. Neuromolecular Med. 2015 Sep;17(3):270-84. doi: 10.1007/s12017-015-8355-9. Epub 2015 Apr 29. PMID: 25920466. 

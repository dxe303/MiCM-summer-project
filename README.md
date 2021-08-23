# MiCM-summer-project

Data visualization tools for MEA data of 2D and 3D cell cultures

## Installation:
Dependencies:
- python 3.6+
- seaborn 0.11.1

To install seaborn:
```
$ pip install seaborn
```

Seaborn is also included in the Anaconda distribution:
```
$ conda install seaborn
```
Clone the repository:
```
$ git clone https://github.com/dxe303/MiCM-summer-project.git
```
## Data sorting
To preprocess the spike train data of all organoids on a plate given by the spike_list.csv file generated by Axion software and generate separate spikes.csv files for every organoid on the plate, 

1. From the Spike_analysis folder of the cloned directory, run the spike_sort.py bash script with the input folder containing all spike_list.csv files as the first command line argument. 
```
$ python spike_sort.py inputFolder
```

## Clustering analysis
### Example of hierarchical clustering on provided dataset:
Generate an example of a hierarchically clustered heatmap showing how midbrain organoids generated from a synuclein triplication mutant line and a healthy control line are clustered based on their electrophysiological activity.

1. From the cloned directory, run the hierarchical_exercise.py script with the filepath to Extracted-Parameters.xlsx as an argument
```
$ python hierarchical_exercise.py Extracted-Parameters.xlsx
```
#### Output:
The plot will be saved in the cloned directory under hierarchical.png
![Fig_2_Mut_vs_Con](https://user-images.githubusercontent.com/71605598/122827100-f405d780-d2b1-11eb-8510-56a367b2a518.png)

### Hierarchical clustering
Generate 3 hierarchically clustered heatmaps showing how different cell plates or cell lines are clustered based on their electrophysiological activity. Input file must be an excel sheet with similar format to Extracted-Parameters.xlsx. Data is read by default from sheet_name="Combined by plate" for hierarchical clustering by plate, sheet_name="Combined by line" for hierarchical clustering by cell line, and sheet_name="Synuclein triplication" for hierarchical clustering by plate for syn mutants only. 

The extracted parameters used for hierarchical clustering are: Total spikes, number of bursts, number of network bursts, mean firing rate (MFR), synchrony index

1. From the Clustering_analysis folder inside the cloned directory, run the hierarchical.py script with the filepath to the input file as an argument. For example:
```
$ python hierarchical.py Extracted-Parameters.xlsx
``` 

## Burst analysis + inter event interval histogram plotting
### Burst detection using the ISI threshold method:
Detect electrode burts for a well using the ISI threshold method, with the minimum number of spikes allowed in a burst set to 5 and the maximum inter spike interval allowed in a burst set to 0.1 sec. Also computes the histogram of logISIs for each organoid.

Output: a bursts.csv file and a log_ISI.png file for every spikes.csv input file

1. To run the ISI_threshold_burst_detection.py script on all spikes.csv files inside some $inputFolder: 
```
$ python ISI_threshold_burst_detection.py inputFolder
```
#### Example output:
![W2_D6_log_ISI](https://user-images.githubusercontent.com/71605598/130262587-7541aade-b070-4a53-904b-eca5ff946aff.png)

### Network burst detection using the adaptive threshold method:
Detect network burts for a well using the ISI threshold method, with the minimum percent of spikes allowed in a burst set to 0.1875 out of 16 bursting electrodes. Also computes the histogram of logIBeIs for each organoid. 
N.B.: ISI_threshold_burst_detection.py must be run on data before running this script

Output: a histogram of log inter burst event intervals saved as a log_IBeIH.png file and a networkBursts.csv file for every burst_list.csv input file.

1. To run the Adaptive_threshold_network_burst_detection.py script on all bursts.csv files inside some $inputFolder: 
```
$ python Adaptive_threshold_network_burst_detection.py inputFolder
```
### Example output:
![W2_D6_log_IBeIH](https://user-images.githubusercontent.com/71605598/130262655-2413706a-e827-4cbd-8b0b-4ff580e25d62.png)

## Spike analysis
### Raster plots + histograms of spike count per 1 second bin
Plots a raster plot of spike train data for every organoid, along with a histogram of spike counts per 1 second interval. If available, will also plot the burst and network burst information for every organoid. To get burst and network burst information, run ISI_threshold_burst_detection.py and Adaptive_threshold_network_burst_detection.py on data before running spike_raster.py.

1. To run the spike_raster.py script on all spikes.csv files inside some $inputFolder: 
```
$ python spike_raster.py inputFolder
```
#### Example output:
![W2_D6_spikes_raster](https://user-images.githubusercontent.com/71605598/130263335-1ef5b03f-f9a3-4e70-b507-4eaba7d12d47.png)

### Power spectral density plots
Plots the power spectral density from the spike train data of an organoid. Bin size (1/sampling frequency) is by default 0.0005 sec.

1. To run the power_spectrum.py script on all spikes.csv files inside some $inputFolder: 
```
$ python power_spectrum.py inputFolder
```
#### Example output with bin size=0.05:
![W2_D6_spikes_pow_spec_freq_20](https://user-images.githubusercontent.com/71605598/130263494-40eb40ef-82d6-4efc-b64e-905748a3a32b.png)

### Mean power spectral density plots
Plots the averaged power spectral density for a set of organoids. Bin size (1/sampling frequency) can be provided as the second command line argument, default bin size is 0.0005 sec.

1. From the Spike_analysis folder inside the cloned directory, run the power_spectrum_mean.py script with the filepath to the input folder containting the spikes.csv files to be averaged as the first argument, and the bin size as the second argument. For example:
```
$ python power_spectrum_mean.py Mutant_organoids 0.05
```
#### Example output with bin size=0.05:
![mean_pow_spec_freq_20](https://user-images.githubusercontent.com/71605598/130263689-07bb7ba4-74a5-4153-8907-698efb0e13b2.png)

## Others
`MiCM-summer-project\bash_scripts` contains spikesort.sh, a bash script version of spike_sort.py, and spike_filefinder.sh, for finding spikes.csv files and executing another script on every file found.

`MiCM-summer-project\Burst_analysis\original_scripts` contains the original raster plotting, data organization, burst detection and network burst detection scripts that work with excel files.

`MiCM-summer-project\Clustering_analysis\kmeans` performs k means clustering on an Extracted-Parameters.xlsx file, similar to the hierarchical clustering script.

`MiCM-summer-project\Spike_analysis\drafts` contains spike_histogram.py, which plots a histogram of logISIs for an input spikes.csv file, and power_spectrum_axion.py, which plots a grid of power spectrums for every organoid in the spike_counts.csv outputted by Axion software.

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

- Lancaster, M., Renner, M., Martin, CA. et al. Cerebral organoids model human brain development and microcephaly. Nature 501, 373–379 (2013). https://doi.org/10.1038/nature12517  

- Galet Benjamin, Cheval Hélène, Ravassard Philippe. Patient-Derived Midbrain Organoids to Explore the Molecular Basis of Parkinson's Disease. Frontiers in Neurology. DOI=10.3389/fneur.2020.01005 

- Smits, L.M., Reinhardt, L., Reinhardt, P. et al. Modeling Parkinson’s disease in midbrain-like organoids. npj Parkinsons Dis. 5, 5 (2019). https://doi.org/10.1038/s41531-019-0078-4 

### Parkinson's Disease
- Klein C, Westenberger A. Genetics of Parkinson's disease. Cold Spring Harb Perspect Med. 2012 Jan;2(1):a008888. doi: 10.1101/cshperspect.a008888. PMID: 22315721; PMCID: PMC3253033. 

- McGregor MM, Nelson AB. Circuit Mechanisms of Parkinson's Disease. Neuron. 2019 Mar 20;101(6):1042-1056. doi: 10.1016/j.neuron.2019.03.004. PMID: 30897356. 

- Hammond C, Bergman H, Brown P. Pathological synchronization in Parkinson's disease: networks, models and treatments. Trends Neurosci. 2007 Jul;30(7):357-64. doi: 10.1016/j.tins.2007.05.004. Epub 2007 May 25. PMID: 17532060. 

- Galvan A, Wichmann T. Pathophysiology of parkinsonism. Clin Neurophysiol. 2008 Jul;119(7):1459-74. doi: 10.1016/j.clinph.2008.03.017. Epub 2008 May 7. PMID: 18467168; PMCID: PMC2467461. 

- Nimmrich V, Draguhn A, Axmacher N. Neuronal Network Oscillations in Neurodegenerative Diseases. Neuromolecular Med. 2015 Sep;17(3):270-84. doi: 10.1007/s12017-015-8355-9. Epub 2015 Apr 29. PMID: 25920466. 

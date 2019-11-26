# Iowa_Analyzer
Python based Iowa gambling task result analyzer

@Knowblesse 2019

made for 2019 Autumn Sim yeon presentation

# Important
**DATA_FOLDER** variable in *main.py* must be set manually.

# File Structre
**Main.py** : primary analysis script. score, ratio of the best choice.

**RW_parameter_extractor.py** : generate csv file (RW_result.csv) which contains optimized hyper-parameter value.

**CSV_data_plot.py**
- *imshow_score* : draw heatmap of the hyper-parameter plane
- *parameterGraph* : load RW_result.csv and draw plot of alpha and it. 
# Automated image analysis

This script was used to access healthy plant tissue automatically (see references for scientific paper). Base script follows the image analysis script of Exposito-Alonso et al. (2018) with multiple adaptations (see references for git repository). Adaptations were done in colour filtering, especially when distinguishing between plant material and soil as well as tissue colour change, smoothing and masking of individual pots/plants. 

## Adapatations

We build a “black-box” that fitted quite closely over our trays and had a stable camera holding on top. Inside walls were sprayed matt black to prevent reflection by flash (see folder "example_pictures"). 

Camera was a 12 MP Panasonic DMC-FS10 digital camera with ISO 100 and -2/3 exposure. Every second pot per tray was filled with one individual plant to reduce the possibility of leave overlap during growth. 

Due to the applied stress plants tended to turn red/lilac during the experiment. As plant tissue is still viable, we adapted the existing script to also include these colour range. Therefore, it was necessary to add another filtering as well as a new merging step to obtain the “real” size of the plants. Pictures were separately filtered for all green and red leaf pixels before the obtained images were merged.

Adaptation for the selection of “area of interest” was necessary due to a different tray layout. Individual pots are shifted half a pot from row to row and each row has a different number of pots (4-5). Therefore, a black mask was produced that had the same size as the raw picture and a hole at the position of interest. 

The program computes date of observation, tray ID, pot position (plant ID) and number of counted pixels per individual as .csv file and can save the obtained filtered picture, separately per pot or for the whole tray.

## Workflow

![Workflow](/automated_image_analysis/blob/main/example_pictures/workflow_image_analysis.svg?raw=true "Workflow")

Code can be run via shell script from every OS. We specified the working directory to be the folder in which the analyzed images are stored. Code is commented in detail. Main script is "countgreen_master", which accesses the specific method scripts. Careful, running the shell script overwrites the existing files in the image folders!

Example pictures include day specific images as well as pot positions (slightly changed from day to day). We included fully processed images of each workflow step and pixel count outputs (see folder "201204).

## References

Base script: https://github.com/MoisesExpositoAlonso/hippo

Scientific paper: in preparation


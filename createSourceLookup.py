# Python script to generate a list of tectonic source regions in Canada, for CanSRM1 postprocessing. Written by TEH on 20 Oct 2021, updated 27 Oct 2021.

from xml.dom import minidom
import glob
import pandas as pd

#### Read in model summary files
#filepath = "../CanadaSHM6/source_summary_csv/simplifiedModel/"
#W = pd.read_csv(filepath+"W_CANADA_UPDATED_simplified_collapsedRates.csv"); W['regWt'] = 1; W['regName'] = 'W'
#SE_R2 = pd.read_csv(filepath+"SE_CANADA_R2_simplified_collapsedRates.csv"); SE_R2['regWt'] = 0.2; SE_R2['regName'] = 'SE_R2'
#SE_H2 = pd.read_csv(filepath+"SE_CANADA_H2_simplified_collapsedRates.csv"); SE_H2['regWt'] = 0.4; SE_H2['regName'] ='SE_H2'
#SE_HY = pd.read_csv(filepath+"SE_CANADA_HY_simplified_collapsedRates.csv"); SE_HY['regWt'] = 0.4; SE_HY['regName'] = 'SE_HY'
#EA_R = pd.read_csv(filepath+"EasternArctic_R_simplified_collapsedRates.csv"); EA_R['regWt'] = 0.4; EA_R['regName'] = 'EA_R'
#EA_H = pd.read_csv(filepath+"EasternArctic_H_simplified_collapsedRates.csv"); EA_H['regWt'] = 0.6; EA_H['regName'] = 'EA_H'
#### Merge regional models into national
#df = pd.concat([W, SE_R2, SE_H2, SE_HY, EA_R, EA_H]).reset_index()
#### Find all unique source regions, and their source types
#df2 = df[['srcCode', 'srcName', 'tectReg']].drop_duplicates()
### Above file paths are not updated? Don't contain all sources.

### Initialize a dataframe for results
df2 = pd.DataFrame(columns=['code', 'name', 'tectonicRegion'])

### FOR ALL SOURCE FILES:
filepath = "../CanadaSHM6/OpenQuake_model_files/sources/nationalModel/xml/simplifiedModel/"
all_files = glob.glob(filepath + "WCan_*.xml")

for fname in all_files:
    ### Read in source xml file
    file = minidom.parse(fname)
    ### Extract sources
    source = file.getElementsByTagName('areaSource')
    for el in source:
        code = el.attributes['id'].value
        name = el.attributes['name'].value
        regi = el.attributes['tectonicRegion'].value
        #wrap = pd.DataFrame([[code, name, regi]])
        df2 = df2.append({'code': code, 'name': name, 'tectonicRegion': regi}, ignore_index=True)
    
### Remove duplicates
df2 = df2.drop_duplicates()

### Save it
df2.to_csv('sourceTypes.csv', index=False)
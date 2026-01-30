import pandas as pd
DfChomage2024 = pd.read_csv("DD_EEC_ANNUEL_2024_data.csv", sep=";")
DfChomage2024c= DfChomage2024.dropna(subset=["OBS_VALUE"]).copy()
#Creating a copy of the DataSet

DfChomage2024c.info()
#We have 16 columns and 16 407 values
#I want to illustrate the unenmployement rate considering the level of education and the age




#cleaning EMPSTA
DfChomage2024c["EMPSTA"] = DfChomage2024c["EMPSTA"].str.replace(pat="1_BIT", repl="Actif")
DfChomage2024c["EMPSTA"] = DfChomage2024c["EMPSTA"].str.replace(pat="2_BIT", repl="Chômeur")
DfChomage2024c["EMPSTA"] = DfChomage2024c["EMPSTA"].str.replace(pat="3_BIT", repl="Inactif")

#As I see, the dataset has age brackets (T25T49 so 25yo to 49yo) and single age values (Y30), now I'll try to see if the sum of Y25 to Y49 = Y25T49 for example
#print(DfChomage2024c["AGE"].value_counts().head(20))
#I can tell from a glance that they are not equal, the survey must have counted them independentaly which means I'll focus on specific age brackets for my study, from 20 Y/O to 64 Y/O. 
# There are many other brackets that overlap each others so I'll go with simplicity
#Cleaning AGE
AGE_map ={"Y20T24":("20-24 ans",1), "Y25T49":("25-49 ans",2),"Y50T64":("50-64 ans",3)}
DfChomage2024c = DfChomage2024c[DfChomage2024c["AGE"].isin(AGE_map.keys())]

DfChomage2024c[["AGE_LABEL", "AGE_SORT"]] = DfChomage2024c["AGE"].map(AGE_map).apply(pd.Series)

print(DfChomage2024["EDUC"].value_counts())
#print(DfChomage2024c["AGE_LABEL"].value_counts())
#print(DfChomage2024c["AGE_SORT"].value_counts())

#Cleaning EDUC
EDUC_map={"0T2":("Aucun diplôme",1),"3_X_353":("Baccalauréat",2),"3A":("CAP/BEP",3),"4T5":("Bac+2",4),"6T8":("Bac+3 et plus",5)}

DfChomage2024c = DfChomage2024c[DfChomage2024c["EDUC"].isin(EDUC_map.keys())]

DfChomage2024c[["EDUC_LABEL","EDUC_SORT"]] = DfChomage2024c["EDUC"].map(EDUC_map).apply(pd.Series)

#Time for the agregate, we set up our conditions for the final dataset
df = DfChomage2024c[
    (DfChomage2024c["EEC_MEASURE"] == "UNEMPRATE") &
    (DfChomage2024c["UNIT_MEASURE"] == "PT") &                                        #PT is percentage so a rate
    (DfChomage2024c["EMPSTA"] == "Chômeur")]                                          #What we want so unemployment

df=df.copy()
df_final = (df.groupby(["AGE_LABEL", "AGE_SORT", "EDUC_LABEL", "EDUC_SORT"],as_index=False)["OBS_VALUE"].mean())
df_final.rename(columns={"OBS_VALUE":"Taux_chômage"}, inplace=True)
df_final = df_final.sort_values(by=["AGE_LABEL","Taux_chômage"], ascending=[True, False])


df_final.to_csv(r"e:\Datasets\Taux_chômage_2024_âge_education.csv", index=False)

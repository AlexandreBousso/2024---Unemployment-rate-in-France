import pandas as pd 
DfChomage2024 = pd.read_csv("DD_EEC_ANNUEL_2024_data.csv", sep=";")
DfChomage2024c= DfChomage2024.dropna(subset=["OBS_VALUE"]).copy()

#cleaning EMPFORM 
#(DfChomage2024c["EMPFORM"] = DfChomage2024c["EMPFORM"].str.replace(pat="11", repl="Indé")
#DfChomage2024c["EMPFORM"] = DfChomage2024c["EMPFORM"].str.replace(pat="2", repl="Salarié")
#DfChomage2024c["EMPFORM"] = DfChomage2024c["EMPFORM"].str.replace(pat="211", repl="CDI/Fonct")
#DfChomage2024c["EMPFORM"] = DfChomage2024c["EMPFORM"].str.replace(pat="22", repl="CDD")
#DfChomage2024c["EMPFORM"] = DfChomage2024c["EMPFORM"].str.replace(pat="22_GE3M", repl="CDD_Less3M")
#DfChomage2024c["EMPFORM"] = DfChomage2024c["EMPFORM"].str.replace(pat="22_LT3M", repl="CDD_More3M")
#DfChomage2024c["EMPFORM"] = DfChomage2024c["EMPFORM"].str.replace(pat="23_25_27", repl="Alt/Stg/ContratAid")
#DfChomage2024c["EMPFORM"] = DfChomage2024c["EMPFORM"].str.replace(pat="23T25", repl="Alt/Stg/ContratAid")
#DfChomage2024c["EMPFORM"] = DfChomage2024c["EMPFORM"].str.replace(pat="26", repl="Interim")
#DfChomage2024c["EMPFORM"] = DfChomage2024c["EMPFORM"].str.replace(pat="271", repl="NoCont/Uknwn"))
#cleaning EMPSTA
DfChomage2024c["EMPSTA"] = DfChomage2024c["EMPSTA"].str.replace(pat="1_BIT", repl="Actif")
DfChomage2024c["EMPSTA"] = DfChomage2024c["EMPSTA"].str.replace(pat="2_BIT", repl="Chômeur")
DfChomage2024c["EMPSTA"] = DfChomage2024c["EMPSTA"].str.replace(pat="3_BIT", repl="Inactif")

#Cleaning PCS (Profession et catégorie socioprofessionnelles). I try the mapping method to have a comparison with the str.replace
PCS_mapping ={
    "_X": "NoValue",
    "10": "Agriculteurs",
    "20": "Arti,Commerc,ChefEntre",
    "2_NP": "Arti,Commerc,ChefEntreNP",
    "21" : "Artistans",
    "22": "Commerçant&assimilé",
    "23": "ChefEntre_10>salarié",
    "3_NP":"Cadre_NP",
    "30" : "Cadres",
    "30_NP": "Cadre_NP",
    "31" : "Profession_Libérale",
    "33" : "Cadres Admin/tech FonctPub",
    "34" : "Enseignants & Profession ScienSupp",
    "35" : "Information, Art et Spectacles",
    "37" : "Cadre Admni & Commerciaux Entre",
    "38" : "Ingénieurs & Cadre Techniques",
    "4_NP" :" Profession Intermédiaire NP",
    "40": "Profession Intérmédiaire",
    "42" : "Enseign primaire & pro, form continue & sport"
}
DfChomage2024c["PCS"]=DfChomage2024c["PCS"].replace(PCS_mapping)
print("PCS NaN", DfChomage2024c["PCS"].isna().sum())


#Cleaning EMPFORM 2.0. Transforming ENSEE codes into readable values
EMPFORM_mapping = {
    "11":"Indé",
    "2":"Salarié",
    "211":"CDI/Fonctionnaire",
    "22":"CDD",
    "22_GE3M":"CDD_Less3M",
    "22_LT3M":"CDD_More3M",
    "23_25_27": "Alt/Stg/ContratSubv",
    "23T25":"Alt/Stg/ContratSub",
    "26":"Interim",
    "271":"NoContract/Ukwn"
}
DfChomage2024c["EMPFORM"]=DfChomage2024c["EMPFORM"].replace(EMPFORM_mapping)
DfChomage2024c["EMPFORM"].value_counts()
print("EMPFORM NaN", DfChomage2024c["EMPFORM"].isna().sum())

#Cleaning EDUC column, it displays the level of education, it ranges from no diploma to Master-PhD
EDUC_mapping = {
    "0T2":"Sans Diplôme",
    "3_X_353":"Baccalauréat",
    "3A": "CAP,BEP",
    "4T5":"Bac+2",
    "540_550":"Bac+2",
    "600T800":"Bac+3 et +",
}
DfChomage2024c["EDUC_LEVEL"]=DfChomage2024c["EDUC"].map(EDUC_mapping).fillna("Autre/non Precisé")
DfChomage2024c["EDUC_LEVEL"].isna().sum()

#Cleaning AGE to make it more readable because there are way too many age codes and age classes. I do a value_counts() to hightlight meaningful values
age_counts = DfChomage2024c["AGE"].value_counts()
print(age_counts)

#I arbitrarly define a threshold of counted values, above this threshold, I count the vlaue and below they go in a separate category
age_major = age_counts[age_counts > 100].index
#print(age_major)
#I can now observe the values I want to work on and rename for readability purposes

AGE_mapping = {
    "Y15T19":"15-19ans",
    "Y15T24":"15-24ans",
    "Y15T29":"15-29ans",
    "Y15T64":"15-64ans",
    "Y15T74":"15-74ans",
    "Y15T89":"15-89ans",
    "Y20T24":"20-24ans",
    "Y25T49":"25-49 ans",
    "Y50T64":"50-64ans",
    "Y65T89":"65-89ans",
    "Y_GE15":"15ans ou +",
    "Y_GE65":"65ans ou +",
    "Y_GE75":"75ans ou +"

}

#DfChomage2024c["AGE"]=DfChomage2024c["AGE"].map(AGE_mapping) Here I'll adopt the .replace method because I don't want to rename all the values
DfChomage2024c["AGE_LABEL"]=DfChomage2024c["AGE"].replace(AGE_mapping)
DfChomage2024c["AGE_LABEL"].isna().sum()
DfChomage2024c["AGE_LABEL"].value_counts

#I want to illustrate the unemployement(rate and length) factoring the level of education and age, basic filter we select the lines with 2024(all of them in this case) and where the persons are Unenmployed
DFforAnalysis= DfChomage2024c[(DfChomage2024c["TIME_PERIOD"]== 2024) & (DfChomage2024c["EMPSTA"]=="Chômeur")]


#Verification, removed the print to not have excess information on the terminal
DFforAnalysis["TIME_PERIOD"].unique()
DFforAnalysis["EMPSTA"].value_counts()
#I observe here that we have 2 differents units, PT which is a percentage and _Z which is a non-standard value/unit. I'll take the PT for my study
DFforAnalysis = DFforAnalysis[DFforAnalysis["UNIT_MEASURE"] == "PT"]
print(DFforAnalysis["UNIT_MEASURE"].value_counts())




#Now I'm grouping the data by level of education and age
chomage_age_diplome = (DFforAnalysis.groupby(["EDUC_LEVEL", "AGE_LABEL"],as_index=False)["OBS_VALUE"].mean())
chomage_age_diplome.rename(columns={"OBS_VALUE":"Taux_chômage"}, inplace=True)
chomage_age_diplome = chomage_age_diplome.sort_values(by=["AGE_LABEL","Taux_chômage"], ascending=[True, False])
print(chomage_age_diplome["Taux_chômage"].describe())

chomage_age_diplome.to_csv(r"e:\Datasets\Taux_chômage_2024.csv", index=False)

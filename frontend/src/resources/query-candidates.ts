type QueryCand = {
  key: string;
  title: string;
  text: string;
};

const obesityCandidates: Record<string, QueryCand> = {
  "dixon-peters-2018": {
    key: "dixon-peters-2018",
    title:
      "Dixon, Anne E, and Ubong Peters. “The effect of obesity on lung function.” Expert review of respiratory medicine vol. 12,9 (2018): 755-767.",
    text: `\
There is a major epidemic of obesity, and many obese patients suffer with respiratory symptoms and disease. The overall impact of obesity on lung function is multifactorial, related to mechanical and inflammatory aspects of obesity. Areas covered: Obesity causes substantial changes to the mechanics of the lungs and chest wall, and these mechanical changes cause asthma and asthma-like symptoms such as dyspnea, wheeze, and airway hyperresponsiveness. Excess adiposity is also associated with increased production of inflammatory cytokines and immune cells that may also lead to disease. This article reviews the literature addressing the relationship between obesity and lung function, and studies addressing how the mechanical and inflammatory effects of obesity might lead to changes in lung mechanics and pulmonary function in obese adults and children. Expert commentary: Obesity has significant effects on respiratory function, which contribute significantly to the burden of respiratory disease. These mechanical effects are not readily quantified with conventional pulmonary function testing and measurement of body mass index. Changes in mediators produced by adipose tissue likely also contribute to altered lung function, though as of yet this is poorly understood.`,
  },
  "ishikawa-et-al-2021": {
    key: "ishikawa-et-al-2021",
    title:
      "Ishikawa, C., Barbieri, M.A., Bettiol, H. et al. Comparison of body composition parameters in the study of the association between body composition and pulmonary function. BMC Pulm Med 21, 178 (2021).",
    text: `\
Obesity is known to affect pulmonary function regardless of the presence of respiratory, cardiovascular, or metabolic diseases , interfering with respiratory mechanics and lung-thorax compliance. Furthermore, studies have demonstrated that adipose tissue, especially the visceral adipose tissue, is an active tissue in terms of inflammation (cytokine production) and endocrinological activity, releasing hormones that also interfere with pulmonary function .
This study has several strengths. It has used cross-sectional data from a birth cohort, which allowed us to obtain a large and representative sample of the population studied, in addition to being subjected to standardization and quality techniques of a longitudinal study in which the responsibility to record detailed quality data is fundamental. Additionally, the study employed sophisticated and accurate methods for body composition measurement. On the other hand, the study has limitations. Its cross-sectional design does not allow to evaluate the causal relationship between body composition and pulmonary function reduction, nor how weight evolution over the time influences the maximal lung function and its decline over the years. The study used a population sample with a limited age range from the city of Ribeirão Preto, whose socioeconomic pattern differs from that of most other Brazilian cities, impairing generalization of our findings to other ages and regions. The original project also did not have this study as the central objective. It is difficult to extract data from a questionnaire that was predefined with other initial general objectives. Some anthropometric parameters such as hip circumference and skinfold thickness that could be useful for comparison with other publications were not measured.`,
  },
  "rhee-et-al-2016": {
    key: "rhee-et-al-2016",
    title:
      "Rhee CM, Ahmadi SF, Kalantar-Zadeh K. The dual roles of obesity in chronic kidney disease: a review of the current literature. Curr Opin Nephrol Hypertens. 2016 May;25(3):208-16.",
    text: `\
PURPOSE OF REVIEW: Obesitysubject: Obesity is a major risk factor for the development of de novo chronic kidney disease (CKD). However, once kidney disease is acquired, obesitysubject: Obesity is paradoxically linked with greater survival, especially in those with advanced CKD. This review examines current evidence for obesitysubject: Obesity as a risk factor for incident CKD, studies of obesitysubject: Obesity and mortality across various CKD populations, and potential mechanisms underlying the 'obesitysubject: Obesity paradox' in kidney disease.RECENT FINDINGS: Large cohort studies show that overweight body habitus, especially in the context of metabolic syndrome, is associated with higher risk of incident CKD. Emerging data also suggest weight-loss interventions retard or reverse early CKD progression, whereas in hemodialysis patients weight-loss paradoxically heralds poor outcomes. Although the pathogenesis of CKD in obesitysubject: Obesity remains unclear, studies indicate that excess body fat leads to kidney disease via indirect and direct mechanisms. Meta-analyses suggest that overweight and obese BMI ranges are counterintuitively associated with lower mortality in advanced predialysis and dialysis-dependent CKD patients, whereas a pooled analysis observed that higher pretransplantation BMI was associated with higher mortality in kidney transplantation recipients.SUMMARY: In addition to its role as a risk factor for de novo CKD, there appears to be a consistent association between obesitysubject: Obesity and lower mortality in those with established CKD, particularly among hemodialysis patients, suggesting that the reverse epidemiology of obesitysubject: Obesity is biologically plausible.`,
  },
};

const hypertensionCandidates: Record<string, QueryCand> = {
  "guvenc-et-al-2012": {
    key: "guvenc-et-al-2012",
    title:
      "Güvenc TS, Erer HB, Ilhan S, Zeren G, Ilhan E, Karakuş G, Sayar N, Orhan AL, Eren M. Comparison of mean platelet volume values among different causes of pulmonary hypertension. Cardiol J. 2012;19(2):180-7.",
    text: `\
Background: Pulmonary hypertension is caused by a heterogenous group of disorders with diverse pathophysiological mechanisms, with ultimate structural changes in the pulmonary vascular bed. Platelet activation plays an important role in the development of pulmonary arterial hypertension, while it is unknown whether it contributes to pathogenesis in other conditions. We aimed to investigate platelet activation in different causes of pulmonary hypertension by means of mean platelet volume measurement.
Methods: A total of 67 patients with different causes of pulmonary hypertension, and 31 controls, were retrospectively reviewed. Patients with pulmonary hypertension were further grouped according to underlying disease, including pulmonary arterial hypertension, pulmonary hypertension due to left ventricular failure, and pulmonary hypertension due to chronic obstructive pulmonary disorder. All patients and controls past medical data, admission echocardiograms and complete blood counts were reviewed.
Results: Patients with pulmonary hypertension had higher mean platelet volume levels compared to healthy controls (8.77 ± 1.18 vs 7.89 ± 0.53; p < 0.001), and statistical significance was still present when pulmonary arterial hypertension patients were not included in the pulmonary hypertension group (8.59 ± 1.23 vs 7.89 ± 0.53; p < 0.001). Among patients with pulmonary hypertension, the pulmonary arterial hypertension group and the pulmonary hypertension due to left ventricular failure group had higher mean platelet volumes compared to healthy controls. Mean platelet volume did not correlate with pulmonary artery pressure.
Conclusions: Our results indicate that mean platelet volume is not only elevated in pulmonary arterial hypertension, but also due to other causes of pulmonary hypertension.`,
  },
  "shibata-itoh-2012": {
    key: "shibata-itoh-2012",
    title:
      "Shibata H, Itoh H. Mineralocorticoid receptor-associated hypertension and its organ damage: clinical relevance for resistant hypertension. Am J Hypertens. 2012 May;25(5):514-23.",
    text: `\
The role of aldosterone in the pathogenesis of hypertension and cardiovascular diseases has been clearly shown in congestive heart failure and endocrine hypertension due to primary aldosteronism. In resistant hypertension, defined as a failure of concomitant use of three or more different classes of antihypertensive agents to control blood pressure (BP), add-on therapy with mineralocorticoid receptor (MR) antagonists is frequently effective, which we designate as "MR-associated hypertension". The MR-associated hypertension is classified into two subtypes, that with elevated plasma aldosterone levels and that with normal plasma aldosterone levels. The former subtype includes primary aldosteronism (PA), aldosterone-associated hypertension which exhibited elevated aldosterone-to-renin ratio and plasma aldosterone levels, but no PA, aldosterone breakthrough phenomenon elicited when angiotensin-converting enzyme inhibitor (ACE-I) or angiotensin II receptor blocker (ARB) is continued to be given, and obstructive sleep apnea. In contrast, the latter subtype includes obesity, diabetes mellitus, chronic kidney disease (CKD), and polycystic ovary syndrome (PCOS). The pathogenesis of MR-associated hypertension with normal plasma aldosterone levels is considered to be mediated by MR activation by pathways other than high aldosterone levels, such as increased MR levels, increased MR sensitivity, and MR overstimulation by other factors such as Rac1. For resistant hypertension with high plasma aldosterone levels, MR antagonist should be given as a first-line therapy, whereas for resistant hypertension with normal aldosterone levels, ARB or ACE-I should be given as a first-line therapy and MR antagonist would be given as an add-on agent.`,
  },
};

export const topics: Record<
  string,
  {
    key: string;
    label: string;
    candidates: Record<string, QueryCand>;
  }
> = {
  obesity: {
    key: "obesity",
    label: "Obesity, overweight, and high BMI",
    candidates: obesityCandidates,
  },
  hypertension: {
    key: "hypertension",
    label: "Hypertension and heart diseases",
    candidates: hypertensionCandidates,
  },
};

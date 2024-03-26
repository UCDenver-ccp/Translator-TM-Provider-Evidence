# Evidence Service

Simple API for retrieving all the sentences used as evidence for a given assertion. 
Exposes three endpoint:

The root endpoint `/` returns a list of 5 random assertion ids (useful for testing and health checks)

-`/version` simply returns the current version as a string

-`/api/sentences/` accepts a JSON list of assertion or evidence IDs (the same list can have both types) and returns 
all evidence for the assertion. If an ID is for evidence the service will return all evidence for the associated assertion.
The request JSON can also provide `limit` and `threshold` attributes. `limit` will cap the total number of evidence 
records returned per assertion, and `threshold` will only return evidence records with `score` >= `threshold`. 

The example input
```
{
	"ids": ["122f3d2f8876dc6856866f9b69922f31e8879e7470134c0348f74c84d688cad1"]
}
```
yields the output
```
[
	{
		"assertion_id": "fca14abfe19059f76cf65c9b3c5f65996ee254251fa0b163df24d0c8308dbe76",
		"subject": "CHEBI:28499",
		"object": "MONDO:0002771",
		"association": "biolink:ChemicalToDiseaseOrPhenotypicFeatureAssociation",
		"evidence_list": [
			{
				"evidence_id": "10c1564e96e542380bdf824a83dd4a5ce2d141643056cf96f325d20147658f1d",
				"sentence": "Kaempferol Modulates Autophagy and Alleviates Silica-Induced Pulmonary Fibrosis",
				"document_id": "PMC7697279",
				"document_zone": "reference",
				"document_year": 2020,
				"subject_span_start": "0",
				"subject_span_end": "10",
				"subject_text": "Kaempferol",
				"object_span_start": "61",
				"object_span_end": "79",
				"object_text": "Pulmonary Fibrosis",
				"predicate": "biolink:treats",
				"score": 0.9994816
			},
			{
				"evidence_id": "122f3d2f8876dc6856866f9b69922f31e8879e7470134c0348f74c84d688cad1",
				"sentence": "The above researches illustrate that COVID-19 and PF share the common targeting pathways, and IL-17, TNF, HIF-1, EGFR, PI3K/AKT and Toll-like receptor signaling pathways were the critical mechanisms of kaempferol against COVID-19/PF co-occurrence.",
				"document_id": "PMC9214245",
				"document_zone": "DISCUSS",
				"document_year": 2022,
				"subject_span_start": "202",
				"subject_span_end": "212",
				"subject_text": "kaempferol",
				"object_span_start": "50",
				"object_span_end": "52",
				"object_text": "PF",
				"predicate": "biolink:treats",
				"score": 0.9913503
			},
			{
				"evidence_id": "162cc78a9587934242771915dbb10b7260b53e76ad35ba2196c43d86e6b4d4d9",
				"sentence": "Methods: Various open-source databases and Venn Diagram tool were applied to confirm the targets of kaempferol against COVID-19/PF co-occurrence.",
				"document_id": "PMC9214245",
				"document_zone": "ABSTRACT",
				"document_year": 2022,
				"subject_span_start": "100",
				"subject_span_end": "110",
				"subject_text": "kaempferol",
				"object_span_start": "128",
				"object_span_end": "130",
				"object_text": "PF",
				"predicate": "biolink:treats",
				"score": 0.9812836
			},
			{
				"evidence_id": "1d96ec20552f090b04d1df8f84c8d5c2874791c3944f598b64945988f8678cec",
				"sentence": "The above researches illustrate that COVID-19 and PF share the common targeting pathways, and IL-17, TNF, HIF-1, EGFR, PI3K/AKT and Toll-like receptor signaling pathways were the critical mechanisms of kaempferol against COVID-19/PF co-occurrence.",
				"document_id": "PMC9214245",
				"document_zone": "DISCUSS",
				"document_year": 2022,
				"subject_span_start": "202",
				"subject_span_end": "212",
				"subject_text": "kaempferol",
				"object_span_start": "230",
				"object_span_end": "232",
				"object_text": "PF",
				"predicate": "biolink:treats",
				"score": 0.9992717
			},
			{
				"evidence_id": "53e7908f3334d9a373dda06b1e68af92ed48404b08ca74f588b21214de73d384",
				"sentence": "In a mice model of severe progressive pulmonary fibrosis, kaempferol significantly inhibits pulmonary inflammation and inflammatory cells infiltration, through the restoration of LC3 lipidation and a concomitant increase in autophagy flux.",
				"document_id": "PMC7697279",
				"document_zone": "INTRO",
				"document_year": 2020,
				"subject_span_start": "58",
				"subject_span_end": "68",
				"subject_text": "kaempferol",
				"object_span_start": "38",
				"object_span_end": "56",
				"object_text": "pulmonary fibrosis",
				"predicate": "biolink:treats",
				"score": 0.9994424
			},
			{
				"evidence_id": "73e7045215392211ec6189162963309e4415befcd7f2f870192076f10592ab34",
				"sentence": "The underlying mechanisms of kaempferol against COVID-19/PF co-occurrence may be related to bind to EGFR, SRC, MAPK3, MAPK1, MAPK8, AKT1, RELA and PIK3CA.",
				"document_id": "PMC9214245",
				"document_zone": "CONCL",
				"document_year": 2022,
				"subject_span_start": "29",
				"subject_span_end": "39",
				"subject_text": "kaempferol",
				"object_span_start": "57",
				"object_span_end": "59",
				"object_text": "PF",
				"predicate": "biolink:treats",
				"score": 0.9989693
			},
			{
				"evidence_id": "7edc89b663c4b2e05cdf701869fdd665dd64dcdb69c8158c5d9ceb8ea0d0683d",
				"sentence": "The detailed strategy of exploring the targets and mechanisms of kaempferol against COVID-19/PF co-occurrence by bioinformatics and network pharmacology is shown in Figure 1.",
				"document_id": "PMC9214245",
				"document_zone": "INTRO",
				"document_year": 2022,
				"subject_span_start": "65",
				"subject_span_end": "75",
				"subject_text": "kaempferol",
				"object_span_start": "93",
				"object_span_end": "95",
				"object_text": "PF",
				"predicate": "biolink:treats",
				"score": 0.999432
			},
			{
				"evidence_id": "9178b6ab27cae44177c223ead6ff83f52f5b4a4c10a0306df4b8538840a60690",
				"sentence": "The top 15 targets and components are shown in Tables 1 and 2. Among the components, 3-O-methylfunicone (OMF), panaxytriol, brevisamide, 3,3?,4?,5,6,7,8-heptamethoxyflavone, ruscogenin, liquiritin, formononetin, luteolin, kaempferol, and hesperetin showed strong interactions with 10 or more PF targets, and might be the bioactive constituents of JSHX against PF.",
				"document_id": "PMC9304367",
				"document_zone": "paragraph",
				"document_year": 2022,
				"subject_span_start": "222",
				"subject_span_end": "232",
				"subject_text": "kaempferol",
				"object_span_start": "360",
				"object_span_end": "362",
				"object_text": "PF",
				"predicate": "biolink:treats",
				"score": 0.9818647
			},
			{
				"evidence_id": "92ae624d2e3696df86d05bc5871b3af3cfec996f628237018cc6deec74da9263",
				"sentence": "Therefore, this study explored the targets and molecular mechanisms of kaempferol against COVID-19/PF co-occurrence by bioinformatics and network pharmacology.",
				"document_id": "PMC9214245",
				"document_zone": "paragraph",
				"document_year": 2022,
				"subject_span_start": "71",
				"subject_span_end": "81",
				"subject_text": "kaempferol",
				"object_span_start": "99",
				"object_span_end": "101",
				"object_text": "PF",
				"predicate": "biolink:treats",
				"score": 0.9994504
			},
			{
				"evidence_id": "9f91a5d6c57bbb029116bf70f3a033e5d2c39cd03cd1c7b2e0b51eeafc1b06d7",
				"sentence": "Thus, this study analyzed potential targets and mechanisms of kaempferol against COVID-19/PF co-occurrence by integrating bioinformatics and system pharmacological tools.",
				"document_id": "PMC9214245",
				"document_zone": "paragraph",
				"document_year": 2022,
				"subject_span_start": "62",
				"subject_span_end": "72",
				"subject_text": "kaempferol",
				"object_span_start": "90",
				"object_span_end": "92",
				"object_text": "PF",
				"predicate": "biolink:treats",
				"score": 0.9994405
			},
			{
				"evidence_id": "fc716a7838fef22b6e88848814a21bb4fe23d4a5da906b61622fb27bc9d8dea2",
				"sentence": "Kaempferol Modulates Autophagy and Alleviates Silica-Induced Pulmonary Fibrosis",
				"document_id": "PMC7795780",
				"document_zone": "reference",
				"document_year": 2021,
				"subject_span_start": "0",
				"subject_span_end": "10",
				"subject_text": "Kaempferol",
				"object_span_start": "61",
				"object_span_end": "79",
				"object_text": "Pulmonary Fibrosis",
				"predicate": "biolink:treats",
				"score": 0.9994816
			}
		]
	}
]
```
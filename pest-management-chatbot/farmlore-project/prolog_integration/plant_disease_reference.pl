% ========================
% PLANT DISEASE REFERENCE KNOWLEDGE BASE
% ========================
% Contains general educational information about plant diseases for reference

% Ensure compatibility with existing knowledge base
:- discontiguous(frame/2).

% ========================
% FRAME TEMPLATES
% ========================
frame(disease_general, [
    name: atom,
    category: atom,
    description: string,
    characteristics: list(atom),
    context: list(atom)
]).

frame(disease_type, [
    name: atom,
    pathogen_type: atom,
    description: string,
    examples: list(atom),
    context: list(atom)
]).

frame(disease_management, [
    name: atom,
    category: atom,
    description: string,
    methods: list(atom),
    context: list(atom)
]).

frame(specific_disease, [
    name: atom,
    type: atom,  % 'fungal', 'bacterial', 'viral', 'physiological_disorder', 'nematode', 'parasitic_plant'
    scientific_name: atom,
    description: string,
    symptoms: string,
    host_plants: list(atom),
    spread_mechanism: string,
    conditions_favoring: list(atom),
    prevention_methods: list(atom),
    control_methods: list(atom),
    region: list(atom)
]).

% ========================
% TAXONOMY & ONTOLOGY
% ========================
% Disease Classification
subclass(plant_disease, plant_health_issue).
subclass(infectious_disease, plant_disease).
subclass(non_infectious_disease, plant_disease).
subclass(disorder, non_infectious_disease).

% Infectious Disease Types
subclass(fungal_disease, infectious_disease).
subclass(bacterial_disease, infectious_disease).
subclass(viral_disease, infectious_disease).
subclass(nematode_disease, infectious_disease).
subclass(parasitic_plant_disease, infectious_disease).

% Non-infectious Disease Types
subclass(environmental_disorder, disorder).
subclass(cultural_disorder, disorder).
subclass(nutritional_disorder, disorder).
subclass(genetic_disorder, disorder).

% ========================
% GENERAL DISEASE INFORMATION
% ========================
frame(disease_general, [
    name: plant_disease_definition,
    category: basic_concept,
    description: 'Disease is an irritation that disturbs a plant\'s normal functions (such as water uptake or cell division). Some scientists further restrict the definition to conditions or organisms that cause continuous irritation. Infectious diseases are those that can be transmitted from one plant to another. Noninfectious diseases—called plant disorders—are problems that cannot be transmitted.',
    characteristics: [
        disrupts_plant_functions,
        may_be_infectious_or_non_infectious,
        causes_abnormal_growth_or_appearance,
        may_reduce_yield_or_quality,
        may_cause_plant_death
    ],
    context: [educational_reference, disease_identification]
]).

frame(disease_general, [
    name: disease_development,
    category: disease_cycle,
    description: 'Disease development depends on an interaction between the host plant, the pathogen, and the environment. Before any disease symptoms show up, three conditions must be met: the pathogen must be present, there must be a susceptible plant, and environmental conditions must be favorable. The disease cycle includes inoculation (contact with the plant), penetration and infection, incubation and invasion, reproduction, dissemination, and overwintering.',
    characteristics: [
        requires_pathogen_presence,
        requires_susceptible_host,
        requires_favorable_environment,
        follows_disease_cycle,
        can_be_interrupted
    ],
    context: [disease_management, preventive_approach]
]).

frame(disease_general, [
    name: plant_defenses,
    category: disease_resistance,
    description: 'Plants have natural defenses against disease, including structural defenses like thick waxy leaf surfaces or impenetrable cell walls that can stop pathogens, and chemical defenses including biochemicals that are toxic to fungi or bacteria. Some protective biochemicals are produced only after a plant has been attacked by a disease-causing organism.',
    characteristics: [
        structural_defenses,
        preexisting_chemical_defenses,
        induced_chemical_defenses,
        varying_resistance_levels
    ],
    context: [plant_immunity, disease_management, breeding_for_resistance]
]).

% ========================
% DISEASE TYPES
% ========================
frame(disease_type, [
    name: fungal_diseases,
    pathogen_type: fungi,
    description: 'Fungi are responsible for many common plant diseases. Fungi are multi-celled and have threadlike bodies called hyphae that spread over plants. Fungi form spores, which are tiny, seedlike structures that can travel great distances and are more tolerant of unfavorable conditions than actively growing hyphae. Most fungi produce multiple types of spores during their life cycles.',
    examples: [
        powdery_mildew,
        damping_off,
        late_blight,
        apple_scab,
        corn_smut,
        root_rot,
        early_blight,
        leaf_spot,
        rust
    ],
    context: [
        most_common_plant_pathogens,
        spores_key_to_spread,
        favored_by_moisture,
        may_attack_specific_plant_parts
    ]
]).

frame(disease_type, [
    name: bacterial_diseases,
    pathogen_type: bacteria,
    description: 'Bacteria are single-celled organisms large enough to be visible through a common light microscope. About 200 different bacteria can cause plant diseases. Bacteria divide rapidly by fission and can enter plants through wounds or natural openings. Warmth and moisture are most conducive to bacterial growth, so bacterial diseases generally are worse in warm, humid climates.',
    examples: [
        soft_rot,
        crown_gall,
        fire_blight,
        bacterial_wilt,
        bacterial_leaf_spot,
        bacterial_canker
    ],
    context: [
        require_wound_or_opening_for_entry,
        produce_sticky_gummy_material,
        favored_by_warm_humid_conditions,
        spread_by_water_and_insects
    ]
]).

frame(disease_type, [
    name: viral_diseases,
    pathogen_type: virus,
    description: 'Viruses are the smallest plant pathogens, consisting of nucleic acid surrounded by a protein sheath. They can only be seen with an electron microscope and are inactive outside of living cells. Once inside a live cell, viruses use the cell\'s machinery to multiply, upsetting the cell\'s metabolism and causing disease. A single infected plant cell may become home to over a million virus particles.',
    examples: [
        cucumber_mosaic,
        tobacco_mosaic,
        tomato_spotted_wilt,
        peach_rosette,
        dahlia_ring_spot,
        bean_mosaic
    ],
    context: [
        require_vectors_for_spread,
        difficult_to_control,
        no_cure_once_infected,
        prevention_critical
    ]
]).

frame(disease_type, [
    name: nematode_diseases,
    pathogen_type: nematodes,
    description: 'Nematodes are multi-cellular animals with smooth, unsegmented bodies. They are often described as worm-like but are not closely related to true worms. Plant-parasitic nematodes have sharply pointed mouthparts to puncture cell walls and inject saliva, then suck out the cell contents. The plant responds with swellings, distorted growth, and dead areas.',
    examples: [
        root_knot,
        lesion_nematodes,
        cyst_nematodes,
        foliar_nematodes
    ],
    context: [
        mostly_affect_roots,
        spread_through_soil_movement,
        some_species_affect_above_ground_parts,
        can_transmit_viruses
    ]
]).

frame(disease_type, [
    name: parasitic_plant_diseases,
    pathogen_type: parasitic_plants,
    description: 'Unlike most plants, parasitic plants seldom produce their own food through photosynthesis. Instead, these plants attach themselves to host plants and withdraw water and nutrients from the hosts. The two most common parasitic plants are mistletoe and dodder.',
    examples: [
        mistletoe,
        dodder,
        broomrape,
        witchweed
    ],
    context: [
        attach_to_host_plants,
        withdraw_water_and_nutrients,
        spread_by_birds_or_seeds,
        difficult_to_control_once_established
    ]
]).

frame(disease_type, [
    name: physiological_disorders,
    pathogen_type: non_infectious,
    description: 'Various environmental and cultural problems are considered diseases since they upset the plant\'s normal function. Because such diseases cannot be transmitted from one plant to the next, they are called noninfectious diseases or physiological disorders. Environmental problems are caused by a lack or excess of something that a plant needs to grow, while cultural problems are the things people and other animals do that injure plants.',
    examples: [
        nutrient_deficiency,
        temperature_stress,
        drought_stress,
        oxygen_deficiency,
        herbicide_damage,
        physical_injury,
        air_pollution_damage
    ],
    context: [
        not_caused_by_pathogens,
        not_transmissible,
        related_to_growing_conditions,
        often_resemble_infectious_diseases
    ]
]).

% ========================
% DISEASE SYMPTOMS
% ========================
frame(disease_general, [
    name: leaf_spot_symptoms,
    category: symptom_pattern,
    description: 'Leaf spots are localized lesions on leaves characterized by dead tissue. They can be circular, angular, or irregular and may be various colors including brown, black, tan, or reddish. Some spots have distinctive patterns such as concentric rings or yellow haloes. As the disease progresses, spots may enlarge, coalesce, and cause the leaf to die and drop prematurely.',
    characteristics: [
        necrotic_areas_on_leaves,
        variable_in_shape_and_color,
        may_have_distinctive_patterns,
        can_cause_defoliation
    ],
    context: [fungal_bacterial_diseases, disease_diagnosis]
]).

frame(disease_general, [
    name: blight_symptoms,
    category: symptom_pattern,
    description: 'When plants suffer from blight, leaves or branches suddenly wither, stop growing, and die. Later, plant parts may rot. Blights can rapidly kill large areas of plant tissue and are often caused by fungi or bacteria. Common blights include fire blight, Alternaria blight, and bacterial blights.',
    characteristics: [
        rapid_tissue_death,
        withering_of_leaves_or_branches,
        sudden_onset,
        may_be_followed_by_rot
    ],
    context: [fungal_bacterial_diseases, disease_diagnosis]
]).

frame(disease_general, [
    name: canker_symptoms,
    category: symptom_pattern,
    description: 'Cankers usually form on woody stems and may be cracks, sunken areas, or raised areas of dead or abnormal tissue. Sometimes cankers ooze conspicuously. Cankers can girdle shoots or trunks, causing everything above the canker to wilt and die.',
    characteristics: [
        localized_stem_damage,
        may_be_sunken_or_raised,
        may_ooze_sap_or_gum,
        can_cause_dieback_above_infection
    ],
    context: [fungal_bacterial_diseases, woody_plants]
]).

frame(disease_general, [
    name: gall_symptoms,
    category: symptom_pattern,
    description: 'Galls are swollen masses of abnormal tissue. They can be caused by fungi and bacteria as well as certain insects. If you cut open a gall and there is no sign of an insect inside, suspect disease.',
    characteristics: [
        abnormal_growths_on_plant_tissue,
        varied_in_size_and_appearance,
        may_disrupt_water_and_nutrient_flow,
        often_persist_for_the_life_of_the_plant
    ],
    context: [fungal_bacterial_diseases, disease_diagnosis]
]).

frame(disease_general, [
    name: leaf_curl_symptoms,
    category: symptom_pattern,
    description: 'On plants suffering from leaf curl diseases, the new leaves are pale or reddish and the midrib doesn\'t grow properly. The leaves become puckered and curled as they expand. Blisters are yellow bumps on the upper surfaces of the leaves with gray depressions on the lower surfaces.',
    characteristics: [
        distorted_leaf_growth,
        puckering_and_curling,
        abnormal_coloration,
        stunted_growth
    ],
    context: [fungal_viral_diseases, disease_diagnosis]
]).

frame(disease_general, [
    name: mildew_symptoms,
    category: symptom_pattern,
    description: 'There are two common types of mildews: downy mildew and powdery mildew. The primary symptom of downy mildew is a white to purple, downy growth, usually on the undersides of leaves and along stems, which turns black with age. Powdery mildew first appears as a white to grayish powdery growth, usually on the upper surfaces of leaves.',
    characteristics: [
        fungal_growth_on_plant_surfaces,
        powdery_or_downy_appearance,
        may_cause_leaf_distortion,
        can_lead_to_premature_defoliation
    ],
    context: [fungal_diseases, disease_diagnosis]
]).

frame(disease_general, [
    name: rot_symptoms,
    category: symptom_pattern,
    description: 'Rots are diseases that decay roots, stems, wood, flowers, and fruit. Some diseases cause leaves to rot, but those symptoms tend to be described as leaf spots and blights. Rots can be soft and squishy or hard and dry.',
    characteristics: [
        tissue_decay,
        may_be_soft_or_dry,
        often_accompanied_by_odor,
        may_have_fungal_growth_visible
    ],
    context: [fungal_bacterial_diseases, disease_diagnosis]
]).

frame(disease_general, [
    name: rust_symptoms,
    category: symptom_pattern,
    description: 'Rusts are a specific type of fungal disease. Many of them require two different plant species as hosts to complete their life cycles. Typical rust symptoms include a powdery tan to rust-colored coating or soft tentacles. Cedar-apple rust and white pine blister rust are two common rust problems that can appear in home landscapes.',
    characteristics: [
        powdery_pustules_on_plant_surfaces,
        orange_yellow_or_brown_coloration,
        may_require_alternate_hosts,
        complex_life_cycles
    ],
    context: [fungal_diseases, disease_diagnosis]
]).

frame(disease_general, [
    name: wilt_symptoms,
    category: symptom_pattern,
    description: 'Plants wilt when they don\'t get enough water. When fungi or bacteria attack or clog a plant\'s water-conducting system, they can cause permanent wilting, often followed by the death of all or part of the plant. Wilt symptoms may resemble those of blights. Wilting may also be from a cultural problem, such as improper watering.',
    characteristics: [
        drooping_of_leaves_or_stems,
        may_affect_whole_plant_or_parts,
        unresponsive_to_watering,
        often_accompanied_by_vascular_discoloration
    ],
    context: [fungal_bacterial_diseases, disease_diagnosis]
]).

% ========================
% DISEASE MANAGEMENT
% ========================
frame(disease_management, [
    name: disease_prevention,
    category: management_approach,
    description: 'Preventing disease outbreaks in the garden requires optimizing growing conditions for each plant while minimizing the growth of pathogens. This includes providing good drainage, proper air circulation, balanced fertility, appropriate pH, and selecting resistant plant varieties. Exclusion of pathogens through clean seeds and plants, quarantine of new arrivals, and good garden hygiene also helps prevent disease.',
    methods: [
        site_selection,
        resistant_varieties,
        clean_seeds_and_plants,
        quarantine,
        proper_spacing,
        balanced_fertility,
        appropriate_watering,
        crop_rotation
    ],
    context: [
        preventive_approach,
        foundation_of_organic_disease_management,
        reduces_need_for_intervention
    ]
]).

frame(disease_management, [
    name: cultural_controls,
    category: management_approach,
    description: 'Cultural controls focus on creating conditions unfavorable for pathogen development. Proper watering techniques, good air circulation, crop rotation, and sanitation practices like removing infected plant material all help reduce disease pressure. Timing of planting and harvesting can also be adjusted to avoid periods of high disease risk.',
    methods: [
        proper_watering_technique,
        pruning_for_air_circulation,
        crop_rotation,
        sanitation,
        mulching,
        soil_pH_adjustment,
        timing_of_planting,
        resistant_varieties
    ],
    context: [
        preventive_approach,
        long_term_strategies,
        foundation_of_disease_management
    ]
]).

frame(disease_management, [
    name: organic_sprays_and_dusts,
    category: control_measure,
    description: 'Organic fungicides and bactericides act to provide protection against further disease infection. Most form a coating around plant parts, inhibiting the germination of fungal spores, or killing germinated spores or bacteria before they invade the plant. Common organic products include sulfur, lime-sulfur, copper-based compounds like bordeaux mix, and homemade solutions like baking soda spray and garlic spray.',
    methods: [
        sulfur_application,
        lime_sulfur_application,
        copper_based_sprays,
        bordeaux_mix,
        baking_soda_spray,
        garlic_spray,
        neem_oil_spray,
        compost_tea
    ],
    context: [
        preventive_application,
        protective_not_curative,
        timing_critical,
        may_have_limitations
    ]
]).

frame(disease_management, [
    name: biological_controls,
    category: control_measure,
    description: 'Biological control uses living organisms to control disease-producing organisms. This can include beneficial fungi and bacteria that compete with or parasitize pathogens. Adding compost to soil raises the level of organic matter and encourages large populations of beneficial, disease-suppressing organisms. Commercial products like Galltrol-A, which contains nonpathogenic bacteria to control crown gall disease, are also available.',
    methods: [
        beneficial_microorganisms,
        compost_application,
        compost_tea,
        commercial_biological_products,
        soil_building
    ],
    context: [
        works_with_nature,
        self_sustaining_when_established,
        preventive_approach,
        may_take_time_to_establish
    ]
]).

frame(disease_management, [
    name: physical_controls,
    category: control_measure,
    description: 'Physical controls involve manipulating the physical environment to reduce disease. This includes techniques like soil solarization to kill soilborne pathogens, heat treatment of seeds and bulbs, cold storage of harvested crops to slow pathogen growth, and physical barriers like row covers to protect plants from insect vectors of disease.',
    methods: [
        soil_solarization,
        heat_treatment,
        cold_storage,
        physical_barriers,
        pruning_and_removal,
        hot_water_seed_treatment
    ],
    context: [
        may_require_specialized_equipment,
        effective_for_specific_diseases,
        combines_well_with_other_methods,
        often_preventive
    ]
]).

frame(disease_management, [
    name: disease_resistant_varieties,
    category: management_approach,
    description: 'Using disease-resistant plant varieties is one of the most effective ways to prevent disease problems. Resistant plants can occur naturally or be developed through breeding programs. Resistance may be complete (immunity) or partial (tolerance), and can be specific to certain strains of a pathogen. Some plants produce compounds that are toxic to pathogens or create physical barriers that prevent infection.',
    methods: [
        selecting_resistant_varieties,
        understanding_resistance_codes,
        rotating_resistant_varieties,
        combining_with_other_control_methods
    ],
    context: [
        preventive_approach,
        long_term_solution,
        may_have_trade_offs_in_other_traits,
        resistance_can_break_down_over_time
    ]
]).

% ========================
% SPECIFIC DISEASES
% ========================

% Example specific disease entries - more would be added from the provided material
frame(specific_disease, [
    name: anthracnose,
    type: fungal,
    scientific_name: 'Various species',
    description: 'A common fungal disease that affects many plants with characteristic dark spots and lesions.',
    symptoms: 'On leaves, anthracnose diseases generally appear first as small, irregular yellow or brown spots that darken as they age. These spots may also expand and join to cover the leaves. On trees, infection can begin before the leaves appear, killing the tips of young twigs. More often, anthracnose fungi strike the young leaves, producing brown spots and patches. Defoliation may occur, forcing the tree to produce a new set of leaves in the summer.',
    host_plants: [vegetables, trees, ornamentals, dogwoods, maples, sycamores, beans, cucumbers, melons, peppers, tomatoes],
    spread_mechanism: 'Spores spread by water splash, wind, insects, and on tools. Fungi can overwinter in plant debris.',
    conditions_favoring: [warm_temperatures, high_humidity, wet_foliage, poor_air_circulation],
    prevention_methods: [
        resistant_varieties,
        proper_spacing,
        good_air_circulation,
        clean_garden_tools,
        avoid_overhead_watering,
        crop_rotation
    ],
    control_methods: [
        remove_infected_plant_parts,
        apply_copper_fungicides,
        dormant_sprays_for_trees,
        clean_garden_debris,
        water_management
    ],
    region: [north_america, global]
]).

frame(specific_disease, [
    name: apple_scab,
    type: fungal,
    scientific_name: 'Venturia inaequalis',
    description: 'A serious fungal disease of apple and crabapple trees that affects leaves and fruit.',
    symptoms: 'Symptoms first appear on leaves as olive green spots that gradually turn black. These spots may expand and run together, forming large blotches. Leaves may drop prematurely. The leaves may be deformed or smaller than normal. Brown or black spots may also appear on the fruit.',
    host_plants: [apple, crabapple],
    spread_mechanism: 'Spores overwintering in fallen leaves are released in spring and carried by wind to new growth. Secondary infections occur throughout the growing season during wet weather.',
    conditions_favoring: [cool_moist_weather, extended_wet_periods, poor_air_circulation],
    prevention_methods: [
        resistant_varieties,
        proper_pruning_for_air_circulation,
        collect_and_destroy_fallen_leaves,
        proper_spacing
    ],
    control_methods: [
        copper_sprays_in_early_spring,
        sulfur_sprays,
        lime_sulfur_sprays,
        good_sanitation_practices
    ],
    region: [north_america, europe, temperate_regions]
]).

frame(specific_disease, [
    name: bacterial_spot,
    type: bacterial,
    scientific_name: 'Xanthomonas species',
    description: 'A bacterial disease causing spots on leaves and fruit of various plants.',
    symptoms: 'Depending on the plant they attack, these bacteria will produce round, angular, or elongated discolorations on leaves. The spots are tiny at first but may spread and join to cover whole leaves. The spots are usually brown and are sometimes surrounded with a yellow ring referred to as a halo. The damaged tissue often drops out of the leaves, leaving small holes. Severely infected leaves may fall early.',
    host_plants: [tomato, pepper, stone_fruits, ornamentals],
    spread_mechanism: 'Spreads by water splash, insects, equipment, and infected seeds. Bacteria can survive in plant debris and seeds.',
    conditions_favoring: [warm_temperatures, high_humidity, rainfall, overhead_irrigation],
    prevention_methods: [
        disease_free_seeds_and_plants,
        crop_rotation,
        good_sanitation,
        resistant_varieties,
        proper_spacing
    ],
    control_methods: [
        copper_sprays,
        remove_infected_plants,
        avoid_working_with_wet_plants,
        clean_garden_tools
    ],
    region: [north_america, global]
]).

frame(specific_disease, [
    name: black_spot,
    type: fungal,
    scientific_name: 'Diplocarpon rosae',
    description: 'A common fungal disease of roses causing black spots on leaves.',
    symptoms: 'This disease appears as circular black spots on infected leaves. The spots usually have fringed or indistinct margins and are often surrounded by a ring of yellow tissue. Severely infected leaves may fall early. Black spot fungus can also infect stems, causing purplish or black blisters on young canes.',
    host_plants: [rose],
    spread_mechanism: 'Spores are spread by water splash and can overwinter on fallen leaves and on canes.',
    conditions_favoring: [high_humidity, wet_foliage, poor_air_circulation, susceptible_varieties],
    prevention_methods: [
        resistant_varieties,
        proper_spacing,
        avoid_overhead_watering,
        collect_and_destroy_fallen_leaves,
        pruning_for_air_circulation
    ],
    control_methods: [
        remove_infected_leaves,
        sulfur_sprays,
        fungicidal_soap_sprays,
        baking_soda_sprays,
        proper_pruning
    ],
    region: [north_america, global]
]).

frame(specific_disease, [
    name: botrytis_blight,
    type: fungal,
    scientific_name: 'Botrytis cinerea',
    description: 'A common fungal disease causing gray mold on various plants.',
    symptoms: 'Infected leaves develop water-soaked spots that later turn brown or dry. The fungus can also damage flowers and fruit, causing them to rot and develop a fuzzy gray mold. This disease is particularly common on peonies where it can prevent flower buds from opening.',
    host_plants: [cabbage, onion, peony, strawberry, many_ornamentals, many_vegetables, many_fruits],
    spread_mechanism: 'Spores are spread by air currents and water splash. The fungus can overwinter in plant debris.',
    conditions_favoring: [cool_temperatures, high_humidity, wet_conditions, poor_air_circulation],
    prevention_methods: [
        proper_spacing,
        good_air_circulation,
        proper_watering_practices,
        sanitation,
        removal_of_plant_debris
    ],
    control_methods: [
        remove_infected_plant_parts,
        cut_back_herbaceous_plants_after_they_die_down,
        improve_air_circulation,
        copper_fungicides
    ],
    region: [north_america, global]
]).

frame(specific_disease, [
    name: cedar_apple_rust,
    type: fungal,
    scientific_name: 'Gymnosporangium juniperi-virginianae',
    description: 'A fungal disease requiring both cedar and apple trees to complete its life cycle.',
    symptoms: 'On apples, rust symptoms commonly appear in spring. Tiny yellow spots, which later expand and turn orange, form on upper leaf surfaces and on fruit. Brown spots may appear on the undersides of leaves. On cedar trees, the fungus produces brown galls that swell and produce orange gelatinous tendrils when wet.',
    host_plants: [apple, crabapple, cedar, juniper],
    spread_mechanism: 'The fungus requires both cedar/juniper and apple/crabapple to complete its life cycle. Spores are wind-borne between the two hosts.',
    conditions_favoring: [proximity_of_host_plants, wet_spring_weather, susceptible_varieties],
    prevention_methods: [
        resistant_varieties,
        separate_host_plants_by_at_least_4_miles,
        good_air_circulation,
        proper_pruning
    ],
    control_methods: [
        remove_cedar_galls,
        copper_based_fungicides,
        separate_host_plants,
        remove_one_host_if_possible
    ],
    region: [north_america, particularly_eastern_united_states]
]).

frame(specific_disease, [
    name: cherry_leaf_spot,
    type: fungal,
    scientific_name: 'Blumeriella jaapii',
    description: 'A fungal disease causing spots on cherry leaves that can lead to defoliation.',
    symptoms: 'The first noticeable symptoms are tiny purple spots on the upper leaf surfaces. Corresponding whitish spots on the undersides of leaves may appear. The centers of these spots often dry and fall out, giving the leaves a shothole appearance. Entire leaves may turn yellow and drop early. Fruit, as well as leaf and fruit stems, can also show symptoms.',
    host_plants: [cherry, plum],
    spread_mechanism: 'Spores are spread by water splash and wind. The fungus overwinters in fallen leaves.',
    conditions_favoring: [wet_weather, poor_air_circulation, susceptible_varieties],
    prevention_methods: [
        resistant_varieties,
        proper_pruning_for_air_circulation,
        collect_and_destroy_fallen_leaves,
        proper_spacing
    ],
    control_methods: [
        sulfur_sprays,
        good_sanitation_practices,
        copper_fungicides
    ],
    region: [north_america, europe]
]).

% More frames would be added for other diseases described in the source material

% ========================
% RELATIONSHIPS
% ========================

% Disease-pathogen relationships
causes_disease(fungus, powdery_mildew).
causes_disease(fungus, downy_mildew).
causes_disease(fungus, apple_scab).
causes_disease(fungus, anthracnose).
causes_disease(fungus, black_spot).
causes_disease(fungus, early_blight).
causes_disease(fungus, late_blight).
causes_disease(fungus, rust).
causes_disease(fungus, botrytis_blight).
causes_disease(fungus, cedar_apple_rust).
causes_disease(fungus, cherry_leaf_spot).
causes_disease(bacterium, bacterial_spot).
causes_disease(bacterium, fire_blight).
causes_disease(bacterium, bacterial_wilt).
causes_disease(bacterium, crown_gall).
causes_disease(virus, cucumber_mosaic).
causes_disease(virus, tobacco_mosaic).
causes_disease(virus, tomato_spotted_wilt).
causes_disease(nematode, root_knot).
causes_disease(parasitic_plant, dodder_infestation).
causes_disease(parasitic_plant, mistletoe_infestation).

% Environmental condition-disease relationships
favors_disease(high_humidity, powdery_mildew).
favors_disease(high_humidity, downy_mildew).
favors_disease(high_humidity, late_blight).
favors_disease(high_humidity, botrytis_blight).
favors_disease(wet_foliage, anthracnose).
favors_disease(wet_foliage, apple_scab).
favors_disease(wet_foliage, black_spot).
favors_disease(wet_foliage, early_blight).
favors_disease(wet_foliage, late_blight).
favors_disease(poor_air_circulation, powdery_mildew).
favors_disease(poor_air_circulation, downy_mildew).
favors_disease(poor_air_circulation, botrytis_blight).
favors_disease(warm_temperatures, bacterial_diseases).
favors_disease(insect_feeding, viral_diseases).
favors_disease(wet_soil, root_rot).
favors_disease(wet_soil, damping_off).

% Control method-disease relationships
controls(copper_spray, bacterial_spot).
controls(copper_spray, fire_blight).
controls(copper_spray, downy_mildew).
controls(copper_spray, early_blight).
controls(copper_spray, late_blight).
controls(sulfur, powdery_mildew).
controls(sulfur, black_spot).
controls(sulfur, apple_scab).
controls(lime_sulfur, apple_scab).
controls(lime_sulfur, peach_leaf_curl).
controls(baking_soda_spray, black_spot).
controls(baking_soda_spray, powdery_mildew).
controls(good_air_circulation, fungal_diseases).
controls(resistant_varieties, most_diseases).
controls(crop_rotation, soilborne_diseases).
controls(sanitation, most_diseases).
controls(proper_watering, water_related_diseases).
controls(remove_infected_parts, most_diseases).
controls(soil_solarization, soilborne_diseases).

% Plant-disease susceptibility relationships
susceptible_to(apple, apple_scab).
susceptible_to(apple, cedar_apple_rust).
susceptible_to(apple, fire_blight).
susceptible_to(rose, black_spot).
susceptible_to(rose, powdery_mildew).
susceptible_to(tomato, early_blight).
susceptible_to(tomato, late_blight).
susceptible_to(tomato, bacterial_spot).
susceptible_to(tomato, tobacco_mosaic).
susceptible_to(cherry, cherry_leaf_spot).
susceptible_to(peony, botrytis_blight).
susceptible_to(cucumber, downy_mildew).
susceptible_to(cucumber, powdery_mildew).
susceptible_to(cucumber, bacterial_wilt).
susceptible_to(cucumber, cucumber_mosaic).

% Helper predicates
common_diseases_of(Plant, DiseaseList) :- findall(Disease, susceptible_to(Plant, Disease), DiseaseList).
effective_controls_for(Disease, ControlList) :- findall(Control, controls(Control, Disease), ControlList).
favorable_conditions_for(Disease, ConditionList) :- findall(Condition, favors_disease(Condition, Disease), ConditionList).

% Add new specific diseases from the provided content
frame(specific_disease, [
    name: foliar_nematodes,
    type: nematode,
    scientific_name: 'Aphelenchoides species',
    description: 'Microscopic worms that infect leaf tissue causing distinctive discoloration and damage patterns.',
    symptoms: 'Leaves show yellow patches that later turn brown or black; these blotches may enlarge to cover whole leaves, causing early leaf drop. Symptoms start near the bottom of plants and work upward. Infected shoots are stunted, and flowers may be deformed.',
    host_plants: [chrysanthemum, aster, dahlia, phlox, primrose, strawberry, herbaceous_plants],
    spread_mechanism: 'Nematodes move up stems in a film of water and infect leaf tissue. They can overwinter in plant debris.',
    conditions_favoring: [high_humidity, poor_air_circulation, wet_foliage],
    prevention_methods: [
        avoid_planting_susceptible_species,
        ensure_good_air_circulation,
        thin_stems_for_quick_drying,
        clean_up_plant_debris,
        plant_in_well_drained_soil
    ],
    control_methods: [
        destroy_infected_plant_parts,
        remove_plant_debris,
        avoid_overhead_watering
    ],
    region: [north_america, global]
]).

frame(specific_disease, [
    name: iron_deficiency,
    type: physiological_disorder,
    scientific_name: 'None',
    description: 'A nutritional disorder where plants are unable to absorb enough iron, often due to high soil pH rather than actual iron deficiency in the soil.',
    symptoms: 'The youngest leaves, those near the tips of shoots, turn yellow except for the veins, which remain green (interveinal chlorosis).',
    host_plants: [azalea, rhododendron, gardenia, blueberry, oak, holly, acid_loving_plants],
    spread_mechanism: 'Not infectious. Occurs when soil pH is too high for acid-loving plants, or from concrete leaching lime into soil near buildings.',
    conditions_favoring: [high_soil_ph, alkaline_soil, proximity_to_concrete_foundations],
    prevention_methods: [
        plant_in_acidic_soil,
        add_sulfur_to_soil,
        add_peat_moss_to_soil,
        plant_in_raised_beds,
        mulch_with_evergreen_needles
    ],
    control_methods: [
        spray_with_chelated_iron,
        spray_with_seaweed_extract,
        acidify_soil_for_long_term_solution
    ],
    region: [global]
]).

frame(specific_disease, [
    name: leaf_scorch,
    type: physiological_disorder,
    scientific_name: 'None',
    description: 'Environmental condition causing leaf margin damage due to water stress or environmental factors.',
    symptoms: 'Yellowing and browning of leaves beginning along the margins and tips. Associated symptoms may include wilting, rolling of leaves, stunted growth, and death of the plant.',
    host_plants: [woody_plants, herbaceous_plants, maple, horse_chestnut],
    spread_mechanism: 'Not infectious. Caused by environmental stress, particularly drought or reflected heat.',
    conditions_favoring: [drought, heat_stress, reflected_heat_from_pavement, shallow_rooting],
    prevention_methods: [
        proper_watering,
        deep_irrigation,
        avoid_frequent_light_watering,
        mulching,
        avoid_planting_susceptible_plants_near_pavement
    ],
    control_methods: [
        increase_watering_during_drought,
        apply_mulch_to_conserve_soil_moisture
    ],
    region: [global]
]).

frame(specific_disease, [
    name: mosaic_virus,
    type: viral,
    scientific_name: 'Various mosaic viruses',
    description: 'A group of viral diseases causing distinctive mottled patterns on plant leaves and sometimes stunting growth.',
    symptoms: 'Mosaic-infected leaves are mottled with yellow, white, and light and dark green spots or streaks. Fruit may show similar symptoms. Plants are often stunted.',
    host_plants: [squash, cucumber, tomato, bean, ornamentals, woody_plants, herbaceous_plants],
    spread_mechanism: 'Primarily spread by insect vectors, especially aphids and leafhoppers. Can also be spread by handling infected plants then touching healthy ones.',
    conditions_favoring: [presence_of_insect_vectors, poor_sanitation, overcrowding],
    prevention_methods: [
        plant_resistant_cultivars,
        cover_plants_with_floating_row_cover,
        control_insect_vectors,
        wash_hands_after_handling_plants
    ],
    control_methods: [
        remove_and_destroy_infected_plants,
        control_aphids_and_leafhoppers
    ],
    region: [global]
]).

frame(specific_disease, [
    name: nitrogen_deficiency,
    type: physiological_disorder,
    scientific_name: 'None',
    description: 'A nutritional disorder where plants lack sufficient nitrogen for proper growth.',
    symptoms: 'Uniform yellowing of the oldest leaves (those nearest the base of the stem). Less-obvious symptom is stunted and spindly growth.',
    host_plants: [all_plants],
    spread_mechanism: 'Not infectious. Results from insufficient nitrogen in soil or inability of plants to access nitrogen.',
    conditions_favoring: [poor_soil, soil_lacking_organic_matter, heavy_rainfall_leaching_nutrients],
    prevention_methods: [
        apply_compost,
        apply_aged_manure,
        grow_leguminous_cover_crops,
        add_organic_nitrogen_sources
    ],
    control_methods: [
        apply_soybean_meal,
        apply_dried_blood,
        spray_leaves_with_fish_emulsion,
        add_composted_manure
    ],
    region: [global]
]).

frame(specific_disease, [
    name: ozone_damage,
    type: physiological_disorder,
    scientific_name: 'None',
    description: 'Plant damage caused by elevated ozone levels in the atmosphere, typically from air pollution.',
    symptoms: 'White or tan stippling or flecking on leaves. High concentrations of ozone in the atmosphere may cause early fall color and leaf drop.',
    host_plants: [bean, spinach, tomato, blackberry, sweet_gum, pine, tulip_poplar, nasturtium],
    spread_mechanism: 'Not infectious. Environmental pollution, particularly from automobile exhaust during hot, calm days.',
    conditions_favoring: [high_ozone_levels, hot_calm_days, urban_environments, high_traffic_areas],
    prevention_methods: [
        plant_resistant_species,
        grow_less_susceptible_plants
    ],
    control_methods: [
        no_direct_control_measures,
        plant_ozone_tolerant_species_like_beet_lettuce_strawberry
    ],
    region: [urban_areas, areas_with_air_pollution]
]).

frame(specific_disease, [
    name: pan_damage,
    type: physiological_disorder,
    scientific_name: 'None',
    description: 'Plant damage from peroxyacyl nitrate (PAN), an air pollutant found in smog.',
    symptoms: 'Silvery glaze on the lower surfaces of leaves, resembling damage due to frost, sunscald, mites, thrips, or leafhoppers. Young, rapidly growing tissue is most sensitive.',
    host_plants: [petunia, bean, lettuce, pepper, tomato, woody_plants, herbaceous_plants],
    spread_mechanism: 'Not infectious. Environmental pollution, component of engine exhaust and smog.',
    conditions_favoring: [urban_environments, smoggy_areas, high_traffic_areas],
    prevention_methods: [
        grow_tolerant_plants
    ],
    control_methods: [
        plant_resistant_species_like_sugar_maple_arborvitae_euonymus_ivy_snapdragon_cabbage_cucumber_squash
    ],
    region: [urban_areas, smoggy_regions]
]).

frame(specific_disease, [
    name: phosphorus_deficiency,
    type: physiological_disorder,
    scientific_name: 'None',
    description: 'A nutritional disorder where plants lack sufficient phosphorus for proper growth and development.',
    symptoms: 'A bluish or purplish cast to leaves or stems; some plants develop purple spots. Phosphorus-deficient plants also do not flower and fruit as well as healthy plants.',
    host_plants: [all_plants, corn],
    spread_mechanism: 'Not infectious. Results from insufficient phosphorus in soil or inability of plants to access phosphorus, often due to cold soil in early spring.',
    conditions_favoring: [cold_soil, early_spring_planting, soil_lacking_organic_matter],
    prevention_methods: [
        enrich_soil_with_compost,
        add_leaf_mold,
        add_organic_materials,
        add_bonemeal,
        add_rock_phosphate
    ],
    control_methods: [
        wait_for_soil_to_warm,
        increase_soil_organic_matter
    ],
    region: [global]
]).

frame(specific_disease, [
    name: potassium_deficiency,
    type: physiological_disorder,
    scientific_name: 'None',
    description: 'A nutritional disorder where plants lack sufficient potassium for proper growth and development.',
    symptoms: 'Symptoms usually appear on older leaves first as yellowing and browning of the leaf margins. Dead areas on edges may drop, giving the leaves a ragged appearance.',
    host_plants: [all_plants, tomato],
    spread_mechanism: 'Not infectious. Results from insufficient potassium in soil.',
    conditions_favoring: [sandy_soil, soil_lacking_organic_matter, heavy_leaching],
    prevention_methods: [
        regular_soil_testing,
        apply_compost,
        apply_organic_fertilizers,
        add_kelp_meal,
        add_granite_dust,
        add_greensand,
        add_wood_ashes_sparingly
    ],
    control_methods: [
        add_potassium_sources,
        increase_soil_organic_matter
    ],
    region: [global]
]).

frame(specific_disease, [
    name: sulfur_dioxide_injury,
    type: physiological_disorder,
    scientific_name: 'None',
    description: 'Plant damage from sulfur dioxide, an air pollutant primarily from industrial processes.',
    symptoms: 'Mild cases show general leaf yellowing. More severe damage involves yellowing or browning of the tissues between leaf veins.',
    host_plants: [woody_plants, herbaceous_plants, blackberry],
    spread_mechanism: 'Not infectious. Environmental pollution from industrial processes.',
    conditions_favoring: [proximity_to_industrial_areas, areas_with_high_sulfur_dioxide_levels],
    prevention_methods: [
        grow_tolerant_plants
    ],
    control_methods: [
        plant_tolerant_trees_like_ginkgo_juniper_sycamore_arborvitae,
        plant_tolerant_vegetables_like_cucumber_corn_onion
    ],
    region: [industrial_areas, urban_areas]
]).

frame(specific_disease, [
    name: verticillium_wilt,
    type: fungal,
    scientific_name: 'Verticillium species',
    description: 'A fungal disease that infects plant vascular systems, causing wilting and eventual plant death.',
    symptoms: 'Infection causes leaves to yellow and leaf stems to droop, giving plants a wilted appearance. The yellow leaf patches turn brown and may spread to cover whole leaves. Leaves often fall early, and plants will die. Symptoms usually first appear on the lower or outer parts of plants. The interior of the stem near the base may be discolored.',
    host_plants: [tomato, pepper, melon, aster, chrysanthemum, peach, cherry, strawberry, maple, woody_plants, herbaceous_plants],
    spread_mechanism: 'Soilborne fungus that enters through roots and colonizes vascular tissue. Can survive in soil for many years.',
    conditions_favoring: [cool_weather, temperate_areas, previously_infected_soil],
    prevention_methods: [
        plant_resistant_cultivars,
        soil_solarization,
        avoid_planting_susceptible_species_in_infected_soil
    ],
    control_methods: [
        remove_and_destroy_infected_plants,
        soil_solarization_may_help
    ],
    region: [temperate_regions, global]
]).

frame(specific_disease, [
    name: winter_injury,
    type: physiological_disorder,
    scientific_name: 'None',
    description: 'Damage to plants from cold temperatures, winter desiccation, or temperature fluctuations.',
    symptoms: 'Symptoms of cold injury can be similar to sunscald symptoms: blotchy, water-soaked areas on leaves. Shoot tips often die back. Evergreens may show bronzing or browning of needles.',
    host_plants: [cherry_laurel, evergreens, woody_plants, herbaceous_plants, corn, beans],
    spread_mechanism: 'Not infectious. Environmental stress caused by cold temperatures, drying winter winds, or frozen soil limiting water uptake.',
    conditions_favoring: [cold_temperatures, winter_winds, frozen_soil, lack_of_snow_cover],
    prevention_methods: [
        water_plants_thoroughly_in_late_fall,
        apply_antitranspirant_spray,
        move_plants_to_sheltered_location,
        erect_wind_barriers,
        mulch_base_of_plants,
        acclimate_seedlings_gradually,
        protect_garden_seedlings_with_cloches_or_row_covers
    ],
    control_methods: [
        prune_out_damaged_wood_in_spring,
        wait_for_warmer_weather_to_plant_heat_loving_crops
    ],
    region: [cold_winter_regions]
]).

frame(specific_disease, [
    name: yellows,
    type: phytoplasma,
    scientific_name: 'Phytoplasma species',
    description: 'Disease caused by mycoplasma-like organisms that infect plant phloem tissue.',
    symptoms: 'Gradual yellowing of leaves. Plants often appear dwarfed. Plant parts, including roots and flowers, may be deformed. On trees, leaves turn yellow, then brown, and may drop early. Symptoms appear over the whole crown of the tree. Plants may die in a single growing season.',
    host_plants: [carrot, lettuce, tomato, china_aster, gladiolus, elm, marigold],
    spread_mechanism: 'Transmitted primarily by leafhoppers. Can overwinter in weeds and perennial plants.',
    conditions_favoring: [presence_of_leafhopper_vectors, weedy_areas, presence_of_overwintering_sites],
    prevention_methods: [
        control_leafhoppers,
        remove_weed_hosts_like_thistle_queen_annes_lace_dandelion_wild_chicory
    ],
    control_methods: [
        remove_and_destroy_infected_plants,
        control_leafhopper_vectors
    ],
    region: [global]
]).

frame(specific_disease, [
    name: powdery_mildew,
    type: fungal,
    scientific_name: 'Various species',
    description: 'A common fungal disease appearing as a white powdery coating on plant surfaces.',
    symptoms: 'Plants suffering from powdery mildew look as if they have been dusted with flour. Powdery mildew fungi mostly attacks new leaves, causing distorted growth. It can also attack fruit; fruit may color slowly or not at all and may show russeting of the skin.',
    host_plants: [lilac, phlox, bee_balm, squash, rose, zinnia, pumpkin, apple, grape],
    spread_mechanism: 'Fungal spores are spread by air currents. Unlike most fungi, powdery mildew does not require free water to germinate and infect.',
    conditions_favoring: [hot_weather, cool_nights, moderate_humidity, poor_air_circulation],
    prevention_methods: [
        plant_resistant_cultivars,
        ensure_good_air_circulation,
        proper_spacing
    ],
    control_methods: [
        spray_with_sulfur,
        spray_with_lime_sulfur,
        spray_with_baking_soda_solution,
        remove_infected_plant_parts
    ],
    region: [global]
]).

frame(specific_disease, [
    name: salt_injury,
    type: physiological_disorder,
    scientific_name: 'None',
    description: 'Plant damage from excess salt in soil or on plant surfaces.',
    symptoms: 'Plants respond to excess soil salt just as they would to drought: stunting, wilting, drying out of leaves, even death. White, crusty material may build up on leaves or soil surface.',
    host_plants: [ivy, woody_plants, herbaceous_plants],
    spread_mechanism: 'Not infectious. Caused by road de-icing salts, sea spray, naturally saline soils, or excess fertilizer application.',
    conditions_favoring: [coastal_areas, roadside_plantings, poor_drainage, over_fertilization],
    prevention_methods: [
        improve_soil_drainage,
        use_sand_or_sawdust_instead_of_salt_for_deicing,
        choose_salt_tolerant_plants,
        leach_salts_with_heavy_watering,
        apply_gypsum_to_sodium_affected_soils
    ],
    control_methods: [
        flush_soil_with_water_to_leach_salts,
        improve_drainage
    ],
    region: [coastal_areas, northern_regions_using_road_salt, arid_regions]
]).

frame(specific_disease, [
    name: sooty_mold,
    type: fungal,
    scientific_name: 'Various species',
    description: 'Fungi that grow on the honeydew secretions produced by sap-feeding insects.',
    symptoms: 'Leaves and stems are speckled or coated with a thin black film, which can be wiped off to expose healthy green leaf surfaces. Plants may also feel sticky.',
    host_plants: [woody_plants, herbaceous_plants],
    spread_mechanism: 'Not directly infectious to plants. Grows on honeydew produced by aphids, scales, mealybugs, and other sap-feeding insects.',
    conditions_favoring: [presence_of_sap_feeding_insects, honeydew_secretions],
    prevention_methods: [
        control_insects_producing_honeydew,
        inspect_plants_regularly
    ],
    control_methods: [
        wipe_coating_off_with_damp_cloth,
        control_aphids_scales_or_mealybugs,
        check_for_insect_problems_on_overhanging_plants
    ],
    region: [global]
]).

frame(specific_disease, [
    name: curly_top_virus,
    type: viral,
    scientific_name: 'Beet curly top virus',
    description: 'A viral disease causing leaf curling and plant stunting.',
    symptoms: 'Leaves of infected plants twist and curl upward, becoming stiff and leathery. They eventually turn yellow and then brown. Leaf stems bend downward. The plant may appear stunted, and fruit production stops.',
    host_plants: [beet, tomato, bean, melon, spinach, herbaceous_plants],
    spread_mechanism: 'Transmitted by beet leafhoppers. Can overwinter in weed hosts.',
    conditions_favoring: [presence_of_leafhopper_vectors, weedy_areas],
    prevention_methods: [
        plant_resistant_cultivars,
        remove_surrounding_weeds_like_thistle_and_plantain,
        protect_plants_with_floating_row_cover,
        control_leafhoppers
    ],
    control_methods: [
        remove_and_destroy_affected_plants
    ],
    region: [western_north_america]
]).

frame(specific_disease, [
    name: leaf_gall,
    type: fungal,
    scientific_name: 'Exobasidium species',
    description: 'A fungal disease causing distinctive swellings on leaves.',
    symptoms: 'Reddish or yellowish leaf spots often appear first. Infected leaves develop light green galls that later turn white and then brown. Flowers may also be damaged.',
    host_plants: [azalea, rhododendron, camellia],
    spread_mechanism: 'Fungal spores spread by wind and water splash.',
    conditions_favoring: [high_humidity, poor_air_circulation],
    prevention_methods: [
        improve_air_circulation,
        avoid_overhead_watering
    ],
    control_methods: [
        pick_off_and_destroy_infected_leaves
    ],
    region: [regions_where_azaleas_and_rhododendrons_grow]
]).

frame(specific_disease, [
    name: peach_leaf_curl,
    type: fungal,
    scientific_name: 'Taphrina deformans',
    description: 'A fungal disease causing distorted, curled leaves on peach trees.',
    symptoms: 'Infected plants develop yellowish or reddish blisters on leaves, which become curled and distorted. The blisters eventually turn powdery gray. Entire leaves may turn yellow and fall early. Fruit can be deformed and may drop early. New growth can be stunted; infected shoot tips may die back.',
    host_plants: [peach, nectarine],
    spread_mechanism: 'Fungal spores overwinter on bud scales and bark, infecting new growth in spring. Spread by rain splash and wind.',
    conditions_favoring: [cool_wet_spring_weather],
    prevention_methods: [
        plant_resistant_cultivars,
        apply_dormant_spray
    ],
    control_methods: [
        remove_and_destroy_infected_leaves,
        apply_dormant_spray_of_lime_sulfur_or_bordeaux_mix
    ],
    region: [temperate_fruit_growing_regions]
]).

frame(specific_disease, [
    name: bacterial_wilt,
    type: bacterial,
    scientific_name: 'Erwinia tracheiphila',
    description: 'A bacterial disease causing sudden wilting and collapse of plants.',
    symptoms: 'Leaves appear limp and wilted. Infected stems wilt and collapse quickly. All affected parts are soft at first, but turn hard and dry. When you pull apart a cut stem, you may see long, sticky strands of whitish bacterial ooze. Spots may occur on fruit.',
    host_plants: [cucumber, melon, squash, tomato, bean],
    spread_mechanism: 'Transmitted primarily by cucumber beetles and grasshoppers as they feed.',
    conditions_favoring: [presence_of_insect_vectors, warm_weather],
    prevention_methods: [
        plant_resistant_cultivars,
        use_disease_free_seed,
        control_cucumber_beetles_and_grasshoppers,
        protect_plants_with_floating_row_cover
    ],
    control_methods: [
        remove_and_destroy_infected_plants
    ],
    region: [north_america, global]
]).

frame(specific_disease, [
    name: fusarium_wilt,
    type: fungal,
    scientific_name: 'Fusarium species',
    description: 'A fungal disease that clogs plant vascular systems causing wilting and death.',
    symptoms: 'Wilt fungi cause leaves to yellow and leaf stems to droop, giving plants a wilted appearance. The yellow leaf patches turn brown and may spread to cover whole leaves. Leaves often fall early, and the plants will die. Symptoms usually first appear on the lower or outer parts of plants. In some cases, the symptoms are most apparent on only one side of a plant. If you cut the stem near the base, you may notice a brown discoloration in the interior.',
    host_plants: [tomato, pea, pepper, melon, dahlia, mimosa, woody_plants, herbaceous_plants],
    spread_mechanism: 'Soilborne fungus that enters through roots and colonizes vascular tissue. Can survive in soil for years.',
    conditions_favoring: [warm_weather, warm_soil],
    prevention_methods: [
        plant_resistant_cultivars,
        crop_rotation
    ],
    control_methods: [
        remove_and_destroy_infected_plants,
        soil_solarization
    ],
    region: [warmer_regions, global]
]).

frame(specific_disease, [
    name: waterlogging,
    type: physiological_disorder,
    scientific_name: 'None',
    description: 'Plant stress caused by excess water in soil depriving roots of oxygen.',
    symptoms: 'Because waterlogging inhibits root function, it causes essentially the same symptoms as droughty conditions do—wilting. Other common symptoms include yellowed leaves and sudden leaf drop.',
    host_plants: [yew, woody_plants, herbaceous_plants],
    spread_mechanism: 'Not infectious. Caused by excess water application or poor soil drainage.',
    conditions_favoring: [heavy_soil, poor_drainage, overwatering, compacted_soil],
    prevention_methods: [
        improve_soil_drainage,
        add_organic_matter,
        create_raised_beds,
        water_according_to_plant_needs
    ],
    control_methods: [
        improve_drainage,
        reduce_watering
    ],
    region: [global]
]).

frame(specific_disease, [
    name: botrytis_blight,
    type: fungal,
    scientific_name: 'Botrytis cinerea',
    description: 'A common fungal disease causing gray mold on flowers, fruits, and other plant parts.',
    symptoms: 'Botrytis blight generally begins on flowers, producing a white, gray, or tan, fluffy growth. The fungus then spreads to the flower stalk, weakening the stalk and causing the flowers to droop. Affected plant parts eventually turn brown and dry.',
    host_plants: [rose, begonia, peony, chrysanthemum, dahlia, geranium],
    spread_mechanism: 'Fungal spores are spread by wind and water splash. The fungus can overwinter in plant debris.',
    conditions_favoring: [cool_temperatures, high_humidity, poor_air_circulation],
    prevention_methods: [
        provide_good_air_circulation,
        proper_site_selection,
        avoid_overhead_watering
    ],
    control_methods: [
        remove_and_destroy_affected_parts
    ],
    region: [global]
]).

frame(specific_disease, [
    name: brown_rot,
    type: fungal,
    scientific_name: 'Monilinia species',
    description: 'A fungal disease affecting stone fruits, causing blossom blight and fruit rot.',
    symptoms: 'Infected flowers appear wilted and browned. Eventually they are covered with light brown spore masses, which then attack developing fruit. Small cankers appear near branch tips. On fruit, small brown spots often enlarge to cover the surface with masses of grayish brown spores. The fruit eventually rots and shrivels up (forming a mummy).',
    host_plants: [peach, cherry, plum, stone_fruits],
    spread_mechanism: 'Fungal spores are spread by wind and rain. The fungus can overwinter in mummified fruit and infected twigs.',
    conditions_favoring: [warm_wet_weather, poor_air_circulation],
    prevention_methods: [
        plant_resistant_cultivars,
        prune_for_good_air_circulation,
        pick_off_and_clean_up_rotted_fruit
    ],
    control_methods: [
        prune_out_damaged_shoots,
        spray_with_sulfur_before_blossoms_open_and_after_blossoming,
        spray_again_before_harvest
    ],
    region: [temperate_fruit_growing_regions]
]).

frame(specific_disease, [
    name: flower_blight_of_camellia,
    type: fungal,
    scientific_name: 'Ciborinia camelliae',
    description: 'A fungal disease specifically affecting camellia flowers.',
    symptoms: 'Flower blight fungi produce small brown spots on petals. These spots enlarge and run together, turning whole flowers brown.',
    host_plants: [camellia],
    spread_mechanism: 'Fungal spores spread by wind and water. Can be introduced on infected plants.',
    conditions_favoring: [high_humidity, poor_air_circulation],
    prevention_methods: [
        purchase_bare_root_plants,
        pick_off_flower_buds_before_planting,
        maintain_good_air_circulation
    ],
    control_methods: [
        remove_and_destroy_all_infected_flowers_and_buds,
        replace_existing_mulch,
        spray_bordeaux_mix_in_spring
    ],
    region: [regions_where_camellias_grow]
]).

% Additional relationships based on new disease entries
susceptible_to(chrysanthemum, foliar_nematodes).
susceptible_to(strawberry, foliar_nematodes).
susceptible_to(azalea, iron_deficiency).
susceptible_to(rhododendron, iron_deficiency).
susceptible_to(maple, leaf_scorch).
susceptible_to(squash, mosaic_virus).
susceptible_to(tomato, mosaic_virus).
susceptible_to(bean, nitrogen_deficiency).
susceptible_to(tomato, nitrogen_deficiency).
susceptible_to(nasturtium, ozone_damage).
susceptible_to(tomato, ozone_damage).
susceptible_to(lettuce, pan_damage).
susceptible_to(corn, phosphorus_deficiency).
susceptible_to(tomato, potassium_deficiency).
susceptible_to(blackberry, sulfur_dioxide_injury).
susceptible_to(tomato, verticillium_wilt).
susceptible_to(strawberry, verticillium_wilt).
susceptible_to(maple, verticillium_wilt).
susceptible_to(cherry_laurel, winter_injury).
susceptible_to(marigold, yellows).
susceptible_to(pumpkin, powdery_mildew).
susceptible_to(zinnia, powdery_mildew).
susceptible_to(ivy, salt_injury).
susceptible_to(azalea, leaf_gall).
susceptible_to(peach, peach_leaf_curl).
susceptible_to(cucumber, bacterial_wilt).
susceptible_to(tomato, fusarium_wilt).
susceptible_to(yew, waterlogging).
susceptible_to(rose, botrytis_blight).
susceptible_to(peony, botrytis_blight).
susceptible_to(cherry, brown_rot).
susceptible_to(plum, brown_rot).
susceptible_to(camellia, flower_blight_of_camellia).

% Control method-disease relationships
controls(good_air_circulation, foliar_nematodes).
controls(soil_acidification, iron_deficiency).
controls(chelated_iron, iron_deficiency).
controls(proper_watering, leaf_scorch).
controls(resistant_varieties, mosaic_virus).
controls(fish_emulsion, nitrogen_deficiency).
controls(compost, nitrogen_deficiency).
controls(resistant_species, ozone_damage).
controls(resistant_species, pan_damage).
controls(organic_matter, phosphorus_deficiency).
controls(bonemeal, phosphorus_deficiency).
controls(compost, potassium_deficiency).
controls(kelp_meal, potassium_deficiency).
controls(resistant_species, sulfur_dioxide_injury).
controls(resistant_cultivars, verticillium_wilt).
controls(soil_solarization, verticillium_wilt).
controls(winter_protection, winter_injury).
controls(leafhopper_control, yellows).
controls(sulfur, powdery_mildew).
controls(baking_soda_spray, powdery_mildew).
controls(soil_leaching, salt_injury).
controls(insect_control, sooty_mold).
controls(leafhopper_control, curly_top_virus).
controls(remove_infected_leaves, leaf_gall).
controls(dormant_spray, peach_leaf_curl).
controls(insect_vector_control, bacterial_wilt).
controls(resistant_cultivars, fusarium_wilt).
controls(soil_drainage, waterlogging).
controls(good_air_circulation, botrytis_blight).
controls(sulfur_spray, brown_rot).
controls(sanitation, flower_blight_of_camellia).

% Environmental condition-disease relationships
favors_disease(poor_air_circulation, foliar_nematodes).
favors_disease(high_soil_ph, iron_deficiency).
favors_disease(drought, leaf_scorch).
favors_disease(presence_of_insect_vectors, mosaic_virus).
favors_disease(soil_lacking_organic_matter, nitrogen_deficiency).
favors_disease(air_pollution, ozone_damage).
favors_disease(smoggy_areas, pan_damage).
favors_disease(cold_soil, phosphorus_deficiency).
favors_disease(sandy_soil, potassium_deficiency).
favors_disease(industrial_areas, sulfur_dioxide_injury).
favors_disease(cool_weather, verticillium_wilt).
favors_disease(frozen_soil, winter_injury).
favors_disease(presence_of_leafhopper_vectors, yellows).
favors_disease(hot_weather_cool_nights, powdery_mildew).
favors_disease(poor_drainage, salt_injury).
favors_disease(presence_of_sap_feeding_insects, sooty_mold).
favors_disease(presence_of_leafhopper_vectors, curly_top_virus).
favors_disease(high_humidity, leaf_gall).
favors_disease(cool_wet_spring, peach_leaf_curl).
favors_disease(presence_of_cucumber_beetles, bacterial_wilt).
favors_disease(warm_weather, fusarium_wilt).
favors_disease(overwatering, waterlogging).
favors_disease(high_humidity, botrytis_blight).
favors_disease(warm_wet_weather, brown_rot).
favors_disease(high_humidity, flower_blight_of_camellia).

% Additional helper predicates
disease_symptoms(Disease, SymptomList) :- 
    frame(specific_disease, [name:Disease, symptoms:Symptoms, _]), 
    atom_string(Symptoms, SymptomsStr),
    atomic_list_concat(SymptomList, ', ', SymptomsStr).

disease_control_methods(Disease, ControlList) :- 
    frame(specific_disease, [name:Disease, control_methods:ControlList, _]).

disease_prevention_methods(Disease, PreventionList) :- 
    frame(specific_disease, [name:Disease, prevention_methods:PreventionList, _]). 
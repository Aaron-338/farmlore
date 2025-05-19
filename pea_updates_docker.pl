% Additional Pea Entries from handbook

frame(pest, [
    name: pea_aphid,
    type: insect,
    scientific_name: '',
    symptoms: [thickened_and_curled_leaves, sticky_material_on_leaves, feeds_on_new_growth],
    monitoring: [check_new_growth_for_aphid_clusters],
    action_threshold: '',
    controls: [knock_aphids_off_plants_with_strong_water_spray, insecticidal_soap_general, neem_or_pyrethrin_spray_for_severe_infestations, reflective_mulch_for_aphid_control],
    cultural_context: [common_pest_of_peas_and_other_legumes, light_to_dark_green_soft_bodied_insects]
]).

frame(pest, [
    name: potato_leafhopper_on_pea,
    type: insect,
    scientific_name: '',
    symptoms: [curled_leaf_margins_on_pea, flowers_or_pods_drop, yellowing_growth],
    monitoring: [visual_inspection_for_green_or_brown_spindle_shaped_insects, yellow_sticky_traps],
    action_threshold: '',
    controls: [insecticidal_soap_general, neem_or_pyrethrin_spray_for_severe_infestations, row_cover_for_seedlings],
    cultural_context: [green_or_brown_spindle_shaped_insects_one_sixteenth_to_quarter_inch_long]
]).

frame(pest, [
    name: seedcorn_maggot_on_pea, 
    type: insect,
    scientific_name: '',
    symptoms: [poor_seed_germination, deformed_and_spindly_seedlings],
    monitoring: [check_for_maggots_in_ungerminated_seeds],
    action_threshold: 'preventative_management_recommended',
    controls: [apply_parasitic_nematodes_before_planting, plant_in_warm_soil, cover_soil_with_clear_plastic_before_planting_for_seedcorn_maggot],
    description: 'Quarter-inch long, yellow-white, spindle-shaped seed-eaters. Adults are small flies.',
    cultural_context: [thrives_in_cool_wet_soil]
]).

frame(disease, [
    name: pea_blight,
    type: fungal_and_bacterial_disease,
    scientific_name: 'Various fungi and bacteria',
    symptoms: [light_brown_to_purple_spots_on_leaves, spots_on_stems_and_pods, yellowed_leaves, plant_death],
    monitoring: [visual_inspection_of_leaves_stems_and_pods],
    action_threshold: '',
    controls: [spray_copper_in_wet_weather, remove_severely_infected_plants, presoak_seed_in_compost_tea, avoid_touching_wet_plants],
    cultural_context: [various_fungi_and_bacteria_can_cause_these_disease_symptoms]
]).

% Additional Pea Practices

frame(practice, [
    name: soak_pea_seed_in_compost_tea,
    type: cultural_control,
    controls: [],
    resolves: [root_rots_on_pea, damping_off_general, pea_blight],
    description: 'Soak pea seed in compost tea for 15 minutes or as long as overnight to help prevent disease and speed germination.',
    cost: low,
    difficulty: low,
    season: [pre_planting],
    cultural_context: [preventative_disease_management]
]).

frame(practice, [
    name: inoculate_pea_seed_with_rhizobium,
    type: cultural_control,
    controls: [],
    resolves: [nitrogen_deficiency],
    description: 'Treat pea seed with an inoculant labeled for garden peas before planting to promote nitrogen fixation. Use fresh inoculant each year.',
    cost: low,
    difficulty: low,
    season: [planting_time],
    cultural_context: [promotes_nitrogen_fixation]
]).

frame(practice, [
    name: spray_seaweed_extract_for_micronutrient_deficiencies_on_pea,
    type: fertility_management,
    controls: [],
    resolves: [micronutrient_deficiencies_in_pea, manganese_deficiency_in_pea],
    description: 'Spray young pea plants with seaweed extract every 2 weeks to prevent micronutrient deficiencies and boost production. Prevents manganese deficiency that causes brown spots or cavities in seeds.',
    cost: low,
    difficulty: low,
    season: [growing_season],
    cultural_context: [peas_susceptible_to_certain_micronutrient_deficiencies]
]).

frame(practice, [
    name: plant_pea_cultivars_resistant_to_both_downy_and_powdery_mildew,
    type: cultural_control,
    controls: [],
    resolves: [powdery_mildew_general, downy_mildew_on_pea],
    description: 'Plant pea cultivars like Knight that are resistant to both downy and powdery mildew to prevent these common fungal diseases.',
    cost: low,
    difficulty: low,
    season: [planting_time],
    cultural_context: [preventative_disease_management]
]).

frame(practice, [
    name: spray_copper_for_pea_blight,
    type: organic_pesticide,
    controls: [],
    resolves: [pea_blight],
    description: 'Spray pea plants with copper if weather is wet and blight symptoms appear on leaves and pods.',
    cost: medium,
    difficulty: low,
    season: [growing_season],
    cultural_context: [chemical_control_for_bacterial_and_fungal_diseases]
]).

frame(practice, [
    name: reflective_mulch_for_aphid_control,
    type: physical_control,
    controls: [pea_aphid, aphid_general],
    resolves: [],
    description: 'Use reflective mulch around pea plants to repel aphids, or plant cultivars with silvery leaves.',
    cost: medium,
    difficulty: low,
    season: [growing_season],
    cultural_context: [physical_deterrent_for_aphids]
]).

frame(practice, [
    name: plant_bolero_or_sprite_for_root_rot_tolerance,
    type: cultural_control,
    controls: [],
    resolves: [root_rots_on_pea],
    description: 'Plant pea cultivars such as Bolero and Sprite that are somewhat tolerant to pea root rot.',
    cost: low,
    difficulty: low,
    season: [planting_time],
    cultural_context: [preventative_disease_management]
]).

% Define micronutrient deficiencies

frame(disease, [
    name: micronutrient_deficiencies_in_pea,
    type: physiological_disorder,
    scientific_name: '',
    symptoms: [various_symptoms_depending_on_specific_deficiency],
    monitoring: [visual_inspection_of_plants],
    action_threshold: '',
    controls: [spray_seaweed_extract_for_micronutrient_deficiencies_on_pea],
    cultural_context: [peas_susceptible_to_certain_micronutrient_deficiencies]
]).

frame(disease, [
    name: manganese_deficiency_in_pea,
    type: physiological_disorder,
    scientific_name: '',
    symptoms: [brown_spots_or_cavities_in_pea_seeds],
    monitoring: [inspect_seeds_for_spots_or_cavities],
    action_threshold: '',
    controls: [spray_seaweed_extract_for_micronutrient_deficiencies_on_pea],
    cultural_context: [deficiency_primarily_affects_seed_quality]
]).

frame(disease, [
    name: copper_deficiency_in_pea,
    type: physiological_disorder,
    scientific_name: '',
    symptoms: [blossoms_drop_no_pods_form],
    monitoring: [observe_blossom_retention],
    action_threshold: '',
    controls: [spray_seaweed_extract_for_micronutrient_deficiencies_on_pea],
    cultural_context: [affects_reproductive_development]
]).

frame(disease, [
    name: molybdenum_deficiency_in_pea,
    type: physiological_disorder,
    scientific_name: '',
    symptoms: [blossoms_drop_no_pods_form],
    monitoring: [observe_blossom_retention],
    action_threshold: '',
    controls: [spray_seaweed_extract_for_micronutrient_deficiencies_on_pea],
    cultural_context: [affects_reproductive_development]
]).

% Add a general caterpillar entry for peas
frame(pest, [
    name: caterpillar_general,
    type: insect,
    scientific_name: 'Various species',
    symptoms: [holes_in_leaves, holes_in_pods, defoliation],
    monitoring: [visual_inspection_for_caterpillars_and_damage],
    action_threshold: '',
    controls: [handpicking, btk_spray_for_caterpillars, row_cover_to_prevent_egg_laying],
    cultural_context: [many_different_species_attack_vegetables]
]). 
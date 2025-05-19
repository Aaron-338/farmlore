% Crop Updates for Knowledgebase
% Contains frames for Pea and Pepper crops with their pest entries

% =========================
% PEPPER CROP
% =========================
frame(crop, [
    name: pepper,
    pests: [pepper_weevil, pepper_maggot, aphid_general, leafhopper_general, flea_beetle_general, thrips_general],
    diseases: [bacterial_spot_on_pepper, cercospora_leaf_spot_on_pepper, blossom_end_rot, fusarium_wilt_on_pepper, verticillium_wilt],
    resistant_cultivars: [
        cv('Bell Boy', [resistance_to: bacterial_spot_on_pepper]),
        cv('Lady Bell', [resistance_to: bacterial_spot_on_pepper]),
        cv('Valley Giant', [resistance_to: tobacco_mosaic_virus])
    ],
    cultural_context: [
        tender_perennial_grown_as_annual,
        requires_deeply_worked_well_drained_soil,
        prefers_ph_6_to_6_5_but_tolerates_as_low_as_5_5,
        requires_fertile_soil,
        grows_best_with_soil_temperatures_65_to_95_f,
        tolerates_drought_but_benefits_from_consistent_moisture,
        stake_plants_to_keep_fruit_off_soil,
        avoid_planting_where_solanaceous_crops_grown_recently
    ]
]).

% Pepper Pests
frame(pest, [
    name: pepper_weevil,
    type: insect,
    scientific_name: 'Anthonomus eugenii',
    symptoms: [yellow_calyx_on_fruit, black_specks_on_calyx, premature_fruit_drop, holes_in_fruit],
    monitoring: [check_flowers_for_weevils, examine_fallen_fruit],
    action_threshold: 'preventative_management_recommended',
    controls: [remove_fallen_fruit, use_straw_mulch, plant_trap_crops_like_eggplant_and_destroy_when_infested],
    cultural_context: [small_beetle_one_eighth_inch_long, severes_fruit_connection_to_plant]
]).

frame(pest, [
    name: pepper_maggot,
    type: insect,
    scientific_name: '',
    symptoms: [fruit_dimples_or_depressions, soft_spots_on_fruit, discolored_areas_on_fruit],
    monitoring: [check_fruit_for_dimples_and_soft_spots],
    action_threshold: 'preventative_management_recommended',
    controls: [remove_fallen_fruit, use_trap_crops, cover_young_plants_with_row_covers],
    cultural_context: [white_larvae_with_pale_heads, feeds_inside_fruit_causing_damage]
]).

% Pepper Diseases
frame(disease, [
    name: bacterial_spot_on_pepper,
    type: bacterial_disease,
    scientific_name: 'Xanthomonas campestris pv. vesicatoria',
    symptoms: [small_circular_water_soaked_spots_on_leaves, spots_enlarge_turn_brown_with_yellow_halos, leaves_drop, small_raised_blister_like_spots_on_fruit],
    monitoring: [inspect_leaves_and_fruit_regularly],
    action_threshold: '',
    controls: [use_disease_free_seed, spray_copper_at_first_sign, remove_infected_plants, avoid_overhead_watering, plant_resistant_cultivars_bell_boy_lady_bell],
    cultural_context: [common_in_warm_wet_conditions, seed_borne_disease]
]).

frame(disease, [
    name: cercospora_leaf_spot_on_pepper,
    type: fungal_disease,
    scientific_name: 'Cercospora capsici',
    symptoms: [circular_spots_on_leaves_white_or_tan_centers_with_dark_borders, spots_may_merge_as_disease_progresses, leaves_may_yellow_and_drop],
    monitoring: [examine_leaves_regularly_for_spots],
    action_threshold: '',
    controls: [remove_infected_plant_debris, improve_air_circulation, avoid_overhead_watering, spray_copper_fungicide],
    cultural_context: [favored_by_warm_humid_conditions]
]).

frame(disease, [
    name: blossom_end_rot,
    type: physiological_disorder,
    scientific_name: '',
    symptoms: [dark_sunken_area_at_blossom_end_of_fruit, affected_area_leathery_texture],
    monitoring: [inspect_developing_fruit],
    action_threshold: '',
    controls: [maintain_consistent_soil_moisture, add_calcium_to_soil_if_deficient, apply_mulch_to_conserve_moisture],
    cultural_context: [caused_by_calcium_deficiency_often_triggered_by_irregular_watering]
]).

% =========================
% PEA CROP
% =========================
frame(crop, [
    name: pea,
    pests: [pea_aphid, potato_leafhopper_on_pea, seedcorn_maggot_on_pea, caterpillar_general],
    diseases: [pea_blight, root_rots_on_pea, downy_mildew_on_pea, powdery_mildew_general, micronutrient_deficiencies_in_pea, manganese_deficiency_in_pea, copper_deficiency_in_pea, molybdenum_deficiency_in_pea],
    resistant_cultivars: [
        cv('Knight', [resistance_to: downy_mildew_on_pea, resistance_to: powdery_mildew_general]),
        cv('Bolero', [resistance_to: root_rots_on_pea]),
        cv('Sprite', [resistance_to: root_rots_on_pea])
    ],
    cultural_context: [
        cool_season_annual,
        prefers_well_drained_soil,
        sensitive_to_root_rots_in_wet_soil,
        benefits_from_rhizobium_inoculant,
        susceptible_to_micronutrient_deficiencies,
        prefers_moderate_fertility_excessive_nitrogen_reduces_production,
        avoid_planting_in_hot_weather,
        drought_reduces_production_and_quality
    ]
]).

% Existing Pea pest and disease frames are already in pea_updates.pl 

% =========================
% POTATO CROP
% =========================
frame(crop, [
    name: potato,
    pests: [colorado_potato_beetle, flea_beetle_general, blister_beetle_general, potato_aphid, leafhopper_general, wireworm, tuberworm, white_grub_general, root_knot_nematode_general],
    diseases: [late_blight_on_potato, early_blight_on_potato, bacterial_ring_rot, verticillium_wilt, black_leg, potato_scab, potato_scurf, potato_leafroll_virus, hollow_heart],
    resistant_cultivars: [
        cv('Katahdin', [resistance_to: potato_leafroll_virus, resistance_to: late_blight_on_potato, resistance_to: black_leg]),
        cv('Yukon Gold', [resistance_to: potato_leafroll_virus]),
        cv('Atlantic', [resistance_to: black_leg]),
        cv('Kennebec', [resistance_to: black_leg, resistance_to: early_blight_on_potato, resistance_to: late_blight_on_potato]),
        cv('Red Pontiac', [resistance_to: black_leg]),
        cv('Beltsville', [resistance_to: verticillium_wilt, resistance_to: potato_scab]),
        cv('Rhinered', [resistance_to: verticillium_wilt, resistance_to: potato_scab]),
        cv('Butte', [resistance_to: early_blight_on_potato, resistance_to: late_blight_on_potato]),
        cv('Krantz', [resistance_to: early_blight_on_potato, resistance_to: late_blight_on_potato]),
        cv('Cherokee', [resistance_to: late_blight_on_potato]),
        cv('Onoway', [resistance_to: late_blight_on_potato, resistance_to: potato_scab]),
        cv('Rosa', [resistance_to: late_blight_on_potato]),
        cv('Sebago', [resistance_to: late_blight_on_potato]),
        cv('Norland', [resistance_to: potato_scab]),
        cv('Pungo', [resistance_to: potato_scab]),
        cv('Russet Burbank', [resistance_to: potato_scab]),
        cv('Russian Banana', [resistance_to: potato_scab]),
        cv('Superior', [resistance_to: potato_scab])
    ],
    cultural_context: [
        requires_deeply_worked_well_drained_soil,
        prefers_soil_with_high_organic_matter,
        prefers_ph_between_5_0_and_6_8,
        requires_moderate_to_high_levels_of_nutrients,
        needs_consistent_soil_moisture,
        avoid_planting_after_solanaceous_crops_or_strawberries_or_brambles,
        avoid_planting_after_sod_or_grains,
        usually_grown_from_seed_potatoes_or_buds,
        plant_certified_disease_free_tubers,
        pre_condition_tubers_before_planting,
        plant_when_soil_is_at_least_40_f
    ]
]).

% Potato Pests
frame(pest, [
    name: colorado_potato_beetle,
    type: insect,
    scientific_name: 'Leptinotarsa decemlineata',
    symptoms: [large_ragged_holes_in_leaves, defoliation],
    monitoring: [check_undersides_of_leaves_for_eggs_and_larvae, look_for_striped_beetles],
    action_threshold: '',
    controls: [handpick_beetles_and_larvae, squash_egg_masses, spray_btsd_for_larvae, cover_plants_with_row_cover, apply_thick_straw_mulch],
    cultural_context: [oval_yellowish_orange_beetles_with_black_stripes, larvae_are_humpbacked_dark_orange_grubs_with_black_spots]
]).

frame(pest, [
    name: potato_aphid,
    type: insect,
    scientific_name: '',
    symptoms: [stippled_yellow_and_stunted_leaves],
    monitoring: [inspect_young_leaves_for_tiny_pink_insects],
    action_threshold: '',
    controls: [knock_off_plants_with_water_blast, spray_insecticidal_soap, cover_plants_with_row_cover],
    cultural_context: [tiny_pink_insects_found_on_young_leaves, vectors_for_viral_diseases]
]).

frame(pest, [
    name: tuberworm,
    type: insect,
    scientific_name: '',
    symptoms: [tunnels_in_tubers_stems_and_leaves, browned_silk_lined_tunnels_in_potatoes],
    monitoring: [check_tubers_stems_and_leaves_for_damage],
    action_threshold: '',
    controls: [keep_tubers_hilled_with_soil, remove_dead_vines_before_digging, cover_plants_with_row_cover],
    cultural_context: [pinkish_white_larvae_half_inch_long]
]).

% Potato Diseases
frame(disease, [
    name: early_blight_on_potato,
    type: fungal_disease,
    scientific_name: 'Alternaria solani',
    symptoms: [gray_brown_concentrically_ringed_spots_on_leaves, spots_merge_and_cover_entire_leaf, leaves_yellow_and_fall_off, dark_blotches_on_tuber_skin, dark_corky_areas_in_tuber_flesh],
    monitoring: [inspect_leaves_regularly_for_spots],
    action_threshold: '',
    controls: [spray_copper_or_bordeaux_mix_in_warm_wet_weather, spray_antitranspirant_before_symptoms_appear, plant_resistant_cultivars_butte_kennebec_krantz],
    cultural_context: [active_during_warm_rainy_weather]
]).

frame(disease, [
    name: late_blight_on_potato,
    type: fungal_disease,
    scientific_name: 'Phytophthora infestans',
    symptoms: [water_soaked_brown_spots_on_leaves, white_velvety_growth_on_leaf_undersides, dark_water_soaked_stems, dark_blotches_on_tuber_skin, dark_corky_areas_in_tuber_flesh],
    monitoring: [inspect_leaves_and_stems_especially_in_wet_weather],
    action_threshold: '',
    controls: [spray_copper_in_wet_weather, spray_compost_extract_preventatively, plant_tolerant_cultivars],
    cultural_context: [active_during_moderately_warm_rainy_weather, notorious_for_causing_irish_potato_famine]
]).

frame(disease, [
    name: bacterial_ring_rot,
    type: bacterial_disease,
    scientific_name: '',
    symptoms: [leaves_turn_yellow_between_veins, leaves_curl_upward, shoots_stunted_at_tip, wilted_stems, whitish_ooze_from_cut_stems, black_rotted_ring_at_stem_end_of_tuber, soft_light_brown_ring_in_tuber_flesh],
    monitoring: [inspect_plants_for_wilting_and_stunting],
    action_threshold: '',
    controls: [destroy_infected_plants, plant_certified_disease_free_seed, wash_knife_between_cuts_when_cutting_seed_pieces],
    cultural_context: [highly_contagious_bacterial_disease]
]).

frame(disease, [
    name: black_leg,
    type: bacterial_disease,
    scientific_name: '',
    symptoms: [stem_black_and_shrunken_above_soil_line, plant_yellowing, plant_stunting, wilting],
    monitoring: [inspect_stem_bases_regularly],
    action_threshold: '',
    controls: [destroy_diseased_plants, plant_in_well_drained_soil, avoid_overwatering, plant_resistant_cultivars],
    cultural_context: [bacterial_disease_favored_by_wet_conditions]
]).

frame(disease, [
    name: potato_scab,
    type: bacterial_disease,
    scientific_name: 'Streptomyces scabies',
    symptoms: [rough_corky_spots_on_tuber_skin],
    monitoring: [examine_harvested_tubers],
    action_threshold: '',
    controls: [keep_soil_ph_below_5_5, plant_resistant_cultivars],
    cultural_context: [common_soil_borne_disease]
]).

frame(disease, [
    name: potato_scurf,
    type: fungal_disease,
    scientific_name: '',
    symptoms: [brown_or_black_spots_or_patches_on_tuber_skin],
    monitoring: [examine_harvested_tubers],
    action_threshold: '',
    controls: [soak_seed_pieces_in_compost_tea_before_planting, avoid_planting_affected_tubers],
    cultural_context: [fungal_disease_that_affects_tuber_appearance]
]).

frame(disease, [
    name: hollow_heart,
    type: physiological_disorder,
    scientific_name: '',
    symptoms: [gray_to_black_areas_in_potato_flesh, hollow_centers_in_tubers],
    monitoring: [examine_cut_tubers],
    action_threshold: '',
    controls: [maintain_consistent_soil_moisture, prevent_extreme_temperature_fluctuations, ensure_adequate_potassium_and_phosphorus],
    cultural_context: [caused_by_growing_conditions_rather_than_pathogens]
]).

frame(disease, [
    name: potato_leafroll_virus,
    type: viral_disease,
    scientific_name: '',
    symptoms: [upward_rolling_leaf_edges, yellow_green_leaf_color],
    monitoring: [inspect_plants_for_leaf_symptoms],
    action_threshold: '',
    controls: [destroy_infected_plants, control_aphids, plant_resistant_cultivars],
    cultural_context: [aphid_transmitted_virus]
]).

% Potato Cultural Practices
frame(practice, [
    name: soak_potato_seed_pieces_in_compost_tea,
    type: cultural_control,
    controls: [],
    resolves: [potato_scurf, seed_piece_rot, various_potato_diseases],
    description: 'Soak potato seed pieces in compost tea for several hours before planting to help prevent disease problems.',
    cost: low,
    difficulty: low,
    season: [pre_planting],
    cultural_context: [disease_prevention]
]).

frame(practice, [
    name: hill_potato_plants_with_soil_or_mulch,
    type: cultural_control,
    controls: [tuberworm],
    resolves: [greening_of_tubers, temperature_fluctuations],
    description: 'Hill potato plants with soil or mulch as they grow to prevent tuber exposure to light and to maintain more consistent soil temperature.',
    cost: low,
    difficulty: low,
    season: [growing_season],
    cultural_context: [prevents_solanine_development_in_tubers]
]).

frame(practice, [
    name: proper_potato_curing_and_storage,
    type: post_harvest,
    controls: [],
    resolves: [storage_rots_in_potato],
    description: 'Cure harvested potatoes by storing them between 50° and 60°F for 2-3 weeks, then store at 35° to 45°F in a humid place.',
    cost: low,
    difficulty: medium,
    season: [post_harvest],
    cultural_context: [extends_storage_life]
]).

% =========================
% RADISH CROP
% =========================
frame(crop, [
    name: radish,
    pests: [cabbage_maggot_on_radish, flea_beetle_general],
    diseases: [club_root_on_radish, downy_mildew_on_radish, black_root_on_radish, scab_on_radish],
    resistant_cultivars: [
        cv('Fancy Red', [resistance_to: fusarium_yellows]),
        cv('Fuego', [resistance_to: fusarium_yellows]),
        cv('Red Devil', [resistance_to: fusarium_yellows]),
        cv('Red King', [resistance_to: fusarium_yellows, resistance_to: club_root_on_radish]),
        cv('Red Pak', [resistance_to: fusarium_yellows]),
        cv('Saxafire', [resistance_to: club_root_on_radish])
    ],
    cultural_context: [
        annual_or_biennial_vegetable,
        grown_for_crisp_peppery_roots,
        prefers_cool_moist_conditions,
        prefers_ph_between_5_5_and_6_8,
        requires_light_relatively_rich_soil,
        best_planted_as_soon_as_soil_can_be_worked_in_spring,
        optimal_growing_temperature_between_50_and_65_f,
        poor_growth_above_75_f,
        requires_rapid_growth_for_mild_tender_roots,
        needs_heavy_watering_first_2_weeks_after_emergence,
        light_application_of_compost_sufficient_for_good_crop,
        does_not_tolerate_soils_high_in_salt,
        related_to_cabbage_with_similar_problems,
        some_cultivars_grown_for_seed_pods_rather_than_roots,
        some_daikon_cultivars_designed_for_summer_planting
    ]
]).

% Radish Pests
frame(pest, [
    name: cabbage_maggot_on_radish,
    type: insect,
    scientific_name: '',
    symptoms: [slimy_winding_tunnels_in_roots],
    monitoring: [check_roots_for_tunnels, look_for_white_maggots_in_tunnels],
    action_threshold: '',
    controls: [frequent_light_cultivation_when_plants_young, remove_and_destroy_infested_plants],
    cultural_context: [maggots_are_white_and_quarter_inch_long, adults_resemble_houseflies, eggs_laid_on_soil_near_plant_base]
]).

% Radish Diseases
frame(disease, [
    name: club_root_on_radish,
    type: fungal_disease,
    scientific_name: '',
    symptoms: [enlarged_clublike_roots],
    monitoring: [inspect_roots_at_harvest],
    action_threshold: '',
    controls: [destroy_infected_plants, rotate_crops, provide_good_drainage, plant_tolerant_cultivars],
    cultural_context: [soil_borne_fungal_disease]
]).

frame(disease, [
    name: scab_on_radish,
    type: fungal_disease,
    scientific_name: '',
    symptoms: [rough_dark_spots_on_root_skin],
    monitoring: [check_roots_at_harvest],
    action_threshold: '',
    controls: [keep_soil_moist, maintain_ph_below_6_5, spray_foliage_with_epsom_salts_solution, side_dress_with_compost_to_add_magnesium],
    cultural_context: [problem_in_dry_soil_when_ph_high_and_magnesium_low]
]).

frame(disease, [
    name: downy_mildew_on_radish,
    type: fungal_disease,
    scientific_name: '',
    symptoms: [cracked_roots, rough_skin, dark_flesh],
    monitoring: [inspect_roots_for_cracks_and_dark_flesh],
    action_threshold: '',
    controls: [provide_well_drained_soil, use_four_year_crop_rotation],
    cultural_context: [fungal_disease_affecting_root_quality]
]).

frame(disease, [
    name: black_root_on_radish,
    type: fungal_disease,
    scientific_name: '',
    symptoms: [cracked_roots, rough_skin, dark_flesh],
    monitoring: [inspect_roots_for_cracks_and_dark_flesh],
    action_threshold: '',
    controls: [provide_well_drained_soil, use_four_year_crop_rotation],
    cultural_context: [fungal_disease_causing_dark_discoloration_in_roots]
]).

% Radish Cultural Practices
frame(practice, [
    name: succession_planting_of_radishes,
    type: cultural_control,
    controls: [],
    resolves: [ensuring_continuous_supply, preventing_overmaturity],
    description: 'Plant small batches of radishes weekly until early summer to ensure continuous supply and prevent overmaturity issues.',
    cost: low,
    difficulty: low,
    season: [spring],
    cultural_context: [radishes_are_at_their_best_quality_for_only_a_few_days]
]).

frame(practice, [
    name: consistent_soil_moisture_for_radishes,
    type: cultural_control,
    controls: [],
    resolves: [cracked_roots, tough_dry_roots],
    description: 'Maintain even soil moisture throughout growing period to prevent root cracking and ensure tender flesh.',
    cost: low,
    difficulty: low,
    season: [growing_season],
    cultural_context: [rapid_growth_essential_for_quality]
]).

frame(practice, [
    name: cold_protection_for_radishes,
    type: cultural_control,
    controls: [],
    resolves: [soft_shriveled_roots],
    description: 'Protect roots with mulch when temperatures drop below 32°F to prevent cold injury.',
    cost: low,
    difficulty: low,
    season: [late_fall, winter],
    cultural_context: [prevents_cold_damage_to_harvested_roots]
]).

frame(nutrient_disorder, [
    name: nitrogen_deficiency_in_radish,
    type: nutrient_disorder,
    symptoms: [small_imperfect_roots, yellow_leaves],
    monitoring: [check_leaf_color],
    action_threshold: '',
    controls: [spray_leaves_with_compost_tea_or_fish_emulsion, side_dress_with_compost],
    cultural_context: [causes_stunted_growth_and_poor_root_development]
]).

frame(nutrient_disorder, [
    name: phosphorus_deficiency_in_radish,
    type: nutrient_disorder,
    symptoms: [small_imperfect_roots, purple_leaves],
    monitoring: [check_leaf_color],
    action_threshold: '',
    controls: [spray_leaves_with_compost_tea_or_fish_emulsion, side_dress_with_compost],
    cultural_context: [causes_stunted_growth_and_poor_root_development]
]).

% =========================
% SPINACH CROP
% =========================
frame(crop, [
    name: spinach,
    pests: [aphid_on_spinach, leafminer_on_spinach, flea_beetle_on_spinach, caterpillar_general],
    diseases: [fusarium_wilt_on_spinach, curly_top_virus, mosaic_virus_on_spinach, downy_mildew_on_spinach, white_rust_on_spinach, anthracnose_on_spinach],
    resistant_cultivars: [
        cv('Indian Summer', [resistance_to: mosaic_virus_on_spinach, resistance_to: downy_mildew_on_spinach]),
        cv('Melody', [resistance_to: mosaic_virus_on_spinach, resistance_to: downy_mildew_on_spinach]),
        cv('Winter Bloomsdale', [resistance_to: mosaic_virus_on_spinach, resistance_to: downy_mildew_on_spinach]),
        cv('Crystal Savoy', [resistance_to: downy_mildew_on_spinach]),
        cv('Fall Green', [resistance_to: downy_mildew_on_spinach, resistance_to: white_rust_on_spinach]),
        cv('Gladiator', [resistance_to: downy_mildew_on_spinach]),
        cv('Kent', [resistance_to: downy_mildew_on_spinach]),
        cv('Olympia', [resistance_to: downy_mildew_on_spinach]),
        cv('Seven R', [resistance_to: downy_mildew_on_spinach]),
        cv('Tyee', [resistance_to: downy_mildew_on_spinach])
    ],
    cultural_context: [
        cool_season_annual_vegetable,
        savoy_leaved_and_flat_leaved_types,
        prefers_well_drained_soil_with_high_organic_matter,
        prefers_ph_between_6_0_and_7_0,
        germinates_best_at_soil_temperatures_between_45_and_75_f,
        can_germinate_as_low_as_35_f,
        mature_plants_survive_temperatures_of_20_f_if_hardened,
        prolonged_exposure_to_temperatures_below_45_f_causes_bolting,
        temperatures_above_75_f_cause_bolting,
        long_days_cause_bolting,
        requires_consistent_moisture,
        requires_moderate_potassium_and_phosphorus,
        requires_high_nitrogen,
        sensitive_to_low_calcium_and_boron_levels
    ]
]).

% Spinach Pests
frame(pest, [
    name: aphid_on_spinach,
    type: insect,
    scientific_name: '',
    symptoms: [yellow_curled_leaves, stunted_growth],
    monitoring: [check_undersides_of_lower_leaves_near_midrib],
    action_threshold: '',
    controls: [spray_plants_with_water, spray_insecticidal_soap_for_severe_infestations],
    cultural_context: [can_be_green_pink_black_gray_or_white, soft_bodied_small_insects, often_with_fluffy_coating]
]).

frame(pest, [
    name: leafminer_on_spinach,
    type: insect,
    scientific_name: '',
    symptoms: [light_colored_tunnels_in_leaves, light_colored_blotches_on_leaves],
    monitoring: [inspect_leaves_for_tunnels_or_blotches],
    action_threshold: '',
    controls: [destroy_mined_leaves, till_soil_after_harvest],
    cultural_context: [larvae_are_creamy_white_maggots_one_eighth_inch_long]
]).

frame(pest, [
    name: flea_beetle_on_spinach,
    type: insect,
    scientific_name: '',
    symptoms: [small_holes_in_leaves],
    monitoring: [check_for_tiny_beetles_that_hop_when_disturbed],
    action_threshold: '',
    controls: [spray_or_dust_with_pyrethrin_for_severe_infestations, cover_young_plants_with_row_cover, plant_in_partial_shade],
    cultural_context: [tiny_black_brown_or_bronze_beetles, hop_when_disturbed, larvae_are_small_and_white]
]).

% Spinach Diseases
frame(disease, [
    name: fusarium_wilt_on_spinach,
    type: fungal_disease,
    scientific_name: '',
    symptoms: [yellowing_leaves, stunted_growth, wilting],
    monitoring: [watch_for_wilting_despite_adequate_moisture],
    action_threshold: '',
    controls: [destroy_infected_plants, plant_in_cool_seasons_when_soil_is_below_70_f],
    cultural_context: [thrives_in_warm_soil_70_to_80_f]
]).

frame(disease, [
    name: curly_top_virus,
    type: viral_disease,
    scientific_name: '',
    symptoms: [yellow_deformed_stunted_young_leaves, leaf_death],
    monitoring: [check_young_leaves_for_deformities],
    action_threshold: '',
    controls: [destroy_infected_plants, control_beet_leafhoppers],
    cultural_context: [transmitted_by_beet_leafhoppers]
]).

frame(disease, [
    name: mosaic_virus_on_spinach,
    type: viral_disease,
    scientific_name: '',
    symptoms: [mottled_older_leaves, deformed_leaves],
    monitoring: [inspect_leaves_for_mottled_pattern],
    action_threshold: '',
    controls: [destroy_infected_plants, control_aphids, plant_resistant_cultivars],
    cultural_context: [also_called_blight_or_yellows, spread_by_aphids]
]).

frame(disease, [
    name: downy_mildew_on_spinach,
    type: fungal_disease,
    scientific_name: '',
    symptoms: [pale_yellow_patches_on_upper_leaf_surfaces, grayish_mold_on_leaf_undersides],
    monitoring: [inspect_both_sides_of_leaves_with_yellowing],
    action_threshold: '',
    controls: [destroy_infected_leaves_or_plants, thin_plants_to_increase_air_circulation, plant_resistant_cultivars],
    cultural_context: [favored_by_cool_moist_conditions]
]).

frame(disease, [
    name: white_rust_on_spinach,
    type: fungal_disease,
    scientific_name: '',
    symptoms: [pale_yellow_patches_on_upper_leaf_surfaces, white_blisters_on_leaf_undersides],
    monitoring: [inspect_both_sides_of_leaves_with_yellowing],
    action_threshold: '',
    controls: [destroy_infected_leaves_or_plants, thin_plants_to_increase_air_circulation, plant_tolerant_cultivars],
    cultural_context: [favored_by_cool_moist_conditions]
]).

frame(disease, [
    name: anthracnose_on_spinach,
    type: fungal_disease,
    scientific_name: '',
    symptoms: [water_soaked_spots_on_leaves, brown_spots_on_leaves],
    monitoring: [inspect_leaves_especially_in_wet_weather],
    action_threshold: '',
    controls: [destroy_infected_leaves_or_plants, spray_with_sulfur_to_prevent_spread, thin_plants_for_good_air_movement],
    cultural_context: [spots_enlarge_rapidly_in_wet_weather]
]).

% Spinach Cultural Practices
frame(practice, [
    name: spinach_seed_soaking,
    type: cultural_control,
    controls: [],
    resolves: [soilborne_diseases, slow_germination],
    description: 'Soak spinach seeds in compost tea for 30 minutes before planting to speed germination and help suppress soilborne diseases.',
    cost: low,
    difficulty: low,
    season: [pre_planting],
    cultural_context: [improves_germination_success]
]).

frame(practice, [
    name: spinach_mulching,
    type: cultural_control,
    controls: [weed_competition],
    resolves: [moisture_loss, soil_warming],
    description: 'Spread a thin layer of mulch around spinach plants to conserve moisture, suppress weeds, and keep soil cool.',
    cost: low,
    difficulty: low,
    season: [growing_season],
    cultural_context: [helps_prevent_bolting]
]).

frame(practice, [
    name: succession_planting_of_spinach,
    type: cultural_control,
    controls: [],
    resolves: [continuous_harvest],
    description: 'Plant spinach in succession during cool seasons to ensure continuous harvest before plants bolt.',
    cost: low,
    difficulty: low,
    season: [spring, fall],
    cultural_context: [extends_harvest_period]
]).

frame(practice, [
    name: partial_shade_for_spinach,
    type: cultural_control,
    controls: [heat_stress, early_bolting, flea_beetle_on_spinach],
    resolves: [],
    description: 'Plant spinach in filtered shade in warmer climates to extend its season into warmer months and reduce pest pressure.',
    cost: low,
    difficulty: low,
    season: [warm_months],
    cultural_context: [extends_growing_season_in_warm_areas]
]).

frame(practice, [
    name: row_cover_for_spinach,
    type: cultural_control,
    controls: [flea_beetle_on_spinach, caterpillar_general],
    resolves: [temperature_fluctuations],
    description: 'Cover young spinach plants with row cover until temperatures stabilize to prevent temperature-induced bolting and protect from pests.',
    cost: low,
    difficulty: low,
    season: [early_spring, late_fall],
    cultural_context: [can_be_left_on_until_harvest_in_moderate_temperatures]
]).

% =========================
% SQUASH CROP
% =========================
frame(crop, [
    name: squash,
    pests: [cucumber_beetle, squash_bug, aphid_on_squash, mite_on_squash, squash_vine_borer, pickleworm],
    diseases: [mosaic_on_squash, downy_mildew_on_squash, powdery_mildew_on_squash, angular_leaf_spot, scab_on_squash, alternaria_leaf_blight, bacterial_wilt_on_squash],
    resistant_cultivars: [
        cv('Bennings Green Tint', [resistance_to: cucumber_beetle]),
        cv('Blue Hubbard', [resistance_to: cucumber_beetle]),
        cv('Early Butternut Hybrid', [resistance_to: cucumber_beetle]),
        cv('Seneca', [resistance_to: cucumber_beetle]),
        cv('Table King', [resistance_to: cucumber_beetle]),
        cv('Early Prolific', [resistance_to: squash_bug]),
        cv('Early Summer', [resistance_to: squash_bug]),
        cv('Royal Acorn', [resistance_to: squash_bug]),
        cv('Table Queen', [resistance_to: squash_bug]),
        cv('Multipik', [resistance_to: mosaic_on_squash, resistance_to: powdery_mildew_on_squash]),
        cv('Napolini', [resistance_to: mosaic_on_squash]),
        cv('Superpik', [resistance_to: mosaic_on_squash]),
        cv('Superset', [resistance_to: mosaic_on_squash]),
        cv('Cocozelle', [resistance_to: aphid_on_squash]),
        cv('Super Select', [resistance_to: downy_mildew_on_squash]),
        cv('Zucchini Select', [resistance_to: downy_mildew_on_squash, resistance_to: powdery_mildew_on_squash]),
        cv('Sweet Mama Hybrid', [resistance_to: squash_vine_borer])
    ],
    cultural_context: [
        frost_tender_annual,
        summer_squash_eaten_before_seeds_harden,
        winter_squash_harvested_when_mature,
        species_include_cucurbita_maxima_mixta_moschata_pepo,
        needs_60_f_soil_to_germinate,
        prefers_well_drained_loose_textured_soil,
        prefers_soil_with_high_organic_matter,
        grows_in_ph_between_5_5_and_6_8,
        prefers_ph_above_6_0,
        requires_lots_of_water_but_not_saturated_soil,
        need_dry_leaves_to_prevent_disease,
        caution_with_insecticidal_soap_and_copper_sprays,
        needs_insect_pollination_for_fruit_set
    ]
]).

% Squash Pests
frame(pest, [
    name: cucumber_beetle,
    type: insect,
    scientific_name: '',
    symptoms: [chewed_holes_in_leaves, damaged_roots],
    monitoring: [check_young_leaves_for_beetles_with_stripes_or_spots],
    action_threshold: '',
    controls: [spray_or_dust_with_pyrethrin, plant_resistant_cultivars],
    cultural_context: [adults_one_quarter_inch_long_greenish_yellow_beetles_with_black_stripes_or_spots, larvae_feed_on_roots, vectors_for_bacterial_wilt_and_viral_diseases]
]).

frame(pest, [
    name: squash_bug,
    type: insect,
    scientific_name: '',
    symptoms: [pale_green_patches_on_leaves, wilted_blackened_leaves],
    monitoring: [check_undersides_of_leaves_for_bright_orange_eggs, look_under_boards_placed_near_plants],
    action_threshold: '',
    controls: [handpick_adults_and_eggs, trap_under_boards_and_destroy_in_morning, plant_resistant_cultivars],
    cultural_context: [adults_are_brownish_black_half_inch_long, immature_bugs_whitish_green_with_dark_heads]
]).

frame(pest, [
    name: aphid_on_squash,
    type: insect,
    scientific_name: '',
    symptoms: [yellow_curled_wilted_leaves],
    monitoring: [check_plants_for_small_soft_bodied_insects],
    action_threshold: '',
    controls: [knock_off_with_strong_blast_of_water, spray_with_diluted_insecticidal_soap, use_foil_mulch, plant_silver_leaved_cultivars],
    cultural_context: [small_green_pink_gray_black_or_white_insects, may_have_fluffy_coating, vectors_for_viral_diseases]
]).

frame(pest, [
    name: mite_on_squash,
    type: insect,
    scientific_name: '',
    symptoms: [yellow_puckered_leaves, bronzed_leaves, fine_webbing_on_leaf_undersides],
    monitoring: [check_undersides_of_leaves_for_tiny_spiderlike_creatures],
    action_threshold: '',
    controls: [spray_with_weak_insecticidal_soap],
    cultural_context: [tiny_red_yellow_or_green_spiderlike_creatures, worst_in_dry_hot_weather]
]).

frame(pest, [
    name: squash_vine_borer,
    type: insect,
    scientific_name: '',
    symptoms: [sudden_wilting_of_vines, sawdustlike_excrement_from_stem_holes],
    monitoring: [check_stems_near_soil_for_entry_holes_and_excrement],
    action_threshold: '',
    controls: [slit_stems_and_remove_larvae, cover_damaged_stems_with_soil, inject_btk_into_stems, spray_stem_base_with_btk_weekly, plant_resistant_cultivars],
    cultural_context: [fat_white_one_inch_long_larvae_burrow_into_stems]
]).

frame(pest, [
    name: pickleworm,
    type: insect,
    scientific_name: '',
    symptoms: [tunneled_fruit],
    monitoring: [check_fruit_for_tunnels_especially_near_soil_level],
    action_threshold: '',
    controls: [keep_fruit_off_ground_or_mulch],
    cultural_context: [larvae_are_pale_green_with_black_up_to_three_quarters_inch_long]
]).

% Squash Diseases
frame(disease, [
    name: mosaic_on_squash,
    type: viral_disease,
    scientific_name: '',
    symptoms: [yellow_patches_on_leaves, mottled_distorted_older_leaves, deformed_fruit, yellow_green_mottled_fruit],
    monitoring: [check_leaves_for_mottling_and_distortion],
    action_threshold: '',
    controls: [remove_and_destroy_diseased_plants, control_aphids_and_cucumber_beetles, plant_resistant_cultivars],
    cultural_context: [several_types_of_mosaic_viruses_affect_squash]
]).

frame(disease, [
    name: downy_mildew_on_squash,
    type: fungal_disease,
    scientific_name: '',
    symptoms: [yellow_mottling_between_leaf_veins, purple_spots_on_leaf_undersides, brown_dead_older_leaves],
    monitoring: [check_both_sides_of_leaves_with_yellowing],
    action_threshold: '',
    controls: [spray_with_dilute_copper_solution, plant_resistant_cultivars],
    cultural_context: [progressive_disease_affecting_all_leaves]
]).

frame(disease, [
    name: powdery_mildew_on_squash,
    type: fungal_disease,
    scientific_name: '',
    symptoms: [powdery_white_spots_on_upper_leaf_surfaces, brown_dry_leaves],
    monitoring: [check_upper_leaf_surfaces_for_white_powdery_growth],
    action_threshold: '',
    controls: [keep_foliage_dry, avoid_touching_wet_plants, spray_with_dilute_copper_solution, plant_resistant_cultivars],
    cultural_context: [can_kill_plants_if_severe]
]).

frame(disease, [
    name: angular_leaf_spot,
    type: bacterial_disease,
    scientific_name: '',
    symptoms: [water_soaked_spots_on_leaves, gray_dead_spots_that_drop_out, small_cracked_white_spots_on_fruit],
    monitoring: [check_leaves_for_angular_spots_and_shothole_appearance],
    action_threshold: '',
    controls: [keep_foliage_dry, avoid_touching_wet_plants, spray_with_dilute_copper_solution],
    cultural_context: [bacterial_disease_that_affects_both_leaves_and_fruit]
]).

frame(disease, [
    name: scab_on_squash,
    type: fungal_disease,
    scientific_name: '',
    symptoms: [water_soaked_spots_on_leaves, sunken_brown_spots_with_gummy_ooze_on_fruit],
    monitoring: [check_both_leaves_and_fruit],
    action_threshold: '',
    controls: [keep_foliage_dry, avoid_touching_wet_plants, spray_with_dilute_copper_solution],
    cultural_context: [damage_worst_in_cool_moist_weather]
]).

frame(disease, [
    name: alternaria_leaf_blight,
    type: fungal_disease,
    scientific_name: '',
    symptoms: [dark_brown_spots_with_concentric_rings_on_leaves, curled_dropping_leaves, dark_sunken_spots_with_rings_on_fruit],
    monitoring: [check_older_leaves_first_for_ringed_spots],
    action_threshold: '',
    controls: [keep_foliage_dry, avoid_touching_wet_plants, spray_with_dilute_copper_solution],
    cultural_context: [progressive_disease_typically_starting_on_older_leaves]
]).

frame(disease, [
    name: bacterial_wilt_on_squash,
    type: bacterial_disease,
    scientific_name: '',
    symptoms: [midday_wilting_starting_with_younger_leaves, progressive_wilting_with_green_leaves, milky_sticky_astringent_sap],
    monitoring: [check_wilted_stems_by_cutting_and_pressing_out_sap],
    action_threshold: '',
    controls: [destroy_infected_plants_immediately, control_cucumber_beetles],
    cultural_context: [spread_by_cucumber_beetles]
]).

% Squash Cultural Practices
frame(practice, [
    name: row_cover_for_squash,
    type: cultural_control,
    controls: [cucumber_beetle, cold_damage],
    resolves: [],
    description: 'Cover young squash plants with floating row cover to protect from insects and late cold snaps, but remove when flowering begins to allow for pollination.',
    cost: low,
    difficulty: low,
    season: [early_season],
    cultural_context: [must_remove_for_pollination]
]).

frame(practice, [
    name: mulching_for_squash,
    type: cultural_control,
    controls: [],
    resolves: [moisture_loss],
    description: 'Use mulch to conserve water. Black plastic works well in northern areas; organic mulch is good but may harbor squash bugs; foil mulch helps prevent aphids.',
    cost: low,
    difficulty: low,
    season: [growing_season],
    cultural_context: [black_plastic_can_overheat_soil_in_very_warm_areas]
]).

frame(practice, [
    name: squash_crop_rotation,
    type: cultural_control,
    controls: [],
    resolves: [disease_buildup, pest_buildup],
    description: 'Rotate crops so that no member of the cucurbit family (cucumbers, melons, and squash) is grown in the same place more often than every 4 years.',
    cost: low,
    difficulty: low,
    season: [planning],
    cultural_context: [prevents_pest_and_disease_cycles]
]).

frame(practice, [
    name: fruit_support_for_squash,
    type: cultural_control,
    controls: [],
    resolves: [fruit_rot],
    description: 'Support squash fruit on scraps of wood to prevent rot where fruit contacts soil.',
    cost: low,
    difficulty: low,
    season: [fruiting],
    cultural_context: [particularly_important_in_wet_conditions]
]).

frame(practice, [
    name: hand_pollination_of_squash,
    type: cultural_control,
    controls: [],
    resolves: [poor_fruit_set],
    description: 'Hand pollinate female flowers if fruit is not developing due to lack of pollinator activity or poor pollination.',
    cost: low,
    difficulty: low,
    season: [flowering],
    cultural_context: [helps_when_pollinator_population_is_low]
]).

% =========================
% TOMATO CROP
% =========================
frame(crop, [
    name: tomato,
    pests: [aphid_on_tomato, mite_on_tomato, root_knot_nematode_general, colorado_potato_beetle, hornworm, flea_beetle_on_tomato, cutworm, stink_bug, tomato_fruitworm, tomato_pinworm],
    diseases: [tobacco_mosaic_virus, fusarium_wilt_on_tomato, verticillium_wilt, southern_bacterial_wilt, bacterial_spot, bacterial_speck, bacterial_canker, late_blight_on_tomato, early_blight_on_tomato, septoria_leaf_spot, anthracnose_on_tomato, damping_off],
    physiological_disorders: [blossom_end_rot, sunscald, graywall, fruit_cracking, cat_facing, walnut_wilt],
    resistant_cultivars: [
        cv('F', [resistance_to: fusarium_wilt_on_tomato]),
        cv('V', [resistance_to: verticillium_wilt]),
        cv('T', [resistance_to: tobacco_mosaic_virus]),
        cv('N', [resistance_to: root_knot_nematode_general]),
        cv('Saturn', [resistance_to: southern_bacterial_wilt]),
        cv('Venus', [resistance_to: southern_bacterial_wilt]),
        cv('Pieraline', [resistance_to: late_blight_on_tomato]),
        cv('Kotlas', [resistance_to: early_blight_on_tomato]),
        cv('Early Girl', [resistance_to: fruit_cracking]),
        cv('Jet Star', [resistance_to: fruit_cracking]),
        cv('Roma', [resistance_to: fruit_cracking])
    ],
    cultural_context: [
        tender_perennial_grown_as_annual,
        fruits_vary_in_color_and_size,
        determinant_types_grow_to_fixed_height_and_produce_heavily_over_short_period,
        indeterminant_types_grow_and_produce_until_frost,
        requires_full_sun,
        requires_deep_soil,
        prefers_ph_between_6_0_and_6_8,
        benefits_from_high_organic_matter,
        requires_moderate_nitrogen_and_phosphorus,
        requires_moderate_to_high_potassium_and_calcium,
        grows_best_between_75_and_90_f,
        temperatures_over_100_f_kill_blossoms,
        temperatures_below_50_f_cause_chilling_injury,
        should_not_follow_solanaceous_crops_for_3_to_5_years
    ]
]).

% Tomato Pests
frame(pest, [
    name: aphid_on_tomato,
    type: insect,
    scientific_name: '',
    symptoms: [yellow_distorted_sticky_leaves, brown_spots_on_leaves],
    monitoring: [check_for_small_insects_on_leaves],
    action_threshold: '',
    controls: [knock_off_with_water_blast, spray_insecticidal_soap_in_evening, use_neem_or_pyrethrin_for_severe_infestations],
    cultural_context: [small_green_black_gray_pink_or_white_insects, may_have_fluffy_coating, vectors_for_viral_diseases]
]).

frame(pest, [
    name: mite_on_tomato,
    type: insect,
    scientific_name: '',
    symptoms: [stippled_or_bronzed_leaves, fine_webbing_under_leaves, dry_falling_leaves],
    monitoring: [check_undersides_of_leaves_for_tiny_spiderlike_creatures],
    action_threshold: '',
    controls: [spray_with_insecticidal_soap_or_sulfur],
    cultural_context: [tiny_spiderlike_insects, thrive_in_hot_dry_weather]
]).

frame(pest, [
    name: colorado_potato_beetle,
    type: insect,
    scientific_name: '',
    symptoms: [large_ragged_holes_in_leaves, defoliated_plants, chewed_holes_in_green_fruit],
    monitoring: [check_plants_for_striped_beetles_and_orange_grubs],
    action_threshold: '',
    controls: [handpick_insects, spray_btsd_for_young_larvae],
    cultural_context: [yellowish_orange_oval_beetles_with_black_stripes, larvae_are_humpbacked_dark_orange_grubs_with_black_spots]
]).

frame(pest, [
    name: hornworm,
    type: insect,
    scientific_name: '',
    symptoms: [large_ragged_holes_in_leaves, defoliated_plants, chewed_holes_in_green_fruit],
    monitoring: [check_plants_for_large_green_caterpillars_with_diagonal_stripes],
    action_threshold: '',
    controls: [handpick_caterpillars, spray_btk, do_not_spray_if_caterpillars_have_white_parasitic_wasp_cocoons],
    cultural_context: [large_3_to_4_5_inch_caterpillars, tobacco_hornworm_has_red_horn, tomato_hornworm_has_black_horn]
]).

frame(pest, [
    name: flea_beetle_on_tomato,
    type: insect,
    scientific_name: '',
    symptoms: [small_holes_in_leaves],
    monitoring: [check_for_tiny_beetles_that_hop_when_disturbed],
    action_threshold: '',
    controls: [spray_or_dust_with_pyrethrin_for_severe_infestations, protect_transplants_with_row_cover],
    cultural_context: [tiny_black_brown_or_bronze_insects_that_hop_when_disturbed]
]).

frame(pest, [
    name: cutworm,
    type: insect,
    scientific_name: '',
    symptoms: [seedlings_clipped_off_at_soil_line],
    monitoring: [check_soil_near_plant_base_for_dull_brown_or_gray_caterpillars],
    action_threshold: '',
    controls: [place_cutworm_collars_around_transplants, sprinkle_moist_bran_mixed_with_btk_on_soil_in_evening, add_parasitic_nematodes_to_soil_before_planting],
    cultural_context: [fat_1_to_2_inch_long_caterpillars, feed_at_night]
]).

frame(pest, [
    name: stink_bug,
    type: insect,
    scientific_name: '',
    symptoms: [pale_yellow_spots_under_fruit_skin, white_spongy_flesh_under_spots, spots_may_have_central_puncture],
    monitoring: [check_plants_for_shield_shaped_bugs],
    action_threshold: '',
    controls: [keep_garden_well_weeded],
    cultural_context: [brown_tan_gray_or_green_half_inch_shield_shaped_bugs, inject_toxin_when_feeding_on_green_fruit]
]).

frame(pest, [
    name: tomato_fruitworm,
    type: insect,
    scientific_name: '',
    symptoms: [small_holes_on_fruit_surface, rotted_hollow_interior, collapsed_fruit],
    monitoring: [check_fruit_for_holes_and_larvae],
    action_threshold: '',
    controls: [destroy_infested_fruit, spray_btk_if_larvae_seen_on_leaves, cover_plants_with_row_cover_until_flowering],
    cultural_context: [larvae_up_to_2_inches_long, light_yellow_green_pink_or_brown_with_spines_and_stripes, also_called_corn_earworm]
]).

frame(pest, [
    name: tomato_pinworm,
    type: insect,
    scientific_name: '',
    symptoms: [narrow_black_tunnels_in_fruit_flesh, small_holes_near_stem],
    monitoring: [check_fruit_for_tunnels_and_small_gray_larvae],
    action_threshold: '',
    controls: [destroy_infested_fruit, till_soil_after_harvest],
    cultural_context: [small_gray_larvae_that_may_have_reddish_markings]
]).

% Tomato Diseases
frame(disease, [
    name: tobacco_mosaic_virus,
    type: viral_disease,
    scientific_name: '',
    symptoms: [yellow_mottled_leaves, narrow_twisted_young_growth, yellow_patches_on_fruit, unevenly_ripening_fruit],
    monitoring: [check_for_mottled_pattern_on_leaves],
    action_threshold: '',
    controls: [destroy_diseased_plants, presoak_seed_in_10_percent_bleach_solution, plant_resistant_cultivars, wash_hands_after_handling_tobacco, control_aphids],
    cultural_context: [can_be_transmitted_mechanically]
]).

frame(disease, [
    name: fusarium_wilt_on_tomato,
    type: fungal_disease,
    scientific_name: '',
    symptoms: [yellowing_of_older_leaves, wilting_of_shoots_or_whole_plant, brown_discoloration_inside_stem],
    monitoring: [watch_for_wilting_despite_adequate_moisture, check_for_discoloration_in_stem],
    action_threshold: '',
    controls: [destroy_infected_plants, presoak_seed_in_10_percent_bleach_solution, plant_resistant_cultivars, control_nematodes],
    cultural_context: [thrives_in_warm_temperatures_80_to_90_f, may_affect_individual_shoots_first]
]).

frame(disease, [
    name: verticillium_wilt,
    type: fungal_disease,
    scientific_name: '',
    symptoms: [yellowing_of_older_leaves, wilting_of_whole_plant, discoloration_inside_stem],
    monitoring: [watch_for_wilting_despite_adequate_moisture, check_for_discoloration_in_stem],
    action_threshold: '',
    controls: [destroy_infected_plants, presoak_seed_in_10_percent_bleach_solution, plant_resistant_cultivars, control_nematodes],
    cultural_context: [thrives_in_temperatures_68_to_75_f, affects_whole_plant, infects_many_plant_species]
]).

frame(disease, [
    name: southern_bacterial_wilt,
    type: bacterial_disease,
    scientific_name: '',
    symptoms: [whole_plant_wilts, leaves_remain_green],
    monitoring: [check_for_wilting_despite_adequate_moisture],
    action_threshold: '',
    controls: [destroy_infected_plants, plant_tolerant_cultivars],
    cultural_context: [most_damaging_in_deep_south]
]).

frame(disease, [
    name: bacterial_spot,
    type: bacterial_disease,
    scientific_name: '',
    symptoms: [small_dark_spots_on_leaves, spots_dry_and_fall_out, leaves_turn_yellow_then_brown, fruit_with_brown_scabby_spots_with_sunken_centers],
    monitoring: [inspect_leaves_for_spots],
    action_threshold: '',
    controls: [spray_with_copper],
    cultural_context: [favored_by_warm_wet_conditions]
]).

frame(disease, [
    name: bacterial_speck,
    type: bacterial_disease,
    scientific_name: '',
    symptoms: [small_dark_spots_on_leaves, spots_dry_and_fall_out, tiny_dark_brown_spots_with_white_borders_on_fruit],
    monitoring: [inspect_leaves_for_spots],
    action_threshold: '',
    controls: [spray_with_copper],
    cultural_context: [favored_by_cool_moist_conditions]
]).

frame(disease, [
    name: bacterial_canker,
    type: bacterial_disease,
    scientific_name: '',
    symptoms: [leaves_with_brown_edges, lower_leaves_wilting_and_curling, light_colored_streaks_on_stems, brown_mealy_stem_interior, fruit_with_tan_raised_spots_with_white_margins],
    monitoring: [check_leaf_edges_and_stems_for_symptoms],
    action_threshold: '',
    controls: [destroy_infected_plants, presoak_seed_in_10_percent_bleach_solution, avoid_wounding_plants, avoid_touching_wet_plants],
    cultural_context: [highly_contagious_bacterial_disease]
]).

frame(disease, [
    name: late_blight_on_tomato,
    type: fungal_disease,
    scientific_name: 'Phytophthora infestans',
    symptoms: [dark_water_soaked_patches_on_leaves, brown_dry_papery_leaves, white_mold_ring_in_wet_weather, blackened_stem_areas, large_irregular_greasy_brown_spots_on_fruit],
    monitoring: [inspect_plants_in_cool_humid_weather],
    action_threshold: '',
    controls: [spray_compost_tea, spray_copper_for_severe_cases, plant_tolerant_cultivars],
    cultural_context: [favored_by_humid_weather_with_cool_nights_below_60_f_and_warm_days_70_to_85_f]
]).

frame(disease, [
    name: early_blight_on_tomato,
    type: fungal_disease,
    scientific_name: 'Alternaria solani',
    symptoms: [dark_concentrically_ringed_spots_on_lower_leaves, spots_near_stem_on_green_fruit],
    monitoring: [check_lower_leaves_for_ringed_spots],
    action_threshold: '',
    controls: [spray_copper_or_sulfur, spray_transplants_with_antitranspirant, plant_resistant_cultivars],
    cultural_context: [also_known_as_alternaria_blight, occurs_when_plants_loaded_with_fruit_and_during_warm_humid_weather_75_to_85_f]
]).

frame(disease, [
    name: septoria_leaf_spot,
    type: fungal_disease,
    scientific_name: '',
    symptoms: [circular_dark_spots_with_light_centers_peppered_with_dark_specks],
    monitoring: [check_older_leaves_first_for_symptoms],
    action_threshold: '',
    controls: [spray_copper, spray_transplants_with_antitranspirant],
    cultural_context: [fungal_disease_favoring_humid_conditions]
]).

frame(disease, [
    name: anthracnose_on_tomato,
    type: fungal_disease,
    scientific_name: '',
    symptoms: [concentrically_ringed_sunken_spots_on_ripe_fruit, fruit_rot],
    monitoring: [check_ripe_fruit_for_sunken_spots],
    action_threshold: '',
    controls: [keep_plants_dry_when_watering, pick_fruit_promptly, spray_copper_when_first_fruit_develops],
    cultural_context: [more_severe_on_overripe_fruit]
]).

frame(disease, [
    name: damping_off,
    type: fungal_disease,
    scientific_name: '',
    symptoms: [seedlings_fall_over, stems_girdled_or_rotted_at_soil_line],
    monitoring: [check_seedlings_daily],
    action_threshold: '',
    controls: [disinfect_pots_and_flats_with_bleach_solution, use_fresh_seed_starting_mix, sow_seed_thinly, keep_soil_moist_not_soggy, thin_seedlings, spray_with_compost_tea_when_first_true_leaves_appear],
    cultural_context: [common_fungal_disease_of_seedlings]
]).

% Tomato Physiological Disorders
frame(physiological_disorder, [
    name: blossom_end_rot,
    type: nutrient_disorder,
    symptoms: [black_sunken_area_at_blossom_end_of_fruit],
    monitoring: [check_developing_fruit_especially_first_fruit_to_ripen],
    action_threshold: '',
    controls: [maintain_even_soil_moisture, add_calcium_to_soil_if_deficient, spray_plants_with_seaweed_extract_when_first_flowers_open],
    cultural_context: [caused_by_calcium_deficiency_in_fruit, aggravated_by_drought_uneven_moisture_root_damage_high_salt_excess_nitrogen]
]).

frame(physiological_disorder, [
    name: sunscald,
    type: environmental_disorder,
    symptoms: [large_faded_or_gray_white_sunken_patches_on_fruit],
    monitoring: [check_exposed_fruit],
    action_threshold: '',
    controls: [control_leaf_diseases_to_prevent_defoliation],
    cultural_context: [affects_both_green_and_ripe_fruit_exposed_to_direct_sun]
]).

frame(physiological_disorder, [
    name: graywall,
    type: physiological_disorder,
    symptoms: [uneven_ripening, grayish_yellow_blotches_on_fruit, green_or_brown_areas_in_interior],
    monitoring: [check_ripening_fruit],
    action_threshold: '',
    controls: [ensure_good_growing_conditions],
    cultural_context: [caused_by_dense_shade_cool_temperatures_wet_soil_excess_nitrogen_potassium_deficiency_or_diseases]
]).

frame(physiological_disorder, [
    name: fruit_cracking,
    type: physiological_disorder,
    symptoms: [cracks_around_fruit_stems, semicircular_splits_on_shoulders],
    monitoring: [check_fruit_especially_after_rainfall_following_dry_period],
    action_threshold: '',
    controls: [keep_soil_evenly_moist, plant_crack_resistant_cultivars],
    cultural_context: [caused_by_uneven_irrigation, rots_may_invade_through_cracks]
]).

frame(physiological_disorder, [
    name: cat_facing,
    type: physiological_disorder,
    symptoms: [gnarled_malformed_fruit_with_dry_scars_near_blossom_end],
    monitoring: [check_early_fruit],
    action_threshold: '',
    controls: [protect_plants_with_row_cover_until_nights_remain_above_55_f],
    cultural_context: [caused_by_prolonged_cool_weather_during_blossoming, may_involve_poor_pollination]
]).

frame(physiological_disorder, [
    name: walnut_wilt,
    type: environmental_disorder,
    symptoms: [sudden_wilting_and_death_of_plants],
    monitoring: [note_proximity_to_black_walnut_trees],
    action_threshold: '',
    controls: [plant_tomatoes_at_least_50_feet_from_walnut_trees, grow_in_containers_with_good_potting_mix_if_necessary],
    cultural_context: [caused_by_toxic_compound_from_black_walnut_roots, toxin_remains_in_soil_for_years_after_trees_removed]
]).

% Tomato Cultural Practices
frame(practice, [
    name: tomato_seed_treatment,
    type: cultural_control,
    controls: [],
    resolves: [seed_borne_diseases],
    description: 'Soak tomato seeds in 10% bleach solution (1 part bleach, 9 parts water) for 10 minutes and rinse in clean water before planting to reduce seed-borne diseases.',
    cost: low,
    difficulty: low,
    season: [pre_planting],
    cultural_context: [helps_prevent_tobacco_mosaic_virus_fusarium_verticillium_bacterial_canker]
]).

frame(practice, [
    name: tomato_transplanting_boost,
    type: cultural_control,
    controls: [],
    resolves: [transplant_shock, nutrient_deficiencies],
    description: 'Add 1 cup each of bonemeal and kelp to each planting hole, water thoroughly with fish emulsion or compost tea, and spray young plants with seaweed extract.',
    cost: low,
    difficulty: low,
    season: [transplanting],
    cultural_context: [encourages_strong_healthy_growth]
]).

frame(practice, [
    name: tomato_mulching,
    type: cultural_control,
    controls: [disease_spread_from_soil],
    resolves: [soil_moisture_fluctuations, weed_competition],
    description: 'Mulch tomato plants to conserve water, suppress weeds, and prevent disease by keeping fruit from touching soil. Use black plastic in cool areas and organic mulch in warm areas.',
    cost: low,
    difficulty: low,
    season: [growing_season],
    cultural_context: [helps_prevent_blossom_end_rot_fruit_cracking_various_diseases]
]).

frame(practice, [
    name: tomato_crop_rotation,
    type: cultural_control,
    controls: [soil_borne_diseases, pest_buildup],
    resolves: [],
    description: 'Do not plant tomatoes where tomatoes, potatoes, eggplants, or peppers have been planted within the past 3-5 years.',
    cost: low,
    difficulty: medium,
    season: [planning],
    cultural_context: [prevents_disease_buildup_in_soil]
]).

frame(practice, [
    name: tomato_season_end_cleanup,
    type: cultural_control,
    controls: [overwintering_pests, disease_carryover],
    resolves: [],
    description: 'Compost or till under all plant residues at the end of the season and spread 2-4 pounds of bloodmeal or soybean meal per 100 square feet to encourage rapid breakdown.',
    cost: low,
    difficulty: low,
    season: [post_harvest],
    cultural_context: [reduces_pest_and_disease_pressure_for_next_season]
]). 
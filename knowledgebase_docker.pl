% ========================
% FARMLORE KNOWLEDGE BASE
% ========================
% This is a fixed version of the knowledgebase.pl file with syntax errors corrected
% All // comments are replaced with % comments
% All other syntax errors have been fixed

% ========================
% FRAME STRUCTURE DEFINITION
% ========================

% frame(FrameType, [slot:value, ...]).
% Common frame types:
% - pest: insect, disease, weed, etc. that affects crops
% - practice: cultural practice for pest management
% - crop: plant variety with associated information
% - etc.

% ========================
% PESTS
% ========================

% Sample pest frame structure
frame(pest, [
    name: leafhopper_general,
    type: insect,
    scientific_name: 'Cicadellidae spp.', % Family for leafhoppers
    symptoms: [vector_for_aster_yellows, general_leaf_damage, may_cause_stunting_or_yellowing],
    monitoring: [visual_inspection, sticky_traps],
    action_threshold: '',
    controls: [isopropyl_alcohol_soap_spray, row_covers, insecticidal_soap, neem_extract, pyrethrin],
    cultural_context: [global]
]).

frame(pest, [
    name: plant_bug_general,
    type: insect,
    scientific_name: '', 
    symptoms: [leaves_spotted, buds_wilted_and_dark],
    monitoring: [],
    action_threshold: '',
    controls: [handpicking, pyrethrin_dust],
    cultural_context: [global]
]).

frame(pest, [
    name: leaf_roller_general,
    type: insect, 
    scientific_name: '', 
    symptoms: [leaf_edges_webbed_together, feeding_on_enclosed_leaves_and_buds],
    monitoring: [],
    action_threshold: '',
    controls: [handpicking_leaf_rollers, btk],
    cultural_context: [global]
]).

frame(pest, [
    name: aphid_general,
    type: insect,
    scientific_name: 'Aphidoidea spp.',  % General aphid superfamily
    symptoms: [
        leaves_stems_buds_distorted, blossom_and_leaf_drop, sticky_honeydew_excretion, 
        leaves_curled_and_yellow, plant_stunted,  % Cabbage symptoms
        can_transmit_viruses, fluffy_coated_appearance_possible, % General aphid characteristic
        leaves_yellow_and_curled_on_corn, plant_stunted_on_corn, % Corn symptoms
        cucumber_leaves_yellow_curled_wilted % Cucumber symptoms
    ],
    monitoring: [visual_inspection, yellow_sticky_traps_for_winged_aphids],
    action_threshold: '', % Varies greatly
    controls: [strong_jets_of_water, encourage_natural_predators_and_parasites, insecticidal_soap, pyrethrin, release_lady_beetles, neem_extract, flowering_strips, weak_insecticidal_soap_spray_for_aphids_on_cucumbers, foil_mulch_for_aphids_on_cucumbers],
    cultural_context: [global]
]).

frame(pest, [
    name: cutworm_general,
    type: insect, 
    scientific_name: '', 
    symptoms: [seedlings_or_young_plants_cut_off_at_soil_level, seedlings_cut_off_at_ground_level, leaf_margins_ragged],
    monitoring: [],
    action_threshold: '',
    controls: [cutworm_collars, parasitic_nematodes_for_cutworms, spray_btk_in_evening_for_cutworms, sprinkle_moist_bran_with_btk_for_cutworms],
    cultural_context: [global]
]).

frame(pest, [
    name: mealybug_general,
    type: insect,
    scientific_name: '', 
    symptoms: [white_cottony_clusters_on_leaves_stems, plant_wilts, unhealthy_plant_appearance, honeydew_secretion],
    monitoring: [],
    action_threshold: '',
    controls: [strong_jets_of_water, insecticidal_soap],
    cultural_context: [global]
]).

frame(pest, [
    name: root_knot_nematode_on_bean,
    type: nematode,
    scientific_name: 'Meloidogyne spp.', 
    symptoms: [swollen_and_darkened_enlargements_of_roots, plant_yellow_and_stunted_wilts_hot_days_recovers_night],
    monitoring: [root_examination],
    action_threshold: '',
    controls: [discard_infected_plants, apply_chitin_to_soil, apply_parasitic_nematodes_to_soil],
    cultural_context: [global]
]).

% ========================
% CROPS (Original + PDF Enhanced)
% ========================
frame(crop, [
    name: tomato,
    pests: [tuta_absoluta, whiteflies, nematodes],
    diseases: [early_blight, verticillium_wilt],
    resistant_cultivars: [
        cv('Gloria F1', [resistance_to:nematodes]),
        cv('Maxifort', [rootstock:nematode_resistant])
    ],
    cultural_context: [global]
]).

frame(crop, [
    name: apple,
    pests: [codling_moth, aphid],
    diseases: [fire_blight, powdery_mildew],
    resistant_cultivars: [
        cv('Liberty', [resistance_to:fire_blight]),
        cv('GoldRush', [resistance_to:powdery_mildew])
    ],
    cultural_context: [temperate]
]).

frame(crop, [
    name: fir,
    pests: [balsam_twig_aphid, spruce_spider_mite, hemlock_looper, spruce_budworm, bagworm],
    diseases: [],
    resistant_cultivars: [],
    cultural_context: [temperate]
]).

frame(crop, [
    name: maple,
    pests: [maple_scale, mite_on_maple, boxelder_bug, caterpillar_on_maple, aphid_on_maple, borer_on_maple],
    diseases: [leaf_scorch, anthracnose, powdery_mildew, leaf_spot, verticillium_wilt, canker],
    resistant_cultivars: [],
    cultural_context: [temperate]
]).

frame(crop, [
    name: achillea,
    pests: [],
    diseases: [powdery_mildew_on_achillea],
    resistant_cultivars: [],
    cultural_context: [global]
]).

frame(crop, [
    name: aesculus,
    pests: [whitemarked_tussock_moth, japanese_beetle_on_aesculus, bagworm_on_aesculus],
    diseases: [leaf_blotch_on_aesculus, leaf_scorch, powdery_mildew_on_aesculus, anthracnose_on_aesculus, canker_on_aesculus],
    resistant_cultivars: [],
    cultural_context: [global]
]).

frame(crop, [
    name: ageratum,
    pests: [whitefly_on_ageratum, spider_mite_on_ageratum],
    diseases: [fungal_wilt_on_ageratum],
    resistant_cultivars: [],
    cultural_context: [global]
]).

frame(crop, [
    name: ajuga,
    pests: [],
    diseases: [crown_and_root_rot_on_ajuga],
    resistant_cultivars: [],
    cultural_context: [global]
]).

frame(crop, [
    name: albizia,
    pests: [mimosa_webworm],
    diseases: [mimosa_wilt],
    resistant_cultivars: [],
    cultural_context: [global]
]).

frame(crop, [
    name: alcea,
    pests: [leaf_feeding_beetle_on_alcea, true_bug_on_alcea],
    diseases: [rust_on_alcea],
    resistant_cultivars: [stated_as_generally_available_for_rust],
    cultural_context: [global]
]).

frame(crop, [
    name: allium_ornamental,
    pests: [slug_and_snail_general, onion_thrips_on_allium],
    diseases: [],
    resistant_cultivars: [],
    cultural_context: [global]
]).

frame(crop, [
    name: almond,
    pests: [squirrel_and_other_animal_pests_on_almond, oriental_fruit_moth_on_almond, peach_twig_borer_on_almond],
    diseases: [brown_rot_on_almond, shothole_disease_on_almond],
    resistant_cultivars: [cv('Archedoise', [resistance_to:'fungal_diseases'])],
    cultural_context: [zone_6_to_9, hot_dry_summers]
]).

frame(crop, [
    name: amaranthus,
    pests: [],
    diseases: [root_rot_on_amaranthus_due_to_overwatering],
    resistant_cultivars: [],
    cultural_context: [hot_dry_sunny_areas, poor_to_average_soil]
]).

% ========================
% UTILITY PREDICATES
% ========================

% Find a frame by name
find_frame(FrameType, Name, Frame) :-
    frame(FrameType, Frame),
    member(name:Name, Frame).

% Find effective controls for a pest
effective_against(Control, Pest) :-
    frame(pest, Frame),
    member(name:Pest, Frame),
    member(controls:Controls, Frame),
    member(Control, Controls).

% Find pests that affect a crop
affects(Pest, Crop) :-
    frame(crop, Frame),
    member(name:Crop, Frame),
    member(pests:Pests, Frame),
    member(Pest, Pests).

% Find diseases that affect a crop
susceptible_to(Crop, Disease) :-
    frame(crop, Frame),
    member(name:Crop, Frame),
    member(diseases:Diseases, Frame),
    member(Disease, Diseases).

% Find resistant cultivars for a crop
resistant_cultivar(Crop, Cultivar, Resistance) :-
    frame(crop, Frame),
    member(name:Crop, Frame),
    member(resistant_cultivars:Cultivars, Frame),
    member(cv(Cultivar, Properties), Cultivars),
    member(resistance_to:Resistance, Properties). 
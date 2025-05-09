% ========================
% FRAME TEMPLATES
% ========================
frame(practice, [
    name: atom,
    type: atom,
    controls: list(atom),
    resolves: list(atom),
    description: string,
    cost: atom,
    difficulty: atom,
    season: list(atom),
    cultural_context: list(atom)
]).

frame(pest, [
    name: atom,
    type: atom,
    scientific_name: string,
    symptoms: list(atom),
    monitoring: list(atom),
    action_threshold: term,
    controls: list(atom),
    cultural_context: list(atom)
]).

frame(crop, [
    name: atom,
    pests: list(atom),
    diseases: list(atom),
    resistant_cultivars: list(term),
    cultural_context: list(atom)
]).

% ========================
% TAXONOMY & ONTOLOGY
% ========================
% Control Type Hierarchy
subclass(pest_control, strategy).
subclass(cultural_control, pest_control).
subclass(biological_control, pest_control).
subclass(organic_pesticide, pest_control).
subclass(microbial_control, biological_control).
subclass(mineral_repellent, pest_control).

% Pest Type Hierarchy
subclass(insect, pest).
subclass(nematode, pest).
subclass(arachnid, pest).
subclass(lepidoptera, insect).
subclass(coleoptera, insect).
subclass(diptera, insect).

% Regional Hierarchy
subclass(region, top).
subclass(african, region).
subclass(european, region).
subclass(mediterranean, region).
subclass(tropical, region).
subclass(basotho, african).

% ========================
% ORIGINAL PRACTICES (Standardized)
% ========================
% Soil Management
frame(practice, [
    name: composting,
    type: soil_fertility,
    resolves: [low_fertility, poor_organic_matter],
    description: 'Decompose organic matter to enrich soil',
    cost: low,
    difficulty: low,
    season: [year_round],
    cultural_context: [basotho, global]
]).

frame(practice, [
    name: contour_plowing,
    type: soil_conservation,
    resolves: [soil_erosion, water_runoff],
    description: 'Plow along contours to prevent erosion',
    cost: low,
    difficulty: medium,
    season: [pre_planting],
    cultural_context: [basotho]
]).

% Pest Controls
frame(practice, [
    name: neem_extract,
    type: organic_pesticide,
    controls: [aphids, whiteflies, spider_mites],
    description: 'Azadirachtin from neem seeds disrupts insect growth',
    cost: medium,
    difficulty: medium,
    season: [growing_season],
    cultural_context: [global]
]).

frame(practice, [
    name: basalt_flour,
    type: mineral_repellent,
    controls: [slugs, snails],
    description: 'Alters soil pH and creates hostile environment for pests',
    cost: low,
    difficulty: low,
    season: [early_season],
    cultural_context: [basotho, european]
]).

% Physical/Mechanical Controls
frame(practice, [
    name: diatomaceous_earth,
    type: physical_control,
    controls: [slugs, beetles],
    description: 'Mechanical insecticide damaging exoskeletons',
    cost: medium,
    difficulty: low,
    season: [dry_season],
    cultural_context: [global]
]).

frame(practice, [
    name: row_covers,
    type: physical_control,
    controls: [flea_beetles, cabbage_moths],
    description: 'Physical barrier against flying pests',
    cost: high,
    difficulty: medium,
    season: [early_season],
    cultural_context: [global]
]).

% Biological Controls
frame(practice, [
    name: release_lady_beetles,
    type: biological_control,
    controls: [aphids],
    description: 'Predatory beetles for aphid control',
    cost: high,
    difficulty: high,
    season: [spring],
    cultural_context: [global]
]).

% ========================
% PDF-INTEGRATED PRACTICES
% ========================
frame(practice, [
    name: beetle_banks,
    type: biodiversity_enhancement,
    controls: [general_pest_suppression],
    description: 'Raised grassy strips for predatory insects',
    cost: low,
    difficulty: medium,
    season: [perennial],
    cultural_context: [european]
]).

frame(practice, [
    name: flowering_strips,
    type: biodiversity_enhancement,
    controls: [aphids, cabbage_moth],
    description: 'Fagopyrum esculentum/Centaurea cyanus planting',
    cost: medium,
    difficulty: high,
    season: [growing_season],
    cultural_context: [global]
]).

% ========================
% ORIGINAL PESTS (Enhanced)
% ========================
frame(pest, [
    name: wireworm,
    type: insect,
    scientific_name: 'Elateridae',
    symptoms: [tunneling_in_roots, wilted_seedlings],
    monitoring: [bait_traps],
    action_threshold: '5_larvae_per_trap',
    controls: [crop_rotation, entomopathogenic_nematodes],
    cultural_context: [global]
]).

frame(pest, [
    name: tuta_absoluta,
    type: lepidoptera,
    scientific_name: 'Tuta absoluta',
    symptoms: [leaf_mines, fruit_damage],
    monitoring: [pheromone_traps],
    action_threshold: '2_moths_per_trap',
    controls: [beauveria_bassiana, trichogramma_wasps],
    cultural_context: [global]
]).

% ========================
% PDF-INTEGRATED PESTS
% ========================
frame(pest, [
    name: nasonovia_ribisnigri,
    type: insect,
    scientific_name: 'Nasonovia ribisnigri',
    symptoms: [heart_damage, virus_transmission],
    monitoring: [visual_inspection],
    action_threshold: '10_aphids_per_plant',
    controls: [neem_oil, resistant_cultivars],
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

% ========================
% VALIDATION SYSTEM
% ========================
:- frame(pest, Pest), 
   (   member(scientific_name:_, Pest)
   ->  true
   ;   format('Validation Error: Missing scientific_name for ~w~n', [Pest]), fail).

:- frame(practice, Practice),
   member(controls:Controls, Practice),
   forall(member(Control, Controls),
     (   pest(name:Control, _)
     ->  true
     ;   format('Validation Error: Undefined pest ~w in practice ~w~n', [Control, Practice]), fail
     )).

% ========================
% REASONING ENGINE
% ========================
% IPM Priority Recommendation
recommend_solution(Pest, Solution) :-
    practice(name:Solution, type:cultural_control, controls:Controls, cultural_context:Ctx),
    member(Pest, Controls), !.

recommend_solution(Pest, Solution) :-
    practice(name:Solution, type:biological_control, controls:Controls, cultural_context:Ctx),
    member(Pest, Controls), !.

recommend_solution(Pest, Solution) :-
    practice(name:Solution, type:organic_pesticide, controls:Controls, cultural_context:Ctx),
    member(Pest, Controls), !.

% Threshold-Based Intervention
current_pest_count(tuta_absoluta, tomato, 3). % Sample dynamic data

intervention_needed(Pest, Crop) :-
    pest(name:Pest, action_threshold:Threshold),
    current_pest_count(Pest, Crop, Count),
    Count >= Threshold.

% ========================
% HELPER PREDICATES
% ========================
contains(List, Item) :- member(Item, List).

pest_solutions(Pest, Region, Solutions) :-
    findall(Sol, (
        practice(name:Sol, controls:Controls, cultural_context:Ctx),
        contains(Controls, Pest),
        contains(Ctx, Region)
    ), Solutions).

% ========================
% EXAMPLE QUERIES
% ========================
% ?- recommend_solution(tuta_absoluta, Solution).
% Solution = beauveria_bassiana

% ?- pest_solutions(aphid, european, Solutions).
% Solutions = [neem_extract, release_lady_beetles]

% ?- intervention_needed(tuta_absoluta, tomato).
% true

% ========================
% INCLUDE INDIGENOUS KNOWLEDGE
% ========================
:- include('indigenous_kb.pl').

% Include community knowledge base
:- include('community_kb.pl').

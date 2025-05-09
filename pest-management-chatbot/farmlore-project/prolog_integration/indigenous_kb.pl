% ========================
% INDIGENOUS KNOWLEDGE BASE
% ========================
% This file contains Basotho indigenous farming knowledge structured to integrate
% with the main knowledge base using the frame-based representation.

% ========================
% INDIGENOUS PRACTICES
% ========================
frame(practice, [
    name: ash_application,
    type: pest_control,
    controls: [aphids, spider_mites],
    description: 'Collecting wood ash from cooking fires and applying it to crops to repel insects. The ash creates a barrier that insects do not like to cross.',
    cost: low,
    difficulty: low,
    materials: ['wood ash', 'container for collecting ash'],
    season: [growing_season],
    cultural_context: [basotho],
    source: 'Ntate Thabo from Maseru',
    verification_count: 5
]).

frame(practice, [
    name: chili_pepper_spray,
    type: pest_control,
    controls: [tomato_hornworm, aphids],
    description: 'Crushing hot chili peppers and mixing with water to create a natural insect repellent. The capsaicin in chilies deters many pests without harming the plants.',
    cost: low,
    difficulty: medium,
    materials: ['hot chili peppers', 'water', 'container for mixing', 'spray bottle'],
    season: [growing_season],
    cultural_context: [basotho],
    source: 'Ntate Thabo from Maseru',
    verification_count: 4
]).

frame(practice, [
    name: marigold_companion_planting,
    type: pest_control,
    controls: [nematodes, aphids],
    description: 'Planting marigolds alongside vegetables to repel nematodes and other soil pests. The roots of marigolds release compounds that are toxic to certain soil pests.',
    cost: low,
    difficulty: low,
    materials: ['marigold seeds', 'garden tools'],
    season: [planting_season],
    cultural_context: [basotho],
    source: 'Ntate Mohau from Butha-Buthe',
    verification_count: 6
]).

frame(practice, [
    name: kraal_manure_fertilization,
    type: soil_fertility,
    resolves: [low_fertility, poor_organic_matter],
    description: 'Using cattle kraal manure to fertilize soil before planting. The manure improves soil structure, adds nutrients, and increases water retention.',
    cost: low,
    difficulty: medium,
    materials: ['aged cattle manure', 'tools for spreading'],
    season: [pre_planting],
    cultural_context: [basotho],
    source: 'Mme Lineo from Leribe',
    verification_count: 7
]).

frame(practice, [
    name: aloe_vera_spray,
    type: disease_management,
    controls: [fungal_diseases],
    description: 'Using aloe vera gel to treat fungal diseases on crops. The aloe gel has natural antifungal properties and helps plants recover from disease stress.',
    cost: low,
    difficulty: medium,
    materials: ['fresh aloe vera leaves', 'knife', 'container for mixing', 'spray bottle'],
    season: [growing_season],
    cultural_context: [basotho],
    source: 'Mme Lineo from Leribe',
    verification_count: 3
]).

% ========================
% ECOLOGICAL INDICATORS
% ========================
frame(ecological_indicator, [
    name: peach_flowering,
    description: 'Early flowering of peach trees',
    region: leribe,
    interpretation: 'When peach trees flower unusually early, it indicates that the coming season will have irregular rainfall patterns.',
    recommended_action: 'Plant drought-resistant crop varieties and implement water conservation techniques.',
    cultural_context: [basotho]
]).

frame(ecological_indicator, [
    name: grasshopper_abundance,
    description: 'Abundance of grasshoppers in early spring',
    region: maseru,
    interpretation: 'Large numbers of grasshoppers in early spring indicate a hot, dry summer ahead.',
    recommended_action: 'Prepare for drought conditions by selecting drought-tolerant crops and implementing water conservation methods.',
    cultural_context: [basotho]
]).

% ========================
% SESOTHO TERMINOLOGY
% ========================
frame(sesotho_term, [
    term: molora,
    english: ash,
    description: 'Used in pest control and as fertilizer',
    cultural_context: [basotho]
]).

frame(sesotho_term, [
    term: likokonyana,
    english: insects,
    description: 'General term for pests',
    cultural_context: [basotho]
]).

frame(sesotho_term, [
    term: moiteli,
    english: manure,
    description: 'Used for soil fertilization',
    cultural_context: [basotho]
]).

frame(sesotho_term, [
    term: lekhala,
    english: aloe_vera,
    description: 'Used for treating plant diseases',
    cultural_context: [basotho]
]).

frame(sesotho_term, [
    term: masimo,
    english: fields,
    description: 'Agricultural land',
    cultural_context: [basotho]
]).

% ========================
% HELPER PREDICATES
% ========================
% Find indigenous practices for controlling a specific pest
indigenous_practice_for_pest(Pest, Practice) :-
    practice(name:Practice, controls:Controls, cultural_context:Context),
    member(basotho, Context),
    member(Pest, Controls).

% Find indigenous practices for a specific crop
indigenous_practice_for_crop(Crop, Practice) :-
    practice(name:Practice, applicable_crops:Crops, cultural_context:Context),
    member(basotho, Context),
    member(Crop, Crops).

% Find verified indigenous practices (verification count >= 3)
verified_indigenous_practice(Practice) :-
    practice(name:Practice, verification_count:Count, cultural_context:Context),
    member(basotho, Context),
    Count >= 3.

% Find all indigenous practices by type
indigenous_practices_by_type(Type, Practices) :-
    findall(Practice, (
        practice(name:Practice, type:Type, cultural_context:Context),
        member(basotho, Context)
    ), Practices).

% Find ecological indicators for a region
ecological_indicators_for_region(Region, Indicators) :-
    findall(Indicator, (
        ecological_indicator(name:Indicator, region:Region, cultural_context:Context),
        member(basotho, Context)
    ), Indicators).

% Integrated queries that combine conventional and indigenous knowledge
all_practices_for_pest(Pest, AllPractices) :-
    findall(practice(Name, conventional), (
        practice(name:Name, controls:Controls, cultural_context:Ctx),
        \+ member(basotho, Ctx),
        member(Pest, Controls)
    ), ConventionalPractices),
    findall(practice(Name, indigenous), (
        practice(name:Name, controls:Controls, cultural_context:Ctx),
        member(basotho, Ctx),
        member(Pest, Controls)
    ), IndigenousPractices),
    append(ConventionalPractices, IndigenousPractices, AllPractices).

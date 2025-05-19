% ========================
% ADVANCED QUERY INTERFACE FOR FARMLORE KNOWLEDGE BASE
% ========================
% This file implements a more robust query interface for the 
% pest management knowledge base with natural language processing
% capabilities and integrated reasoning across multiple domains.

% Load required knowledge bases directly instead of via load_all.pl to avoid circular dependencies
:- consult(knowledgebase).
:- consult(insect_reference).
:- consult(plant_disease_reference).
:- consult(crop_updates).
:- consult(pea_updates).
:- consult(control_methods).
:- consult(organic_sprays).

% ========================
% 1. NATURAL LANGUAGE QUERY INTERFACE
% ========================

% Process natural language queries by identifying key terms
process_query(Query, Response) :-
    tokenize_query(Query, Terms),
    identify_query_intent(Terms, Intent),
    execute_query(Intent, Response).

% Simple tokenizer for natural language queries
tokenize_query(Query, Terms) :-
    downcase_atom(Query, LowerQuery),
    atomic_list_concat(Words, ' ', LowerQuery),
    exclude(stop_word, Words, FilteredWords),
    extract_key_terms(FilteredWords, Terms).

% Common stop words to filter out
stop_word(X) :- member(X, ['a','an','the','is','are','how','to','can','do','what',
                          'for','in','of','on','with','about','and','or','my']).

% Extract key terms from the tokenized input
extract_key_terms([], []).
extract_key_terms([Word|Words], [Term|Terms]) :-
    map_to_term(Word, Term), !,
    extract_key_terms(Words, Terms).
extract_key_terms([_|Words], Terms) :-
    extract_key_terms(Words, Terms).

% Map common words to knowledge base terms
map_to_term(Word, Term) :-
    synonym_mapping(Word, Term).

% Synonym mappings for common terms
synonym_mapping('insects', pest).
synonym_mapping('pests', pest).
synonym_mapping('bugs', pest).
synonym_mapping('aphids', aphids).
synonym_mapping('caterpillars', caterpillars).
synonym_mapping('beetles', beetles).
synonym_mapping('mites', spider_mites).
synonym_mapping('disease', disease).
synonym_mapping('diseases', disease).
synonym_mapping('blight', blight).
synonym_mapping('mildew', mildew).
synonym_mapping('powdery', powdery_mildew).
synonym_mapping('downy', downy_mildew).
synonym_mapping('control', control).
synonym_mapping('treat', control).
synonym_mapping('remedy', control).
synonym_mapping('fix', control).
synonym_mapping('solve', control).
synonym_mapping('prevent', prevention).
synonym_mapping('stop', prevention).
synonym_mapping('avoid', prevention).
synonym_mapping('organic', organic).
synonym_mapping('natural', organic).
synonym_mapping('spray', spray).
synonym_mapping('dust', dust).
synonym_mapping('sprays', spray).
synonym_mapping('dusts', dust).
synonym_mapping('beneficial', beneficial).
synonym_mapping('helpers', beneficial).
synonym_mapping('attract', attract).
synonym_mapping('bring', attract).
synonym_mapping('encourage', attract).
synonym_mapping('tomatoes', tomato).
synonym_mapping('tomato', tomato).
synonym_mapping('potatoes', potato).
synonym_mapping('potato', potato).
synonym_mapping('beans', bean).
synonym_mapping('peas', pea).
synonym_mapping('roses', rose).
synonym_mapping('rose', rose).
synonym_mapping('summer', summer).
synonym_mapping('winter', winter).
synonym_mapping('spring', spring).
synonym_mapping('fall', fall).
synonym_mapping('autumn', fall).

% Identify query intent based on extracted terms
identify_query_intent(Terms, pest_control(Pest)) :-
    member(pest, Terms),
    member(control, Terms),
    member(Pest, Terms),
    is_pest(Pest), !.

identify_query_intent(Terms, disease_control(Disease)) :-
    member(disease, Terms),
    member(control, Terms),
    member(Disease, Terms),
    is_disease(Disease), !.

identify_query_intent(Terms, crop_pests(Crop)) :-
    member(Crop, Terms),
    member(pest, Terms),
    is_crop(Crop), !.

identify_query_intent(Terms, crop_diseases(Crop)) :-
    member(Crop, Terms),
    member(disease, Terms),
    is_crop(Crop), !.

identify_query_intent(Terms, beneficial_attractions) :-
    member(beneficial, Terms),
    member(attract, Terms), !.

identify_query_intent(Terms, seasonal_pests(Season)) :-
    member(Season, Terms),
    member(pest, Terms),
    is_season(Season), !.

identify_query_intent(Terms, organic_controls) :-
    member(organic, Terms),
    member(control, Terms), !.

identify_query_intent(Terms, spray_safety) :-
    (member(spray, Terms); member(dust, Terms)),
    member(safety, Terms), !.

identify_query_intent(_, general_help).

% Predicates to check if a term is a valid entity in our knowledge base
is_pest(Pest) :- 
    (frame(specific_insect, [name:Pest, _, _]); 
     frame(general_insect, [name:Pest, _, _]);
     frame(mite, [name:Pest, _, _]);
     Pest = slugs).

is_disease(Disease) :- 
    frame(plant_disease, [name:Disease, _, _]).

is_crop(Crop) :- 
    (frame(crop, [name:Crop, _, _, _]); 
     Crop = tomato; 
     Crop = potato; 
     Crop = pea;
     Crop = bean;
     Crop = rose).

is_season(Season) :- 
    member(Season, [spring, summer, fall, winter]).

% Execute query based on identified intent
execute_query(pest_control(Pest), Response) :-
    findall(Method, effective_against(Method, Pest), Methods),
    format_response('Control methods for ~w:', [Pest], Intro),
    format_list(Methods, MethodList),
    string_concat(Intro, MethodList, Response).

execute_query(disease_control(Disease), Response) :-
    disease_controls(Disease, Methods),
    format_response('Control methods for ~w:', [Disease], Intro),
    format_list(Methods, MethodList),
    string_concat(Intro, MethodList, Response).

execute_query(crop_pests(Crop), Response) :-
    crop_pest_list(Crop, Pests),
    format_response('Pests affecting ~w:', [Crop], Intro),
    format_list(Pests, PestList),
    string_concat(Intro, PestList, Response).

execute_query(crop_diseases(Crop), Response) :-
    findall(Disease, susceptible_to(Crop, Disease), Diseases),
    format_response('Diseases affecting ~w:', [Crop], Intro),
    format_list(Diseases, DiseaseList),
    string_concat(Intro, DiseaseList, Response).

execute_query(beneficial_attractions, Response) :-
    findall(Method, is_attraction_method(Method), Methods),
    format_response('Methods to attract beneficial insects:', [], Intro),
    format_list(Methods, MethodList),
    string_concat(Intro, MethodList, Response).

execute_query(seasonal_pests(Season), Response) :-
    seasonal_pests(Season, Pests),
    format_response('Common pests in ~w:', [Season], Intro),
    format_list(Pests, PestList),
    string_concat(Intro, PestList, Response).

execute_query(organic_controls, Response) :-
    findall(Method, 
            (frame(organic_spray, [name:Method, _, _, _]) ; 
             frame(physical_control, [name:Method, _, _, _]) ;
             frame(biological_control, [name:Method, _, _, _])), 
            Methods),
    format_response('Organic control methods:', [], Intro),
    format_list(Methods, MethodList),
    string_concat(Intro, MethodList, Response).

execute_query(spray_safety, Response) :-
    (frame(spray_safety, [name:spray_safely, guidelines:Guidelines, _]) ->
        format_response('Spray safety guidelines:', [], Intro),
        format_numbered_list(Guidelines, GuidelinesList),
        string_concat(Intro, GuidelinesList, Response)
    ;
        Response = 'Safety information not found.'
    ).

execute_query(general_help, 'I can help with questions about pests, diseases, controls, and beneficial insects. Try asking about specific pests, crops, or control methods.').

% Helper for response formatting
format_response(Template, Args, Response) :-
    format(string(Response), Template, Args),
    string_concat(Response, '\n', Response).

% Format a list as a string with bullet points
format_list([], '').
format_list([Item|Items], FormattedList) :-
    format(string(ItemStr), '- ~w\n', [Item]),
    format_list(Items, RestList),
    string_concat(ItemStr, RestList, FormattedList).

% Format a numbered list
format_numbered_list(List, FormattedList) :-
    format_numbered_list(List, 1, FormattedList).

format_numbered_list([], _, '').
format_numbered_list([Item|Items], N, FormattedList) :-
    format(string(ItemStr), '~w. ~w\n', [N, Item]),
    N1 is N + 1,
    format_numbered_list(Items, N1, RestList),
    string_concat(ItemStr, RestList, FormattedList).

% ========================
% 2. MISSING QUERY TYPES
% ========================

% Crop rotation strategies
crop_rotation_for(Crop, RotationPlan) :-
    crop_family(Crop, Family),
    findall(OtherCrop, 
           (crop_family(OtherCrop, OtherFamily), 
            OtherFamily \= Family,
            compatible_rotation(Family, OtherFamily)),
           CompatibleCrops),
    rotation_sequence(Crop, CompatibleCrops, RotationPlan).

% Crop families for rotation planning
crop_family(tomato, nightshade).
crop_family(potato, nightshade).
crop_family(eggplant, nightshade).
crop_family(pepper, nightshade).
crop_family(carrot, umbelliferae).
crop_family(parsley, umbelliferae).
crop_family(celery, umbelliferae).
crop_family(dill, umbelliferae).
crop_family(bean, legume).
crop_family(pea, legume).
crop_family(cabbage, brassica).
crop_family(broccoli, brassica).
crop_family(kale, brassica).
crop_family(radish, brassica).
crop_family(lettuce, composite).
crop_family(sunflower, composite).
crop_family(cucumber, cucurbit).
crop_family(squash, cucurbit).
crop_family(melon, cucurbit).

% Compatible rotations between families
compatible_rotation(nightshade, legume).
compatible_rotation(nightshade, brassica).
compatible_rotation(legume, brassica).
compatible_rotation(legume, cucurbit).
compatible_rotation(brassica, umbelliferae).
compatible_rotation(cucurbit, umbelliferae).
compatible_rotation(umbelliferae, composite).
compatible_rotation(composite, legume).
compatible_rotation(composite, brassica).

% Create a rotation sequence
rotation_sequence(MainCrop, CompatibleCrops, [MainCrop, Year2, Year3, Year4]) :-
    length(CompatibleCrops, L), L >= 3,
    select_rotation_crop(CompatibleCrops, 1, Year2),
    select_rotation_crop(CompatibleCrops, 2, Year3),
    select_rotation_crop(CompatibleCrops, 3, Year4).

rotation_sequence(MainCrop, CompatibleCrops, [MainCrop, Year2, Year3, MainCrop]) :-
    length(CompatibleCrops, L), L >= 2,
    select_rotation_crop(CompatibleCrops, 1, Year2),
    select_rotation_crop(CompatibleCrops, 2, Year3).

rotation_sequence(MainCrop, CompatibleCrops, [MainCrop, Year2, MainCrop]) :-
    length(CompatibleCrops, L), L >= 1,
    select_rotation_crop(CompatibleCrops, 1, Year2).

% Select a rotation crop based on position
select_rotation_crop(Crops, N, Crop) :-
    nth_member(N, Crops, Crop), !.
select_rotation_crop(Crops, _, Crop) :-
    member(Crop, Crops).

% Helper to get the nth member of a list
nth_member(1, [X|_], X) :- !.
nth_member(N, [_|Xs], X) :- 
    N > 1, 
    N1 is N - 1, 
    nth_member(N1, Xs, X).

% Seasonal pest management
seasonal_pests(spring, [cutworms, aphids, flea_beetles, cabbage_maggots, slugs, snails]).
seasonal_pests(summer, [aphids, colorado_potato_beetles, japanese_beetles, tomato_hornworms, spider_mites, squash_bugs]).
seasonal_pests(fall, [aphids, cabbage_loopers, squash_bugs, cucumber_beetles, spider_mites]).
seasonal_pests(winter, [spider_mites, scale_insects, mealybugs]).

seasonal_management(Season, Pest, Plan) :-
    seasonal_pests(Season, Pests),
    member(Pest, Pests),
    seasonal_control_plan(Season, Pest, Plan).

% Season-specific management plans
seasonal_control_plan(spring, cutworms, [
    'Use cutworm collars around seedlings',
    'Keep garden free of debris',
    'Release beneficial nematodes',
    'Apply Bacillus thuringiensis (Bt) as needed'
]).

seasonal_control_plan(spring, aphids, [
    'Introduce lady beetles early in season',
    'Use yellow sticky traps for monitoring',
    'Apply insecticidal soap to infestations',
    'Plant trap crops like nasturtiums'
]).

seasonal_control_plan(summer, spider_mites, [
    'Increase humidity around plants with regular misting',
    'Release predatory mites',
    'Apply insecticidal soap or neem oil',
    'Remove heavily infested leaves'
]).

seasonal_control_plan(fall, cucumber_beetles, [
    'Remove all crop debris after harvest',
    'Till soil to expose overwintering adults',
    'Apply row covers to fall plantings',
    'Use trap crops like squash'
]).

seasonal_control_plan(winter, scale_insects, [
    'Apply dormant oil spray',
    'Prune affected branches',
    'Scrub scales off with soft brush',
    'Increase indoor humidity for houseplants'
]).

seasonal_control_plan(Season, Pest, [
    'Monitor regularly for early detection',
    'Implement appropriate organic controls',
    'Practice good sanitation'
]) :-
    seasonal_pests(Season, Pests),
    member(Pest, Pests).

% ========================
% 3. INTEGRATION ACROSS KNOWLEDGE AREAS
% ========================

% Integrated approach combining multiple control strategies
integrated_approach(Pest, Crop, Season, Approach) :-
    % Get physical controls
    findall(PhysMethod, 
           (effective_against(PhysMethod, Pest), 
            belongs_to(PhysMethod, physical_control)), 
           PhysMethods),
    
    % Get biological controls
    findall(BioMethod, 
           (effective_against(BioMethod, Pest), 
            belongs_to(BioMethod, biological_control)), 
           BioMethods),
    
    % Get organic sprays
    findall(SprayMethod, 
           (organic_sprays_for(Pest, AllSprays),
            member(SprayMethod, AllSprays)), 
           SprayMethods),
    
    % Get seasonal considerations
    (seasonal_control_plan(Season, Pest, SeasonalPlan) -> true ; SeasonalPlan = []),
    
    % Get crop-specific considerations
    (crop_specific_controls(Crop, Pest, CropSpecific) -> true ; CropSpecific = []),
    
    % Combine approaches with priority on least-toxic methods
    prioritize_methods(PhysMethods, BioMethods, SprayMethods, 
                      SeasonalPlan, CropSpecific, Approach).

% Prioritize methods from least toxic to most toxic
prioritize_methods(PhysMethods, BioMethods, SprayMethods, SeasonalPlan, CropSpecific, 
                  [cultural_practices:Cultural, physical_controls:PhysSelected, 
                   biological_controls:BioSelected, organic_sprays:SpraySelected]) :-
    % Select cultural practices from seasonal and crop-specific advice
    append(SeasonalPlan, CropSpecific, AllPractices),
    select_unique(AllPractices, Cultural),
    
    % Select up to 3 physical methods
    select_up_to_n(PhysMethods, 3, PhysSelected),
    
    % Select up to 2 biological methods
    select_up_to_n(BioMethods, 2, BioSelected),
    
    % Select only 1 spray method (least toxic)
    select_up_to_n(SprayMethods, 1, SpraySelected).

% Helper to select unique elements
select_unique(List, UniqueList) :-
    list_to_set(List, UniqueList).

% Helper to select up to N elements from a list
select_up_to_n(List, N, Selected) :-
    length(List, L),
    (L =< N -> Selected = List ; take_n(List, N, Selected)).

% Take first N elements of a list
take_n(_, 0, []) :- !.
take_n([], _, []) :- !.
take_n([X|Xs], N, [X|Ys]) :-
    N > 0,
    N1 is N - 1,
    take_n(Xs, N1, Ys).

% Crop-specific control methods
crop_specific_controls(tomato, aphids, [
    'Plant basil as a companion plant',
    'Use reflective mulch',
    'Prune lower leaves for air circulation'
]).

crop_specific_controls(potato, colorado_potato_beetle, [
    'Plant resistant varieties',
    'Use straw mulch to confuse beetles',
    'Practice crop rotation with non-nightshade crops',
    'Hand-pick beetles in small gardens'
]).

crop_specific_controls(pea, aphids, [
    'Use row covers until flowering',
    'Plant with companion plants like mint or chives',
    'Monitor during warm weather'
]).

% ========================
% 4. LOCATION AND GARDEN-SPECIFIC RECOMMENDATIONS
% ========================

% Climate zone based recommendations
climate_zone_control(Pest, Zone, Recommendations) :-
    pest_control_by_zone(Pest, Zone, Recommendations).

% Hardiness zone-specific pest control recommendations
pest_control_by_zone(aphids, Zone, ['Release beneficial insects early in season']) :-
    member(Zone, [3,4,5,6]), !.
pest_control_by_zone(aphids, Zone, ['Monitor carefully during hot, dry periods']) :-
    member(Zone, [7,8,9,10]), !.

pest_control_by_zone(spider_mites, Zone, ['Maintain humidity, use preventive methods']) :-
    member(Zone, [3,4,5,6]), !.
pest_control_by_zone(spider_mites, Zone, ['Regular miticide applications may be needed']) :-
    member(Zone, [7,8,9,10]), !.

pest_control_by_zone(_, _, ['Practice integrated pest management',
                          'Monitor regularly for early detection',
                          'Use multiple control strategies']).

% Garden size-based recommendations
garden_size_recommendations(small, [
    'Hand-picking pests is practical',
    'Individual plant treatment is feasible',
    'Row covers work well for small beds',
    'Focus on intensive preventive measures'
]).

garden_size_recommendations(medium, [
    'Combination of hand-picking and targeted sprays',
    'Beneficial insect releases can be effective',
    'Crop rotation is important',
    'Use trap crops strategically'
]).

garden_size_recommendations(large, [
    'Focus on ecosystem management',
    'Establish permanent beneficial insect habitats',
    'Use broad preventive cultural practices',
    'Consider timing of large-scale interventions carefully',
    'Divide garden into management sections'
]).

% Custom recommendation based on location, season, and garden size
custom_recommendation(Pest, Location, Season, GardenSize, Recommendation) :-
    % Get climate zone for location
    location_to_zone(Location, Zone),
    
    % Get zone-specific recommendations
    climate_zone_control(Pest, Zone, ZoneRecs),
    
    % Get seasonal recommendations
    (seasonal_control_plan(Season, Pest, SeasonRecs) -> true ; SeasonRecs = []),
    
    % Get size-based recommendations
    garden_size_recommendations(GardenSize, SizeRecs),
    
    % Combine all recommendations
    append(ZoneRecs, SeasonRecs, Temp),
    append(Temp, SizeRecs, AllRecs),
    select_unique(AllRecs, Recommendation).

% Simple mapping of locations to USDA hardiness zones
location_to_zone('New York', 6).
location_to_zone('Chicago', 5).
location_to_zone('Miami', 10).
location_to_zone('Phoenix', 9).
location_to_zone('Seattle', 8).
location_to_zone('Denver', 5).
location_to_zone('Boston', 6).
location_to_zone('Los Angeles', 10).
location_to_zone('Portland', 8).
location_to_zone('Minneapolis', 4).
location_to_zone(_, 6).  % Default to zone 6 if location unknown

% Helper predicate to check if something is an attraction method
is_attraction_method(Method) :-
    frame(beneficial_insect, [attraction_methods:Methods, _]),
    member(Method, Methods).

% Helper predicate for crop pests
crop_pest_list(Crop, Pests) :-
    findall(Pest, 
           (frame(specific_insect, [name:Pest, _]),
            affects_crop(Pest, Crop)), 
           DirectPests),
    (frame(crop, [name:Crop, pests:FramePests, _, _]) -> 
        append(DirectPests, FramePests, AllPests),
        sort(AllPests, Pests)
    ;
        sort(DirectPests, Pests)
    ).

% Helper predicate for disease controls
disease_controls(Disease, Controls) :-
    findall(Control, 
           (frame(plant_disease, [name:Disease, controls:DiseaseControls, _]),
            member(Control, DiseaseControls)), 
           DirectControls),
    findall(OtherControl, 
           (effective_against(OtherControl, Disease)), 
           IndirectControls),
    append(DirectControls, IndirectControls, AllControls),
    sort(AllControls, Controls).

% ========================
% EXAMPLE QUERY INTERFACE
% ========================

% Example of a natural language query
example_nl_query_1 :-
    Query = "How can I control aphids on my tomatoes in the summer?",
    write('Query: '), write(Query), nl,
    process_query(Query, Response),
    write('Response: '), nl, write(Response).

% Example of an integrated approach query
example_integrated_query :-
    integrated_approach(aphids, tomato, summer, Approach),
    write('Integrated approach for aphids on tomatoes in summer:'), nl,
    write_integrated_approach(Approach).

% Helper to write out integrated approach
write_integrated_approach([]) :- !.
write_integrated_approach([Category:Methods|Rest]) :-
    write(Category), write(':'), nl,
    format_list(Methods, MethodList),
    write(MethodList),
    write_integrated_approach(Rest).

% Example of a location-specific recommendation
example_location_query :-
    custom_recommendation(spider_mites, 'Phoenix', summer, medium, Recommendations),
    write('Custom recommendations for spider mites in Phoenix during summer in a medium garden:'), nl,
    format_list(Recommendations, RecList),
    write(RecList).

% Example of crop rotation query
example_rotation_query :-
    crop_rotation_for(tomato, Rotation),
    write('Crop rotation sequence for tomatoes:'), nl,
    write('Year 1: '), write(tomato), nl,
    write('Year 2: '), write(Rotation[1]), nl,
    write('Year 3: '), write(Rotation[2]), nl,
    write('Year 4: '), write(Rotation[3]), nl.

% Run examples when loaded
:- nl,
   write('Advanced query interface loaded.'), nl,
   write('Try running example_nl_query_1.'), nl. 
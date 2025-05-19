% ========================
% FARMLORE KNOWLEDGE BASE QUERY EXAMPLES
% ========================
% This file demonstrates how to query the integrated knowledge base

% Load all knowledge bases
:- consult(load_all).

% ========================
% EXAMPLE QUERIES
% ========================

% 1. Find all physical control methods for slugs
example_query_1 :-
    write('Example Query 1: Physical control methods for slugs'), nl,
    findall(Method, effective_against(Method, slugs), Methods),
    findall(PhysicalMethod, 
            (member(PhysicalMethod, Methods), belongs_to(PhysicalMethod, physical_control)), 
            PhysicalMethods),
    write('Physical control methods for slugs:'), nl,
    print_list(PhysicalMethods).

% 2. Find all pests controlled by floating row covers
example_query_2 :-
    write('Example Query 2: Pests controlled by floating row covers'), nl,
    pests_controlled_by(floating_row_covers, Pests),
    write('Pests controlled by floating row covers:'), nl,
    print_list(Pests).

% 3. Find materials needed for making crawling pest barriers
example_query_3 :-
    write('Example Query 3: Materials for crawling pest barriers'), nl,
    materials_for(crawling_pest_barriers, Materials),
    write('Materials needed for crawling pest barriers:'), nl,
    print_list(Materials).

% 4. Find all barrier-type physical controls
example_query_4 :-
    write('Example Query 4: Barrier-type physical controls'), nl,
    physical_controls_in_category(barrier, Controls),
    write('Barrier-type physical controls:'), nl,
    print_list(Controls).

% 5. Find all control methods effective against aphids
example_query_5 :-
    write('Example Query 5: Control methods for aphids'), nl,
    all_controls_for_pest(aphids, Controls),
    write('Control methods effective against aphids:'), nl,
    print_list(Controls).

% 6. Integrated query: Find control methods that work for pests affecting tomatoes
example_query_6 :-
    write('Example Query 6: Control methods for pests affecting tomatoes'), nl,
    (frame(crop, [name:tomato, pests:Pests, _, _]) -> true ; Pests = []),
    findall(TomatoPest, (frame(specific_insect, [name:Pest, _, _]), affects_crop(Pest, tomato)), MorePests),
    append(Pests, MorePests, AllPests),
    sort(AllPests, UniquePests),
    write('Pests affecting tomatoes:'), nl,
    print_list(UniquePests),
    write('Control methods for each pest:'), nl,
    process_pest_controls(UniquePests).

% 7. Integrated query: Find physical controls for diseases affecting roses
example_query_7 :-
    write('Example Query 7: Physical controls for diseases affecting roses'), nl,
    findall(Disease, susceptible_to(rose, Disease), Diseases),
    write('Diseases affecting roses:'), nl,
    print_list(Diseases),
    write('Physical control methods for each disease:'), nl,
    process_disease_controls(Diseases).

% NEW QUERIES FOR BIOLOGICAL CONTROL

% 8. Find all biological control methods 
example_query_8 :-
    write('Example Query 8: All biological control methods'), nl,
    control_methods_by_category(biological_control, Methods),
    write('Biological control methods:'), nl,
    print_list(Methods).

% 9. Find biological controls for caterpillars
example_query_9 :-
    write('Example Query 9: Biological controls for caterpillars'), nl,
    findall(Method, 
            (controls(Method, caterpillars), 
             belongs_to(Method, biological_control)), 
            Methods),
    write('Biological controls for caterpillars:'), nl,
    print_list(Methods),
    (Methods = [] -> 
        write('No specific controls found') 
    ;
        write('Details of most effective method:'), nl,
        find_most_effective_method(Methods)
    ).

% 10. Find beneficial organisms used in predator release programs
example_query_10 :-
    write('Example Query 10: Beneficial organisms for predator release'), nl,
    beneficial_organisms(predator_release, Organisms),
    write('Organisms used in predator release programs:'), nl,
    print_list(Organisms).

% 11. Compare effectiveness of biological vs physical control for aphids
example_query_11 :-
    write('Example Query 11: Comparing controls for aphids'), nl,
    findall(Method, (controls(Method, aphids), belongs_to(Method, biological_control)), BioControls),
    findall(Method, (controls(Method, aphids), belongs_to(Method, physical_control)), PhysControls),
    write('Biological controls for aphids:'), nl,
    print_list(BioControls),
    write('Physical controls for aphids:'), nl,
    print_list(PhysControls),
    write('Recommended integrated approach:'), nl,
    recommend_integrated_approach(aphids).

% 12. Find beneficial insects that prey on aphids
example_query_12 :-
    write('Example Query 12: Beneficial insects for aphid control'), nl,
    beneficial_insects_for(aphids, Beneficials),
    write('Beneficial insects that attack aphids:'), nl,
    print_list(Beneficials),
    write('Detailed information for most effective:'), nl,
    (member(lady_beetles, Beneficials) ->
        print_beneficial_details(lady_beetles)
    ;
        write('Lady beetles not found in list')
    ).

% 13. Find all methods to attract hover flies
example_query_13 :-
    write('Example Query 13: Methods to attract hover flies'), nl,
    attraction_methods_for(hover_flies, Methods),
    write('Methods to attract hover flies:'), nl,
    print_list(Methods).

% 14. Find all parasitoid beneficial insects
example_query_14 :-
    write('Example Query 14: Parasitoid beneficial insects'), nl,
    beneficials_by_category(parasitoid, Parasitoids),
    write('Parasitoid beneficial insects:'), nl,
    print_list(Parasitoids),
    write('Pests controlled by braconid wasps:'), nl,
    findall(Pest, parasitizes(braconid_wasps, Pest), Pests),
    print_list(Pests).

% 15. Find what beneficial insects can be attracted using flowering plants
example_query_15 :-
    write('Example Query 15: Beneficial insects attracted to flowering plants'), nl,
    findall(Beneficial, 
           (frame(beneficial_insect, [name:Beneficial, attraction_methods:Methods, _]),
            (member(pollen_producing_flowers, Methods);
             member(nectar_producing_flowers, Methods);
             member(pollen_producing_plants, Methods);
             member(nectar_producing_plants, Methods))),
           Beneficials),
    write('Beneficial insects attracted to flowering plants:'), nl,
    print_list(Beneficials).

% 16. Determine best beneficial insects for vegetable garden pest control
example_query_16 :-
    write('Example Query 16: Best beneficial insects for vegetable garden'), nl,
    common_vegetable_pests(Pests),
    write('Common vegetable garden pests:'), nl,
    print_list(Pests),
    write('Recommended beneficial insects for vegetable gardens:'), nl,
    recommend_beneficials_for_pests(Pests).

% 17. Find plants and methods for creating beneficial insect habitat
example_query_17 :-
    write('Example Query 17: Creating beneficial insect habitat'), nl,
    write('Habitat management methods:'), nl,
    beneficial_habitat_methods(Methods),
    print_list(Methods),
    write('Plants that attract beneficial insects by family:'), nl,
    write('Carrot family:'), nl,
    plants_by_family(carrot_family, CarrotFam),
    print_list(CarrotFam),
    write('Mint family:'), nl,
    plants_by_family(mint_family, MintFam),
    print_list(MintFam),
    write('Daisy family:'), nl,
    plants_by_family(daisy_family, DaisyFam),
    print_list(DaisyFam),
    write('Recommended habitat management method:'), nl,
    frame(biological_control, [name:beneficial_insect_habitat_management, description:Desc, application_method:App, _]),
    write(Desc), nl,
    write('Application method: '), write(App), nl.

% 18. Find organic sprays for aphid control
example_query_18 :-
    write('Example Query 18: Organic sprays for aphid control'), nl,
    organic_sprays_for(aphids, Sprays),
    write('Organic sprays effective against aphids:'), nl,
    print_list(Sprays),
    write('Safe, beneficial-friendly options:'), nl,
    safe_beneficial_friendly_for_pest(aphids, SafeSprays),
    print_list(SafeSprays).

% 19. Find organic sprays safe for beneficial insects
example_query_19 :-
    write('Example Query 19: Organic sprays safe for beneficial insects'), nl,
    beneficial_friendly_sprays(Sprays),
    write('Sprays that minimize harm to beneficial insects:'), nl,
    print_list(Sprays),
    write('Of these, fungicides include:'), nl,
    findall(Spray, 
           (member(Spray, Sprays),
            belongs_to(Spray, fungicide)),
           Fungicides),
    print_list(Fungicides).

% 20. Compare botanical insecticides by safety level
example_query_20 :-
    write('Example Query 20: Botanical insecticides by safety level'), nl,
    sprays_by_category(botanical_insecticide, BotSprays),
    write('Botanical insecticides:'), nl,
    print_list(BotSprays),
    write('Safety levels:'), nl,
    process_safety_levels(BotSprays).

% Helper predicate to print safety levels
process_safety_levels([]).
process_safety_levels([Spray|Rest]) :-
    safety_level(Spray, Level),
    write(Spray), write(': '), write(Level), nl,
    process_safety_levels(Rest).

% 21. Find application guidelines for spray safety
example_query_21 :-
    write('Example Query 21: Spray safety guidelines'), nl,
    frame(spray_safety, [name:spray_safely, guidelines:Guidelines, _]),
    write('Safety guidelines for spray application:'), nl,
    print_numbered_list(Guidelines).

% Helper predicate to print numbered list
print_numbered_list(List) :-
    print_numbered_list(List, 1).

print_numbered_list([], _).
print_numbered_list([Item|Rest], N) :-
    write(N), write('. '), write(Item), nl,
    N1 is N + 1,
    print_numbered_list(Rest, N1).

% ========================
% HELPER PREDICATES
% ========================

% Print a list with each element on a new line
print_list([]) :- nl.
print_list([H|T]) :-
    write('- '), write(H), nl,
    print_list(T).

% Process each pest to find its control methods
process_pest_controls([]).
process_pest_controls([Pest|Rest]) :-
    write('Controls for '), write(Pest), write(':'), nl,
    (all_controls_for_pest(Pest, Controls) ->
        print_list(Controls)
    ;
        write('- No specific controls found'), nl
    ),
    process_pest_controls(Rest).

% Process each disease to find physical control methods
process_disease_controls([]).
process_disease_controls([Disease|Rest]) :-
    write('Physical controls related to '), write(Disease), write(':'), nl,
    findall(Control, 
            (controls(Control, Disease), 
             belongs_to(Control, physical_control)), 
            Controls),
    (Controls = [] ->
        write('- No specific physical controls found'), nl
    ;
        print_list(Controls)
    ),
    process_disease_controls(Rest).

% Find the most effective method from a list
find_most_effective_method([]) :- 
    write('No methods to evaluate.'), nl.
find_most_effective_method(Methods) :-
    find_highest_effectiveness(Methods, BestMethod),
    (frame(biological_control, [name:BestMethod, description:Desc, effectiveness:Eff, application_method:App, _]) ->
        write('Method: '), write(BestMethod), nl,
        write('Effectiveness: '), write(Eff), nl,
        write('Description: '), write(Desc), nl,
        write('Application: '), write(App), nl
    ;
        write('Could not find details for '), write(BestMethod), nl
    ).

% Find highest effectiveness method
find_highest_effectiveness(Methods, BestMethod) :-
    find_highest_effectiveness(Methods, none, low, BestMethod).

find_highest_effectiveness([], CurrentBest, _, CurrentBest) :- CurrentBest \= none, !.
find_highest_effectiveness([], none, _, 'No effective method found') :- !.
find_highest_effectiveness([Method|Rest], CurrentBest, CurrentEff, BestMethod) :-
    (frame(biological_control, [name:Method, effectiveness:Eff, _]) ->
        (effectiveness_better(Eff, CurrentEff) ->
            find_highest_effectiveness(Rest, Method, Eff, BestMethod)
        ;
            find_highest_effectiveness(Rest, CurrentBest, CurrentEff, BestMethod)
        )
    ;
        find_highest_effectiveness(Rest, CurrentBest, CurrentEff, BestMethod)
    ).

% Compare effectiveness levels
effectiveness_better(high, medium) :- !.
effectiveness_better(high, low) :- !.
effectiveness_better(high, variable) :- !.
effectiveness_better(medium, low) :- !.
effectiveness_better(medium, variable) :- !.
effectiveness_better(variable, low) :- !.
effectiveness_better(_, none) :- !.

% Recommend integrated approach for a pest
recommend_integrated_approach(Pest) :-
    findall(BioMethod, (controls(BioMethod, Pest), belongs_to(BioMethod, biological_control)), BioMethods),
    findall(PhysMethod, (controls(PhysMethod, Pest), belongs_to(PhysMethod, physical_control)), PhysMethods),
    (BioMethods = [], PhysMethods = [] ->
        write('- No specific control methods found for this pest.'), nl
    ;
        (BioMethods \= [] ->
            write('- First try biological controls: '), 
            list_first_n(BioMethods, 2), nl
        ;
            true
        ),
        (PhysMethods \= [] ->
            write('- Supplement with physical barriers: '), 
            list_first_n(PhysMethods, 2), nl
        ;
            true
        ),
        write('- Monitor results and adjust methods as needed.'), nl
    ).

% List first N elements of a list
list_first_n(List, N) :-
    list_first_n(List, N, 0).

list_first_n([], _, _) :- !.
list_first_n(_, N, Count) :- Count >= N, !.
list_first_n([H|T], N, Count) :-
    Count =:= 0 ->
        write(H)
    ;
        write(', '), write(H)
    ,
    NewCount is Count + 1,
    list_first_n(T, N, NewCount).

% Helper predicate to print details of a beneficial insect
print_beneficial_details(Beneficial) :-
    frame(beneficial_insect, [name:Beneficial, scientific_name:Scientific, description:Desc, target_pests:Targets, attraction_methods:Methods, _]),
    write('Name: '), write(Beneficial), nl,
    write('Scientific name: '), write(Scientific), nl,
    write('Description: '), write(Desc), nl,
    write('Target pests: '), nl,
    print_list(Targets),
    write('Attraction methods: '), nl,
    print_list(Methods).

% Helper predicate for common vegetable pests
common_vegetable_pests([aphids, cabbage_loopers, colorado_potato_beetle_larvae, cutworms, tomato_hornworms, spider_mites, whiteflies, leafhoppers]).

% Helper predicate to recommend beneficials for a list of pests
recommend_beneficials_for_pests([]).
recommend_beneficials_for_pests([Pest|Rest]) :-
    write('For '), write(Pest), write(':'), nl,
    beneficial_insects_for(Pest, Beneficials),
    (Beneficials = [] ->
        write('- No specific beneficial insects found'), nl
    ;
        print_top_beneficials(Beneficials, 3)
    ),
    recommend_beneficials_for_pests(Rest).

% Helper predicate to print top N beneficial insects
print_top_beneficials(_, 0).
print_top_beneficials([], _).
print_top_beneficials([B|Bs], N) :-
    write('- '), write(B), nl,
    N1 is N - 1,
    print_top_beneficials(Bs, N1).

% Run all example queries
run_all_examples :-
    example_query_1, nl,
    example_query_2, nl,
    example_query_3, nl,
    example_query_4, nl,
    example_query_5, nl,
    example_query_6, nl,
    example_query_7, nl,
    example_query_8, nl,
    example_query_9, nl,
    example_query_10, nl,
    example_query_11, nl,
    example_query_12, nl,
    example_query_13, nl,
    example_query_14, nl,
    example_query_15, nl,
    example_query_16, nl,
    example_query_17, nl,
    example_query_18, nl,
    example_query_19, nl,
    example_query_20, nl,
    example_query_21.

% Auto-run examples when file is consulted
:- run_all_examples. 
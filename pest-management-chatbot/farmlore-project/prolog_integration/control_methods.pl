% ========================
% CONTROL METHODS KNOWLEDGE BASE
% ========================
% Contains information about physical and biological control methods for pest management

% Ensure compatibility with existing knowledge bases
:- discontiguous(frame/2).

% ========================
% FRAME TEMPLATES
% ========================
frame(physical_control, [
    name: atom,
    category: atom,
    description: string,
    target_pests: list(atom),
    materials_needed: list(atom),
    application_method: string,
    effectiveness: atom, % high, medium, low
    limitations: list(atom),
    context: list(atom)
]).

frame(biological_control, [
    name: atom,
    category: atom,
    description: string,
    target_pests: list(atom),
    beneficial_organism: atom,
    application_method: string,
    effectiveness: atom, % high, medium, low
    limitations: list(atom),
    context: list(atom)
]).

% ========================
% PHYSICAL CONTROL METHODS
% ========================

frame(physical_control, [
    name: crawling_pest_barriers,
    category: barrier,
    description: 'Bands of unattractive or abrasive materials that circle garden plants or beds to keep pests away. Dusts or powders such as diatomaceous earth, wood ashes, or crushed seashells scratch insects\' waxy coating, destroying their water balance and killing them.',
    target_pests: [earwigs, slugs, snails, sowbugs, caterpillars, ants, borers],
    materials_needed: [diatomaceous_earth, wood_ashes, sawdust, crushed_seashells, cinders, aluminum_foil],
    application_method: 'Place a 2-inch wide strip of material as a border around beds or individual plants. For dehydrating dust paint, mix ¼ pound diatomaceous earth with 1 teaspoon pure liquid soap and enough water to make a thick slurry, then apply to lower trunk.',
    effectiveness: medium,
    limitations: [
        requires_replacement_after_rain,
        less_effective_in_wet_weather,
        high_pest_populations_may_overwhelm_barrier
    ],
    context: [organic_gardening, preventive_approach, physical_deterrent]
]).

frame(physical_control, [
    name: copper_strips,
    category: barrier,
    description: 'Copper barriers repel slugs and snails. When these mollusks contact copper, they receive a small electric shock that causes them to retreat.',
    target_pests: [slugs, snails],
    materials_needed: [copper_strips, copper_mesh, copper_tape],
    application_method: 'Place 2-3 inch wide strips of copper around raised beds, container rims, or tree trunks. Keep vegetation from bridging the barrier.',
    effectiveness: high,
    limitations: [
        expensive_for_large_areas,
        vegetation_can_create_bridges,
        requires_proper_installation
    ],
    context: [organic_gardening, preventive_approach, physical_deterrent]
]).

frame(physical_control, [
    name: cutworm_collars,
    category: barrier,
    description: 'Physical barriers placed around seedlings to protect from cutworms, which are night-feeders that spend the day just under the soil surface.',
    target_pests: [cutworms, crawling_insects],
    materials_needed: [cardboard_tubes, shallow_cans],
    application_method: 'Recycle cardboard tubes from toilet paper and paper towels. Cut into 2-3 inch sections, then place over small seedlings while transplanting, pushing the collars into the soil.',
    effectiveness: high,
    limitations: [
        labor_intensive_for_large_plantings,
        temporary_protection_until_plants_mature,
        metal_collars_need_removal
    ],
    context: [organic_gardening, seedling_protection, physical_barrier]
]).

frame(physical_control, [
    name: floating_row_covers,
    category: barrier,
    description: 'Lightweight fabric covers that rest on plant foliage, creating a barrier against pests while allowing light, water, and air to penetrate. They can also extend the growing season by increasing temperatures underneath.',
    target_pests: [aphids, asparagus_beetles, cabbage_root_maggots, caterpillars, colorado_potato_beetles, flea_beetles, leafhoppers, mexican_bean_beetles, carrot_rust_flies],
    materials_needed: [polyethylene, polyester, polypropylene, polyvinyl_alcohol, polystyrene, mosquito_netting, cheesecloth, sheer_drapery_fabric],
    application_method: 'Thoroughly weed the site. Place covers over the row immediately after planting seeds or transplants. Leave enough slack to allow plants to grow underneath. Anchor edges with soil, rocks, boards, or other heavy objects.',
    effectiveness: high,
    limitations: [
        must_be_removed_for_flowering_plants,
        heat_buildup_in_summer,
        does_not_control_soil-dwelling_pests,
        requires_removal_for_weeding
    ],
    context: [organic_gardening, preventive_approach, season_extension]
]).

frame(physical_control, [
    name: mulches,
    category: barrier,
    description: 'Materials placed on soil surface to provide a barrier between plant foliage and soil that may contain disease spores or pests. Also serve as a barrier for pests headed for the garden floor to lay eggs or overwinter.',
    target_pests: [aphids, leafhoppers, thrips, sowbugs, leafminers, fungal_diseases],
    materials_needed: [aluminum_foil, black_plastic, newspaper, organic_materials],
    application_method: 'Cover beds or rows before planting with aluminum-coated paper or foil. For black plastic or paper mulches, anchor edges and cut holes for plants. For organic mulches, apply fresh material several times yearly.',
    effectiveness: medium,
    limitations: [
        some_mulches_need_periodic_replacement,
        can_create_habitat_for_some_pests,
        aluminum_mulch_can_cause_heat_damage_in_summer
    ],
    context: [organic_gardening, soil_protection, disease_prevention, moisture_conservation]
]).

frame(physical_control, [
    name: protective_painting,
    category: barrier,
    description: 'Painting tree trunks with diluted white latex paint or whitewash to protect from borers and sunburn.',
    target_pests: [flatheaded_borers],
    materials_needed: [white_latex_paint, water, whitewash],
    application_method: 'Paint the tree trunk using white latex paint diluted with equal parts of water, or use whitewash. Extend from 1 inch below soil line to 25-30 inches up the trunk.',
    effectiveness: medium,
    limitations: [
        requires_annual_reapplication,
        only_protects_treated_areas,
        primarily_preventive
    ],
    context: [orchard_management, preventive_approach, tree_protection]
]).

frame(physical_control, [
    name: rigid_plant_covers,
    category: barrier,
    description: 'Sturdy frames covered with screening material to protect plants from insects and animals while allowing air, light, and water to reach plants.',
    target_pests: [flying_insects, crawling_insects, birds, small_mammals],
    materials_needed: [window_screening, wooden_frames, staples],
    application_method: 'Make screen cones, plant tents, or frames covered with screening. Place over individual plants or rows, ensuring bottom edges are buried in soil to prevent pest entry.',
    effectiveness: high,
    limitations: [
        labor_intensive_to_construct,
        limit_access_for_maintenance,
        can_restrict_plant_growth,
        require_storage_space
    ],
    context: [organic_gardening, long_term_protection, durable_solution]
]).

frame(physical_control, [
    name: seedling_protectors,
    category: barrier,
    description: 'Paper barriers placed around seedlings to prevent root maggot flies from laying eggs in the soil near plants.',
    target_pests: [root_maggot_flies],
    materials_needed: [tar_paper, heavy_paper],
    application_method: 'Cut 6-8 inch diameter circles with one cut from edge to center. Place on soil around each plant with stem in middle. Leave in place until harvest.',
    effectiveness: medium,
    limitations: [
        labor_intensive_for_large_plantings,
        may_degrade_in_wet_conditions,
        only_protects_against_specific_pests
    ],
    context: [organic_gardening, preventive_approach, transplant_protection]
]).

frame(physical_control, [
    name: shade_cloths,
    category: environmental_modification,
    description: 'Woven fabric used to reduce light intensity and protect plants from extreme heat and sunscald.',
    target_pests: [sunscald, heat_stress, birds, small_animals],
    materials_needed: [shade_cloth, support_structures],
    application_method: 'Suspend shade cloth over crops when temperatures reach 80°F or higher, using stakes or other supports. Choose appropriate shade percentage for specific crops.',
    effectiveness: medium,
    limitations: [
        limited_pest_protection,
        may_reduce_light_too_much,
        requires_support_structure,
        primarily_for_environmental_protection
    ],
    context: [season_extension, cool_season_crops, summer_gardening]
]).

frame(physical_control, [
    name: trunk_bands,
    category: barrier,
    description: 'Barriers and traps placed around tree trunks to intercept pests that crawl up and down trees.',
    target_pests: [ants, codling_moth_caterpillars, gypsy_moth_caterpillars, cutworms, leaf_beetles, snails, slugs],
    materials_needed: [sticky_coating, corrugated_cardboard, burlap_strips, tape, foam_backed_tree_banding_strips],
    application_method: 'Apply sticky material to removable wrap around trunk. For codling moth, wrap corrugated cardboard around trunk and check weekly. For other pests, use sticky bands, burlap traps, or commercial banding products.',
    effectiveness: high,
    limitations: [
        requires_regular_maintenance,
        sticky_material_can_damage_bark_if_applied_directly,
        needs_replacement_when_clogged_with_pests
    ],
    context: [orchard_management, integrated_pest_management, tree_protection]
]).

% ========================
% BIOLOGICAL CONTROL INTRODUCTION
% ========================

frame(biological_control, [
    name: biological_control_principles,
    category: concept,
    description: 'Controlling pests with their natural enemies—a phenomenon as old as the pests themselves. Garden pests and their natural enemies coexist in balanced populations in well-managed organic gardens.',
    target_pests: [garden_pests],
    beneficial_organism: multiple_organisms,
    application_method: 'Enhance effectiveness of beneficial organisms through providing food, water, and habitat. Release commercially reared predators and parasites when necessary.',
    effectiveness: variable,
    limitations: [
        dependent_on_climate_conditions,
        soil_type_influences_success,
        requires_alternate_food_sources,
        may_not_provide_immediate_control
    ],
    context: [ecological_balance, sustainable_gardening, integrated_pest_management]
]).

frame(biological_control, [
    name: encouraging_beneficials,
    category: habitat_management,
    description: 'Methods to attract and retain beneficial organisms in gardens. More beneficial organisms visit plants than pests, though they often go unnoticed due to their inconspicuous size and habits.',
    target_pests: [garden_pests],
    beneficial_organism: multiple_organisms,
    application_method: 'Provide food sources like pollen, nectar, and supplemental food. Create habitat through diverse plantings. Minimize pesticide use that might harm beneficial organisms.',
    effectiveness: medium,
    limitations: [
        takes_time_to_establish_populations,
        may_not_prevent_all_pest_damage,
        requires_understanding_of_ecological_relationships
    ],
    context: [ecological_gardening, preventive_approach, habitat_creation]
]).

% ========================
% BIOLOGICAL CONTROL METHODS
% ========================

frame(biological_control, [
    name: beneficial_habitat,
    category: habitat_management,
    description: 'Creating and maintaining habitat features that attract and sustain beneficial insects and other organisms that prey on or parasitize garden pests.',
    target_pests: [general_garden_pests],
    beneficial_organism: diverse_beneficial_species,
    application_method: 'Plant diverse flowering plants that provide pollen and nectar, create habitat features like brush piles or insect hotels, and minimize pesticide use to protect beneficial populations.',
    effectiveness: medium,
    limitations: [
        takes_time_to_establish,
        requires_season-long_commitment,
        may_not_provide_immediate_control,
        requires_space_dedicated_to_habitat_rather_than_production
    ],
    context: [ecological_gardening, sustainable_pest_management, preventive_approach]
]).

frame(biological_control, [
    name: food_sources_for_beneficials,
    category: habitat_management,
    description: 'Providing supplemental food sources to attract and sustain beneficial insects when pest populations are low, enabling them to reproduce and maintain presence in the garden.',
    target_pests: [general_garden_pests],
    beneficial_organism: diverse_beneficial_species,
    application_method: 'Plant flowers with accessible nectar and pollen, especially umbelliferous plants (carrot family) and composites. Consider supplemental feeding with honeydew substitutes, pollen, or commercial beneficial insect food.',
    effectiveness: medium,
    limitations: [
        indirect_approach,
        results_not_immediate,
        requires_knowledge_of_beneficial_insect_needs,
        requires_continuous_availability_of_flowering_plants
    ],
    context: [ecological_gardening, long_term_approach, preventive_pest_management]
]).

frame(biological_control, [
    name: bird_attraction,
    category: vertebrate_predators,
    description: 'Encouraging insectivorous birds to visit and hunt in garden areas by providing habitat, water, and supplemental food sources.',
    target_pests: [caterpillars, beetles, grubs, aphids, various_insects],
    beneficial_organism: insectivorous_birds,
    application_method: 'Install bird feeders, birdhouses, and birdbaths. Plant native species that provide shelter and nesting sites. Include trees and shrubs that produce berries or seeds as supplemental food.',
    effectiveness: medium,
    limitations: [
        birds_may_also_eat_beneficial_insects,
        requires_consistent_habitat_maintenance,
        birds_may_damage_some_crops,
        seasonal_variation_in_bird_presence
    ],
    context: [ecological_gardening, wildlife_gardening, integrated_pest_management]
]).

frame(biological_control, [
    name: bacillus_thuringiensis,
    category: microbial_control,
    description: 'A naturally occurring soil bacterium that produces proteins toxic to specific insect groups when ingested, particularly effective against caterpillars.',
    target_pests: [caterpillars, cabbage_looper, imported_cabbage_worm, tomato_hornworm, corn_earworm, gypsy_moth_caterpillar, tent_caterpillars],
    beneficial_organism: bacillus_thuringiensis,
    application_method: 'Apply as a spray to plant surfaces where caterpillars feed. Time application for when young caterpillars are actively feeding. Reapply after rain or heavy dew as needed.',
    effectiveness: high,
    limitations: [
        only_affects_feeding_larvae,
        most_effective_on_young_caterpillars,
        breaks_down_in_sunlight,
        requires_ingestion_to_work,
        specific_strains_for_different_pest_groups
    ],
    context: [organic_gardening, targeted_pest_control, minimal_impact_on_non-targets]
]).

frame(biological_control, [
    name: predator_release,
    category: augmentative_biocontrol,
    description: 'The controlled release of commercially reared predatory insects to supplement natural populations and achieve faster pest control.',
    target_pests: [aphids, mealybugs, scale_insects, spider_mites, whiteflies, thrips],
    beneficial_organism: multiple_predators,
    application_method: 'Purchase from commercial insectaries and release according to supplier instructions. Timing is critical - release when pest populations are present but not overwhelming. Some predators require multiple releases.',
    effectiveness: variable,
    limitations: [
        can_be_expensive,
        predators_may_disperse,
        effectiveness_depends_on_environmental_conditions,
        requires_proper_timing,
        may_not_establish_permanent_populations
    ],
    context: [greenhouse_growing, intensive_gardening, rapid_response]
]).

frame(biological_control, [
    name: parasitoid_wasps,
    category: parasitism,
    description: 'Small non-stinging wasps that lay eggs in or on host insects, with larvae developing by consuming the host, eventually killing it.',
    target_pests: [aphids, caterpillars, beetle_larvae, flies],
    beneficial_organism: parasitoid_wasps,
    application_method: 'Enhance habitat with flowering plants that provide nectar for adult wasps. Release commercially reared parasitoids when pest populations are detected but still at moderate levels.',
    effectiveness: high,
    limitations: [
        requires_proper_identification_of_pest_for_specific_parasitoid,
        climate_sensitive,
        may_be_affected_by_pesticides,
        requires_patience_as_control_is_not_immediate
    ],
    context: [targeted_pest_control, sustainable_agriculture, low_environmental_impact]
]).

% ========================
% BENEFICIAL INSECT HABITAT
% ========================
% Information about creating and maintaining habitat for beneficial insects

frame(biological_control, [
    name: beneficial_insect_habitat_management,
    category: habitat_management,
    description: 'Comprehensive approach to managing the garden environment to attract and sustain beneficial insects. Focuses on providing food, water, shelter and creating an environment that supports natural enemies of garden pests.',
    target_pests: [general_garden_pests],
    beneficial_organism: diverse_beneficial_species,
    application_method: 'Create a diverse, pesticide-free garden with flowering plants, water sources, shelter areas, and minimal soil disturbance to encourage natural pest control.',
    effectiveness: high,
    limitations: [
        requires_season_long_commitment,
        takes_time_to_establish,
        requires_garden_space_for_non_crop_plants,
        may_not_provide_immediate_control
    ],
    context: [ecological_gardening, sustainable_pest_management, preventive_approach]
]).

frame(biological_control, [
    name: flowering_plants_for_beneficials,
    category: habitat_management,
    description: 'Using specific flowering plants to attract and sustain beneficial insects. Many beneficial insects require nectar and pollen at some point in their life cycle.',
    target_pests: [general_garden_pests],
    beneficial_organism: diverse_beneficial_species,
    application_method: 'Plant members of the carrot family (Umbelliferae) like caraway, dill, fennel, lovage, and parsley; mint family (Labiatae) plants like catnip, hyssop, and lemon balm; and daisy family (Compositae) plants like coneflowers, daisies and yarrow. Include "weeds" like corn spurry, goldenrod, lamb\'s-quarters, wild mustard, and Queen Anne\'s lace.',
    effectiveness: medium,
    limitations: [
        seasonal_flowering_period,
        requires_multiple_plant_species,
        needs_garden_space,
        slow_establishment
    ],
    context: [ecological_gardening, companion_planting, habitat_creation]
]).

frame(biological_control, [
    name: cover_crops_for_beneficials,
    category: habitat_management,
    description: 'Using cover crops as sources of food and shelter for beneficial insects, creating refuge areas within and around the garden.',
    target_pests: [general_garden_pests],
    beneficial_organism: diverse_beneficial_species,
    application_method: 'Plant buckwheat as a short-term cover crop during garden season to quickly provide blooms and cover. Use alfalfa, clover, or ivy as borders around the garden to create beneficial habitat zones.',
    effectiveness: medium,
    limitations: [
        requires_dedicated_space,
        seasonal_limitations,
        management_required,
        competition_with_crops
    ],
    context: [ecological_gardening, habitat_creation, sustainable_agriculture]
]).

frame(biological_control, [
    name: water_sources_for_beneficials,
    category: habitat_management,
    description: 'Providing water sources for beneficial insects, which like all organisms require hydration, especially during drought periods.',
    target_pests: [general_garden_pests],
    beneficial_organism: diverse_beneficial_species,
    application_method: 'Place shallow containers filled with rocks in shady locations to serve as insect perches and water sources. Change water frequently to prevent mosquito breeding.',
    effectiveness: medium,
    limitations: [
        requires_regular_maintenance,
        mosquito_breeding_risk,
        limited_range_of_effectiveness
    ],
    context: [ecological_gardening, habitat_enhancement]
]).

frame(biological_control, [
    name: shelter_for_beneficials,
    category: habitat_management,
    description: 'Creating shelter areas to protect beneficial insects from weather extremes and disturbance, providing safe havens during garden maintenance activities.',
    target_pests: [general_garden_pests],
    beneficial_organism: diverse_beneficial_species,
    application_method: 'Establish hedgerows, flowering shrubs, perennial borders, and use mulches like newspaper or compost as resting places. For soil-dwelling beneficials, create permanent beds with stone mulches and minimize tillage.',
    effectiveness: high,
    limitations: [
        requires_dedicated_space,
        reduced_tillage_may_favor_some_pests,
        permanent_structures_needed
    ],
    context: [ecological_gardening, habitat_creation, soil_conservation]
]).

frame(biological_control, [
    name: pesticide_avoidance,
    category: habitat_management,
    description: 'Minimizing or eliminating pesticide use to protect beneficial insects. Even botanical insecticides like pyrethrin can harm beneficial species.',
    target_pests: [general_garden_pests],
    beneficial_organism: diverse_beneficial_species,
    application_method: 'Avoid broad-spectrum pesticides completely. If treatment is necessary, use highly targeted approaches that minimize impact on beneficials. Allow some pest presence to maintain food sources for beneficials.',
    effectiveness: high,
    limitations: [
        requires_tolerance_for_some_pest_damage,
        delayed_pest_control,
        knowledge_of_ecological_relationships
    ],
    context: [ecological_gardening, sustainable_pest_management, integrated_pest_management]
]).

frame(biological_control, [
    name: supplemental_feeding,
    category: habitat_management,
    description: 'Providing artificial food sources for beneficial insects when natural food is scarce to maintain populations through low pest periods.',
    target_pests: [general_garden_pests],
    beneficial_organism: diverse_beneficial_species,
    application_method: 'Purchase commercial beneficial insect food containing yeast, sugar, and added vitamins. Place in sheltered areas among garden plants when natural food supplies are low.',
    effectiveness: medium,
    limitations: [
        regular_application_needed,
        cost_of_commercial_products,
        primarily_supplemental_rather_than_primary
    ],
    context: [intensive_gardening, greenhouse_growing, population_maintenance]
]).

% ========================
% RELATIONSHIPS
% ========================

% Control method-pest relationships
controls(crawling_pest_barriers, earwigs).
controls(crawling_pest_barriers, slugs).
controls(crawling_pest_barriers, snails).
controls(crawling_pest_barriers, sowbugs).
controls(crawling_pest_barriers, caterpillars).
controls(copper_strips, slugs).
controls(copper_strips, snails).
controls(cutworm_collars, cutworms).
controls(cutworm_collars, crawling_insects).
controls(floating_row_covers, aphids).
controls(floating_row_covers, asparagus_beetles).
controls(floating_row_covers, cabbage_root_maggots).
controls(floating_row_covers, colorado_potato_beetles).
controls(floating_row_covers, flea_beetles).
controls(floating_row_covers, leafhoppers).
controls(floating_row_covers, mexican_bean_beetles).
controls(floating_row_covers, carrot_rust_flies).
controls(mulches, aphids).
controls(mulches, leafhoppers).
controls(mulches, thrips).
controls(mulches, sowbugs).
controls(mulches, leafminers).
controls(protective_painting, flatheaded_borers).
controls(rigid_plant_covers, flying_insects).
controls(rigid_plant_covers, crawling_insects).
controls(rigid_plant_covers, birds).
controls(rigid_plant_covers, small_mammals).
controls(seedling_protectors, root_maggot_flies).
controls(shade_cloths, birds).
controls(shade_cloths, small_animals).
controls(trunk_bands, ants).
controls(trunk_bands, codling_moth_caterpillars).
controls(trunk_bands, gypsy_moth_caterpillars).
controls(trunk_bands, cutworms).
controls(trunk_bands, leaf_beetles).
controls(trunk_bands, snails).
controls(trunk_bands, slugs).
controls(biological_control_principles, garden_pests).
controls(encouraging_beneficials, garden_pests).
controls(beneficial_habitat, general_garden_pests).
controls(food_sources_for_beneficials, general_garden_pests).
controls(bird_attraction, caterpillars).
controls(bird_attraction, beetles).
controls(bird_attraction, grubs).
controls(bird_attraction, aphids).
controls(bacillus_thuringiensis, caterpillars).
controls(bacillus_thuringiensis, cabbage_looper).
controls(bacillus_thuringiensis, imported_cabbage_worm).
controls(bacillus_thuringiensis, tomato_hornworm).
controls(bacillus_thuringiensis, corn_earworm).
controls(bacillus_thuringiensis, gypsy_moth_caterpillar).
controls(predator_release, aphids).
controls(predator_release, mealybugs).
controls(predator_release, scale_insects).
controls(predator_release, spider_mites).
controls(predator_release, whiteflies).
controls(predator_release, thrips).
controls(parasitoid_wasps, aphids).
controls(parasitoid_wasps, caterpillars).
controls(parasitoid_wasps, beetle_larvae).
controls(parasitoid_wasps, flies).
controls(beneficial_insect_habitat_management, general_garden_pests).
controls(flowering_plants_for_beneficials, general_garden_pests).
controls(cover_crops_for_beneficials, general_garden_pests).
controls(water_sources_for_beneficials, general_garden_pests).
controls(shelter_for_beneficials, general_garden_pests).
controls(pesticide_avoidance, general_garden_pests).
controls(supplemental_feeding, general_garden_pests).

% Material-control method relationships
used_in(diatomaceous_earth, crawling_pest_barriers).
used_in(wood_ashes, crawling_pest_barriers).
used_in(sawdust, crawling_pest_barriers).
used_in(crushed_seashells, crawling_pest_barriers).
used_in(cinders, crawling_pest_barriers).
used_in(aluminum_foil, crawling_pest_barriers).
used_in(copper_strips, copper_strips).
used_in(copper_mesh, copper_strips).
used_in(copper_tape, copper_strips).
used_in(cardboard_tubes, cutworm_collars).
used_in(shallow_cans, cutworm_collars).
used_in(polyethylene, floating_row_covers).
used_in(polyester, floating_row_covers).
used_in(polypropylene, floating_row_covers).
used_in(polyvinyl_alcohol, floating_row_covers).
used_in(polystyrene, floating_row_covers).
used_in(aluminum_foil, mulches).
used_in(black_plastic, mulches).
used_in(newspaper, mulches).
used_in(organic_materials, mulches).
used_in(white_latex_paint, protective_painting).
used_in(whitewash, protective_painting).
used_in(window_screening, rigid_plant_covers).
used_in(wooden_frames, rigid_plant_covers).
used_in(tar_paper, seedling_protectors).
used_in(heavy_paper, seedling_protectors).
used_in(shade_cloth, shade_cloths).
used_in(sticky_coating, trunk_bands).
used_in(corrugated_cardboard, trunk_bands).
used_in(burlap_strips, trunk_bands).
used_in(foam_backed_tree_banding_strips, trunk_bands).

% Organism-control method relationships
used_for(diverse_beneficial_species, beneficial_habitat).
used_for(diverse_beneficial_species, food_sources_for_beneficials).
used_for(insectivorous_birds, bird_attraction).
used_for(bacillus_thuringiensis, bacillus_thuringiensis).
used_for(lady_beetles, predator_release).
used_for(lacewings, predator_release).
used_for(predatory_mites, predator_release).
used_for(trichogramma_wasps, parasitoid_wasps).
used_for(braconid_wasps, parasitoid_wasps).
used_for(aphidius_wasps, parasitoid_wasps).

% Control category relationships
belongs_to(crawling_pest_barriers, physical_control).
belongs_to(copper_strips, physical_control).
belongs_to(cutworm_collars, physical_control).
belongs_to(floating_row_covers, physical_control).
belongs_to(mulches, physical_control).
belongs_to(protective_painting, physical_control).
belongs_to(rigid_plant_covers, physical_control).
belongs_to(seedling_protectors, physical_control).
belongs_to(shade_cloths, physical_control).
belongs_to(trunk_bands, physical_control).
belongs_to(biological_control_principles, biological_control).
belongs_to(encouraging_beneficials, biological_control).
belongs_to(beneficial_habitat, biological_control).
belongs_to(food_sources_for_beneficials, biological_control).
belongs_to(bird_attraction, biological_control).
belongs_to(bacillus_thuringiensis, biological_control).
belongs_to(predator_release, biological_control).
belongs_to(parasitoid_wasps, biological_control).
belongs_to(beneficial_insect_habitat_management, biological_control).
belongs_to(flowering_plants_for_beneficials, biological_control).
belongs_to(cover_crops_for_beneficials, biological_control).
belongs_to(water_sources_for_beneficials, biological_control).
belongs_to(shelter_for_beneficials, biological_control).
belongs_to(pesticide_avoidance, biological_control).
belongs_to(supplemental_feeding, biological_control).

% Helper predicates
control_methods_for(Pest, ControlList) :- findall(Control, controls(Control, Pest), ControlList).
materials_for(ControlMethod, MaterialList) :- findall(Material, used_in(Material, ControlMethod), MaterialList).
control_category(ControlMethod, Category) :- belongs_to(ControlMethod, Category).

% ========================
% CROSS-REFERENCE PREDICATES
% ========================
% These predicates help connect this knowledge base with the insect_reference and plant_disease_reference knowledge bases

% Find all control methods for a specific pest (referenced in any knowledge base)
all_controls_for_pest(Pest, ControlMethods) :-
    findall(Control, controls(Control, Pest), DirectControls),
    findall(Control, (frame(specific_insect, [name:Pest, control_methods:Methods, _]), member(Control, Methods)), InsectKBControls),
    append(DirectControls, InsectKBControls, AllControls),
    sort(AllControls, ControlMethods).

% Find pests that can be controlled by a specific method
pests_controlled_by(Method, Pests) :-
    findall(Pest, controls(Method, Pest), DirectPests),
    findall(Pest, (frame(pest, [name:Pest, controls:Methods, _]), member(Method, Methods)), KBPests),
    append(DirectPests, KBPests, AllPests),
    sort(AllPests, Pests).

% Determine if a control method is effective for a specific pest
effective_against(ControlMethod, Pest) :-
    controls(ControlMethod, Pest).
effective_against(ControlMethod, Pest) :-
    frame(specific_insect, [name:Pest, control_methods:Methods, _]),
    member(ControlMethod, Methods).
effective_against(ControlMethod, Pest) :-
    frame(pest, [name:Pest, controls:Methods, _]),
    member(ControlMethod, Methods).

% Find physical controls for a specific category
physical_controls_in_category(Category, Controls) :-
    findall(Control, 
            (frame(physical_control, [name:Control, category:Category, _])),
            Controls).

% Additional helper predicates
beneficial_organisms(ControlMethod, Organisms) :- 
    findall(Organism, used_for(Organism, ControlMethod), Organisms).

control_methods_by_category(Category, Methods) :-
    findall(Method, belongs_to(Method, Category), Methods).

% Add relationships for plants that attract beneficial insects
attracts_beneficial(caraway, beneficial_insects).
attracts_beneficial(dill, beneficial_insects).
attracts_beneficial(fennel, beneficial_insects).
attracts_beneficial(lovage, beneficial_insects).
attracts_beneficial(parsley, beneficial_insects).
attracts_beneficial(catnip, beneficial_insects).
attracts_beneficial(hyssop, beneficial_insects).
attracts_beneficial(lemon_balm, beneficial_insects).
attracts_beneficial(coneflowers, beneficial_insects).
attracts_beneficial(daisies, beneficial_insects).
attracts_beneficial(yarrow, beneficial_insects).
attracts_beneficial(corn_spurry, beneficial_insects).
attracts_beneficial(goldenrod, beneficial_insects).
attracts_beneficial(lambs_quarters, beneficial_insects).
attracts_beneficial(wild_mustard, beneficial_insects).
attracts_beneficial(queen_annes_lace, beneficial_insects).
attracts_beneficial(buckwheat, beneficial_insects).
attracts_beneficial(alfalfa, beneficial_insects).
attracts_beneficial(clover, beneficial_insects).

% Helper predicates for the new habitat information
plant_family(caraway, carrot_family).
plant_family(dill, carrot_family).
plant_family(fennel, carrot_family).
plant_family(lovage, carrot_family).
plant_family(parsley, carrot_family).
plant_family(catnip, mint_family).
plant_family(hyssop, mint_family).
plant_family(lemon_balm, mint_family).
plant_family(coneflowers, daisy_family).
plant_family(daisies, daisy_family).
plant_family(yarrow, daisy_family).

beneficial_habitat_methods(MethodList) :- 
    findall(Method, 
            (frame(biological_control, [name:Method, category:habitat_management, _])), 
            MethodList).

plants_for_beneficial_habitat(PlantList) :-
    findall(Plant, attracts_beneficial(Plant, beneficial_insects), PlantList).

plants_by_family(Family, PlantList) :-
    findall(Plant, plant_family(Plant, Family), PlantList). 
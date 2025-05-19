% ========================
% INSECT REFERENCE KNOWLEDGE BASE
% ========================
% Contains general educational information about insects for reference

% Ensure compatibility with existing knowledge base
:- discontiguous(frame/2).

% ========================
% FRAME TEMPLATES
% ========================
frame(insect_general, [
    name: atom,
    category: atom,
    description: string,
    characteristics: list(atom),
    context: list(atom)
]).

frame(insect_life_cycle, [
    name: atom,
    type: atom,
    stages: list(atom),
    description: string,
    examples: list(atom),
    context: list(atom)
]).

frame(insect_feeding, [
    name: atom,
    diet_type: atom,
    description: string,
    examples: list(atom),
    context: list(atom)
]).

frame(beneficial_insect, [
    name: atom,
    category: atom,
    benefits: list(atom),
    target_pests: list(atom),
    description: string,
    attraction_methods: list(atom),
    context: list(atom)
]).

frame(pest_management_principle, [
    name: atom,
    category: atom,
    description: string,
    methods: list(atom),
    context: list(atom)
]).

frame(specific_insect, [
    name: atom,
    type: atom,  % 'pest' or 'beneficial'
    scientific_name: atom,
    description: string,
    appearance: string,
    damage: string,
    host_plants: list(atom),
    life_cycle: string,
    control_methods: list(atom),
    region: list(atom)
]).

% ========================
% TAXONOMY & ONTOLOGY
% ========================
% Insect Classification
subclass(arthropod, animal).
subclass(insect, arthropod).
subclass(arachnid, arthropod).
subclass(crustacean, arthropod).
subclass(myriapod, arthropod).  % millipedes, centipedes

% Insect Orders
subclass(lepidoptera, insect).   % butterflies, moths
subclass(coleoptera, insect).    % beetles
subclass(diptera, insect).       % flies, mosquitoes
subclass(hymenoptera, insect).   % bees, wasps, ants
subclass(hemiptera, insect).     % true bugs
subclass(orthoptera, insect).    % grasshoppers, crickets
subclass(odonata, insect).       % dragonflies, damselflies

% Beneficial Categories
subclass(pollinator, beneficial_insect).
subclass(predator, beneficial_insect).
subclass(parasitoid, beneficial_insect).
subclass(decomposer, beneficial_insect).

% ========================
% GENERAL INSECT INFORMATION
% ========================
frame(insect_general, [
    name: insect_anatomy,
    category: anatomy,
    description: 'Insects are cold-blooded arthropods with three main body sections: head, thorax, and abdomen. They have six legs attached to the thorax, one pair of antennae on the head, and most have wings. They breathe through spiracles (small openings) along the sides of their bodies that connect to branching tubes called tracheae.',
    characteristics: [
        exoskeleton,
        three_body_sections,
        six_legs,
        antennae,
        most_have_wings,
        breathe_through_spiracles,
        cold_blooded
    ],
    context: [educational_reference, insect_identification]
]).

frame(insect_general, [
    name: insect_diversity,
    category: taxonomy,
    description: 'Insects are the most diverse group of animals on Earth, with over 1 million described species and potentially millions more undiscovered. They have adapted to virtually every climate and habitat except the deep ocean. Only a small fraction of insects are agricultural or garden pests, while the overwhelming majority are either beneficial or harmless.',
    characteristics: [
        most_diverse_animal_group,
        found_in_nearly_all_habitats,
        small_percentage_are_pests,
        majority_beneficial_or_harmless,
        high_adaptability
    ],
    context: [ecological_importance, pest_management_context]
]).

frame(insect_general, [
    name: garden_insect_balance,
    category: ecology,
    description: 'In gardens and agricultural settings, insect populations naturally tend toward balance, with predatory and parasitic insects helping to control pest species. Organic gardeners aim to work with this natural balance rather than disrupting it with broad-spectrum pesticides that kill beneficial species along with pests.',
    characteristics: [
        natural_pest_control,
        ecological_balance,
        predator_prey_relationships,
        sensitive_to_pesticide_disruption
    ],
    context: [organic_gardening, integrated_pest_management]
]).

% ========================
% INSECT LIFE CYCLES
% ========================
frame(insect_life_cycle, [
    name: complete_metamorphosis,
    type: metamorphosis,
    stages: [egg, larva, pupa, adult],
    description: 'Complete metamorphosis involves four distinct life stages: egg, larva, pupa, and adult. The immature forms look completely different from adults and often live in different habitats and eat different foods. During the pupal stage, the insect undergoes complete transformation of its tissues.',
    examples: [
        butterflies,
        moths,
        beetles,
        flies,
        bees,
        wasps
    ],
    context: [
        caterpillars_become_butterflies,
        maggots_become_flies,
        grubs_become_beetles,
        larvae_and_adults_often_have_different_diets_and_habitats
    ]
]).

frame(insect_life_cycle, [
    name: incomplete_metamorphosis,
    type: metamorphosis,
    stages: [egg, nymph, adult],
    description: 'Incomplete metamorphosis involves three life stages: egg, nymph, and adult. Nymphs resemble small wingless versions of adults and gradually develop adult features through a series of molts. They typically inhabit the same environments and eat similar foods as adults.',
    examples: [
        true_bugs,
        grasshoppers,
        dragonflies,
        aphids,
        leafhoppers,
        cicadas
    ],
    context: [
        nymphs_resemble_adults,
        no_pupal_stage,
        gradual_development_through_molts,
        nymphs_and_adults_have_similar_diets
    ]
]).

% ========================
% INSECT FEEDING HABITS
% ========================
frame(insect_feeding, [
    name: herbivore,
    diet_type: plant_feeding,
    description: 'Plant-eating insects consume various plant parts, including leaves, stems, roots, flowers, fruits, and sap. They have adapted mouthparts for chewing, piercing-sucking, or boring into plant tissues. Most garden pest insects are herbivores.',
    examples: [
        caterpillars,
        aphids,
        grasshoppers,
        beetles,
        leafhoppers,
        thrips
    ],
    context: [
        plant_tissue_consumers,
        primary_consumers_in_food_web,
        most_garden_pests,
        high_plant_consumption_relative_to_size
    ]
]).

frame(insect_feeding, [
    name: carnivore,
    diet_type: animal_feeding,
    description: 'Carnivorous insects feed on other insects or small animals. They include predators that actively hunt prey and parasitoids that lay eggs on or in a host insect. Most are beneficial in gardens as they help control pest populations.',
    examples: [
        lady_beetles,
        ground_beetles,
        lacewings,
        assassin_bugs,
        parasitic_wasps,
        predatory_mites
    ],
    context: [
        pest_controllers,
        secondary_consumers_in_food_web,
        beneficial_in_gardens
    ]
]).

frame(insect_feeding, [
    name: scavenger,
    diet_type: detritus_feeding,
    description: 'Scavenging insects feed on decaying organic matter, including dead plants, animals, and waste materials. They play a crucial role in decomposition and nutrient cycling in ecosystems.',
    examples: [
        dung_beetles,
        carrion_beetles,
        fly_larvae,
        some_ants,
        certain_termites
    ],
    context: [
        decomposers,
        nutrient_cyclers,
        waste_processors,
        ecological_recyclers
    ]
]).

frame(insect_feeding, [
    name: omnivore,
    diet_type: mixed_feeding,
    description: 'Omnivorous insects eat both plant and animal matter, switching food sources based on availability. This flexible feeding strategy allows them to survive in changing conditions.',
    examples: [
        earwigs,
        cockroaches,
        ants,
        crickets,
        some_wasps
    ],
    context: [
        adaptable_feeders,
        opportunistic_eaters,
        diet_flexibility
    ]
]).

frame(insect_feeding, [
    name: specialized_feeder,
    diet_type: specialized_feeding,
    description: 'Some insects have highly specialized diets, feeding only on specific plants, specific parts of plants, or specific prey species. This specialization can make them vulnerable to habitat changes but efficient in their particular niche.',
    examples: [
        monarch_caterpillars_on_milkweed,
        fig_wasps_in_figs,
        aphid_midges_on_aphids,
        leaf_miners_in_leaf_tissue,
        scale_insects_on_sap
    ],
    context: [
        host_specific,
        co_evolution_with_host,
        vulnerable_to_habitat_loss,
        highly_efficient_in_niche
    ]
]).

% ========================
% BENEFICIAL INSECTS
% ========================
frame(beneficial_insect, [
    name: pollinators,
    category: pollinator,
    benefits: [crop_pollination, flower_pollination, increased_yields, seed_production],
    target_pests: [],
    description: 'Insects that transfer pollen between flowers, enabling plant reproduction and fruit/seed production. About 75% of flowering plants and 35% of food crops depend on animal pollinators, primarily insects.',
    attraction_methods: [
        plant_diverse_flowering_plants,
        provide_season_long_bloom,
        avoid_pesticides,
        provide_water_sources,
        leave_bare_soil_patches_for_ground_nesting_bees
    ],
    context: [
        essential_for_food_production,
        critical_for_ecosystem_function,
        declining_populations_worldwide
    ]
]).

frame(beneficial_insect, [
    name: predatory_insects,
    category: predator,
    benefits: [pest_control, reduced_crop_damage, reduced_pesticide_need],
    target_pests: [aphids, caterpillars, mites, thrips, whiteflies, small_insects],
    description: 'Insects that hunt and consume pest insects as a primary food source. Both adults and juveniles may be predatory, eating multiple prey individuals throughout their lives.',
    attraction_methods: [
        plant_small_flowered_plants, 
        provide_shelter_with_perennial_plants, 
        maintain_ground_covers, 
        minimize_dust, 
        provide_water_sources,
        avoid_broad_spectrum_pesticides
    ],
    context: [
        natural_pest_control,
        part_of_integrated_pest_management,
        may_supplement_diet_with_pollen_or_nectar
    ]
]).

frame(beneficial_insect, [
    name: parasitoid_insects,
    category: parasitoid,
    benefits: [targeted_pest_control, long_term_population_reduction, pest_specificity],
    target_pests: [caterpillars, aphids, whiteflies, beetle_larvae, true_bugs],
    description: 'Insects that lay eggs in or on host insects. The parasitoid larvae develop by feeding on the host, eventually killing it. Most parasitoid adults feed on nectar, pollen, or honeydew.',
    attraction_methods: [
        plant_small_flowered_plants,
        provide_nectar_sources,
        minimize_pesticide_use,
        maintain_diverse_plantings
    ],
    context: [
        highly_efficient_pest_control,
        often_host_specific,
        adults_and_larvae_have_different_roles
    ]
]).

frame(beneficial_insect, [
    name: common_beneficial_species,
    category: mixed,
    benefits: [pest_control, pollination, soil_health],
    target_pests: [various_garden_pests],
    description: 'Common beneficial insects include lady beetles, lacewings, hover flies, ground beetles, parasitic wasps, predatory mites, minute pirate bugs, and many bee species. Learning to identify these helps gardeners protect and encourage them.',
    attraction_methods: [
        plant_diverse_flowering_plants,
        provide_shelter,
        avoid_pesticides,
        maintain_permanent_refuge_areas
    ],
    context: [
        often_misidentified_as_pests,
        may_resemble_pest_species,
        provide_multiple_ecosystem_services
    ]
]).

% ========================
% PEST MANAGEMENT PRINCIPLES
% ========================
frame(pest_management_principle, [
    name: organic_pest_management,
    category: management_approach,
    description: 'A holistic approach to pest control that focuses on prevention through cultural practices, encouraging natural enemies, using physical barriers, and applying organic-approved sprays only when necessary. The goal is suppression of pest populations to acceptable levels rather than complete eradication.',
    methods: [
        cultural_controls,
        physical_controls,
        biological_controls,
        organic_sprays_and_dusts
    ],
    context: [
        ecosystem_based,
        prevention_focused,
        minimizes_synthetic_inputs,
        works_with_natural_processes
    ]
]).

frame(pest_management_principle, [
    name: cultural_controls,
    category: prevention,
    description: 'Practices that make the garden less hospitable to pests through plant selection, timing, and maintenance. These methods form the foundation of organic pest management.',
    methods: [
        crop_rotation,
        resistant_varieties,
        timing_plantings,
        companion_planting,
        sanitation,
        proper_irrigation,
        healthy_soil_management
    ],
    context: [
        preventative_approach,
        long_term_strategies,
        foundation_of_pest_management
    ]
]).

frame(pest_management_principle, [
    name: physical_controls,
    category: direct_intervention,
    description: 'Methods that directly prevent pests from reaching plants or physically remove them from the garden. These approaches avoid chemical interventions while providing immediate protection.',
    methods: [
        row_covers,
        barriers,
        handpicking,
        water_sprays,
        trapping,
        pruning,
        soil_cultivation
    ],
    context: [
        immediate_protection,
        direct_intervention,
        non_chemical_approaches,
        labor_intensive
    ]
]).

frame(pest_management_principle, [
    name: biological_controls,
    category: biological_intervention,
    description: 'Using living organisms to control pests, including predatory insects, parasitoids, microbial agents like Bacillus thuringiensis, and nematodes. This approach works with natural ecosystem processes.',
    methods: [
        conserving_native_beneficials,
        releasing_purchased_beneficials,
        using_microbial_controls,
        habitat_management,
        applying_parasitic_nematodes
    ],
    context: [
        self_sustaining_when_established,
        working_with_nature,
        minimal_disruption_to_ecosystem,
        requires_understanding_of_life_cycles
    ]
]).

frame(pest_management_principle, [
    name: attracting_beneficials,
    category: habitat_management,
    description: 'Creating garden conditions that attract and sustain beneficial insects through plant selection, habitat features, and management practices.',
    methods: [
        planting_small_flowered_plants,
        establishing_permanent_plantings,
        providing_water_sources,
        minimizing_dust,
        avoiding_pesticides,
        creating_insect_shelters,
        maintaining_ground_covers
    ],
    context: [
        preventative_approach,
        enhances_garden_biodiversity,
        supports_multiple_beneficial_species,
        creates_self-regulating_system
    ]
]).

frame(pest_management_principle, [
    name: coordinated_pest_control,
    category: integrated_approach,
    description: 'Using multiple control methods timed to target different vulnerable stages in a pest's life cycle. This integrated approach increases effectiveness while minimizing pesticide use.',
    methods: [
        targeting_vulnerable_life_stages,
        combining_compatible_control_methods,
        monitoring_pest_populations,
        preventative_and_reactive_measures,
        timed_interventions
    ],
    context: [
        requires_pest_life_cycle_knowledge,
        more_effective_than_single_methods,
        minimizes_pesticide_use,
        adapts_to_pest_development
    ]
]).

% ========================
% SPECIFIC INSECTS
% ========================

% Beneficial Insects
frame(specific_insect, [
    name: aphid_midge,
    type: beneficial,
    scientific_name: 'Aphidoletes aphidimyza',
    description: 'A small fly whose larvae are effective aphid predators.',
    appearance: 'Adults: delicate, long-legged, 1/10" flies, active at night. Larvae: orange maggots, up to 1/8" long. Eggs: minute orange ovals.',
    damage: '',
    host_plants: [],
    life_cycle: 'Females lay eggs among aphids, eggs hatch in 2-3 days; larvae feed on aphids 3-5 days, then burrow into soil to pupate; adults emerge in 2 weeks. Overwinters as larvae in the soil.',
    control_methods: [],
    region: [north_america]
]).

frame(specific_insect, [
    name: lady_beetle,
    type: beneficial,
    scientific_name: 'Family Coccinellidae',
    description: 'Common predatory beetles that feed primarily on aphids and other soft-bodied pests.',
    appearance: 'Adults: shiny, round, 1/4"-3/8" beetles with short legs and antennae. Common species are pale yellow to dark reddish orange with or without black spots; some species solid black or black with red spots. Larvae: spindle-shaped, alligator-like, usually with short spines or knoblike projections on body.',
    damage: '',
    host_plants: [],
    life_cycle: 'In spring, overwintering adults seek food, then lay eggs among aphids or other prey. Eggs hatch in 3-5 days, larvae feed 2-3 weeks, then pupate. Adults emerge in 7-10 days. In fall, local species overwinter as adults in leaf litter.',
    control_methods: [],
    region: [north_america]
]).

frame(specific_insect, [
    name: hover_fly,
    type: beneficial,
    scientific_name: 'Family Syrphidae',
    description: 'Also called flower flies, their larvae are important aphid predators.',
    appearance: 'Adults: yellow- or white-and-black striped, 1/4"-1/2" flies, often seen hovering like hummingbirds over flowers. Larvae: gray or greenish, somewhat translucent, sluglike maggots.',
    damage: '',
    host_plants: [],
    life_cycle: 'Females lay eggs among aphids; eggs hatch in 2-3 days; larvae feed on aphids for 3-4 weeks, then drop to the soil to pupate. Adults emerge after 2 weeks. Two to 4 generations per year.',
    control_methods: [],
    region: [north_america]
]).

frame(specific_insect, [
    name: lacewing,
    type: beneficial,
    scientific_name: 'Chrysoperla spp.',
    description: 'Common general predators in gardens and orchards.',
    appearance: 'Adults: fragile, green or brown, 1/2"-3/4" insects with small heads, large eyes, and netted, transparent wings. Larvae: spindle-shaped, mottled yellow or brown. Eggs: laid on tips of fine stalks.',
    damage: '',
    host_plants: [],
    life_cycle: 'Adults or pupae overwinter; adults emerge in spring to lay eggs. Eggs hatch in 4-7 days; larvae feed for about 3 weeks, then pupate for 5-7 days. Three to 4 generations per year.',
    control_methods: [],
    region: [north_america]
]).

% Pest Insects
frame(specific_insect, [
    name: aphid,
    type: pest,
    scientific_name: 'Family Aphididae',
    description: 'Small sap-sucking insects that can quickly colonize plants.',
    appearance: 'Adults: pear-shaped, 1/16" insects with 2 short tubes projecting backward from the abdomen; long antennae; green, pink, black, dusty gray, or with white fluffy coating; with or without wings. Nymphs: similar to adults.',
    damage: 'Nymphs and adults suck plant sap from most small fruits, vegetables, ornamentals, and fruit and shade trees. Their feeding causes leaf, bud, and flower distortions; severely infested leaves and flowers drop. Fruit that forms on infested branches are misshapen and stunted. Aphids secrete sticky honeydew that supports growth of sooty mold on leaves and fruit. Feeding can spread viral diseases.',
    host_plants: [vegetables, ornamentals, fruit_trees, shade_trees],
    life_cycle: 'Eggs overwinter on woody stems, hatching in spring into stem females, which can give birth continuously to live nymphs without having to mate. Nymphs mature in 1-2 weeks. In fall, males and normal females are born; these mate to produce overwintering eggs.',
    control_methods: [
        'spray_with_water_stream',
        'attract_natural_predators',
        'release_purchased_predators',
        'spray_insecticidal_soap',
        'spray_neem_or_pyrethrin',
        'spray_dormant_oil_for_eggs'
    ],
    region: [north_america]
]).

frame(specific_insect, [
    name: colorado_potato_beetle,
    type: pest,
    scientific_name: 'Leptinotarsa decemlineata',
    description: 'A serious pest of potato and related crops.',
    appearance: 'Adults: yellowish orange, 1/3" beetles with 10 lengthwise, black stripes on wing covers, black spots on thoraxes. Larvae: dark orange, humpbacked, 1/8"-1/2" grubs with a row of black spots along each side. Eggs: bright yellow ovals, standing on end in clusters on undersides of leaves.',
    damage: 'Both adults and larvae chew leaves of potatoes, tomatoes, eggplants, and related plants, including petunias. Feeding can kill small plants and reduces yields of mature plants.',
    host_plants: [potato, tomato, eggplant, petunia],
    life_cycle: 'Overwintering adults emerge from soil in spring to feed on young plants; after feeding, females lay up to 1,000 eggs during their lifespan of several months. Eggs hatch in 4-9 days; larvae feed 2-3 weeks, then pupate in soil. Adults emerge in 5-10 days. Two generations in most areas, 3 generations in southern states.',
    control_methods: [
        'handpick_adults_and_larvae',
        'attract_native_predators',
        'use_straw_mulch',
        'cover_plants_with_row_cover',
        'release_spined_soldier_bugs',
        'apply_parasitic_nematodes',
        'spray_BTSD',
        'spray_neem_or_pyrethrin'
    ],
    region: [north_america]
]).

frame(specific_insect, [
    name: cabbage_looper,
    type: pest,
    scientific_name: 'Trichoplusia ni',
    description: 'Common pest of cabbage and related crops.',
    appearance: 'Adults: gray moths with a silver spot in the middle of each forewing (1 1/4"-2" wingspan). Larvae: green, 1 1/4" caterpillars with 2 white lines down their backs, 1 along each side; they move by looping their bodies.',
    damage: 'Larvae chew large holes in leaves of cabbage family plants and many other vegetable crops. May destroy whole plants.',
    host_plants: [cabbage, broccoli, cauliflower, kale, other_brassicas, many_vegetables],
    life_cycle: 'Moths emerge from overwintering pupae in May and lay eggs on leaves; larvae feed 2-4 weeks, then pupate 10 days in cocoons attached to stems or leaves. Three to 4 generations per year.',
    control_methods: [
        'handpick_larvae',
        'attract_parasitic_wasps',
        'till_crop_residues',
        'spray_BTK',
        'spray_garlic_oil',
        'spray_pyrethrin'
    ],
    region: [united_states, southern_canada]
]).

frame(specific_insect, [
    name: japanese_beetle,
    type: pest,
    scientific_name: 'Popillia japonica',
    description: 'A serious pest of many plants that can completely defoliate susceptible species.',
    appearance: 'Adults: chunky, metallic blue-green, 1/2" beetles with bronze wing covers, long legs, and fine hairs covering body. Larvae: fat, dirty white grubs with brown heads; up to 3/4"; found in sod.',
    damage: 'Adults eat flowers and skeletonize leaves of a broad range of plants; plants may be completely defoliated. Larvae feed on roots of lawn grasses and garden plants.',
    host_plants: [roses, grapes, fruits, vegetables, ornamentals, many_trees_and_shrubs],
    life_cycle: 'Overwintering larvae deep in the soil move toward the surface in spring to feed on roots, pupating in early summer. Adults emerge, feed on plants, and lay eggs in late summer; eggs hatch into larvae that overwinter in soil. One generation occurs every 1-2 years.',
    control_methods: [
        'handpick_beetles',
        'cover_plants_with_row_cover',
        'apply_milky_disease_spores',
        'apply_parasitic_nematodes',
        'attract_native_parasitic_wasps',
        'community_trapping_program',
        'spray_neem'
    ],
    region: [eastern_united_states]
]).

frame(specific_insect, [
    name: codling_moth,
    type: pest,
    scientific_name: 'Cydia pomonella',
    description: 'A serious pest of apples and related fruit trees.',
    appearance: 'Adults: gray-brown moths; forewings with fine, white lines and brown tips, hindwings brown with pale fringes (3/4" wingspan). Larvae: pink or creamy white, 7/8" caterpillars with brown heads.',
    damage: 'Larvae tunnel through apple, apricot, cherry, peach, pear, and plum fruit to center, ruining them.',
    host_plants: [apple, apricot, cherry, peach, pear, plum],
    life_cycle: 'Overwintering larvae pupate in spring; adults emerge when apple trees bloom. Females lay eggs on fruit, leaves, or twigs; larvae burrow into fruit core, usually from blossom end, for 3-5 weeks, then leave fruit to pupate under tree bark or in ground litter. Two to 3 generations per year, 5-8 weeks apart.',
    control_methods: [
        'scrape_loose_bark',
        'spray_dormant_oil',
        'grow_cover_crops',
        'use_pheromone_traps',
        'release_trichogramma_wasps',
        'trap_larvae_in_tree_bands',
        'apply_codling_moth_granulosis_virus',
        'spray_pyrethrin'
    ],
    region: [north_america]
]).

% Add additional insects as needed

frame(specific_insect, [
    name: corn_earworm,
    type: pest,
    scientific_name: 'Helicoverpa zea',
    description: 'Also known as tomato fruitworm, this pest attacks a variety of crops.',
    appearance: 'Adults: tan moths (1 1/2" wingspan). Larvae: 1"-2" long, light yellow, green, pink, or brown; white and dark stripes along sides; yellow heads and black legs.',
    damage: 'Larvae burrow into ripe tomatoes, eat buds, and chew large holes in leaves. In corn, larvae feed on fresh silks, then move down ears eating kernels, leaving trails of excrement. Larvae will also feed on a broad range of vegetable crops, fruits, and flowers.',
    host_plants: [corn, tomato, vegetables, fruits, flowers],
    life_cycle: 'Adults emerge in early spring, migrating long distances to find food, if necessary. Females lay eggs on leaves or on tips of corn ears. Eggs hatch in 3 days, larvae feed 2-4 weeks, then pupate in soil. Adults emerge in 10-25 days. One to 4 generations per year.',
    control_methods: [
        'plant_tight_husk_corn_cultivars',
        'spray_BTK_into_ear_tips',
        'apply_granular_BTK',
        'attract_parasitic_wasps',
        'squirt_parasitic_nematodes_into_ear_tips',
        'squirt_mineral_oil_on_ear_tips',
        'open_husks_and_remove_larvae',
        'release_lacewings_or_pirate_bugs',
        'use_pyrethrin_molasses_bait',
        'use_pheromone_traps',
        'spray_neem'
    ],
    region: [north_america]
]).

frame(specific_insect, [
    name: cucumber_beetle_striped,
    type: pest,
    scientific_name: 'Acalymma vittatum',
    description: 'Common pest of cucurbit crops and carrier of bacterial wilt.',
    appearance: 'Adults: yellow, elongate, 1/5" beetles with black heads and 3 wide black stripes on wing covers. Larvae: slender, white grubs.',
    damage: 'Adults feed on squash family plants, beans, corn, peas, and blossoms of many garden plants. The beetles swarm on seedlings, feeding on leaves and young shoots, often killing plants; they also attack stems and flowers of older plants and eat holes in fruit. Feeding can transmit wilt and mosaic viruses.',
    host_plants: [squash, cucumber, melons, beans, corn, peas, garden_flowers],
    life_cycle: 'Adults overwinter in dense grass or under leaves, emerging in April to early June. They eat weed pollen for 2 weeks, then move to crop plants, laying eggs in soil at base of plants. Eggs hatch in 10 days; larvae burrow into soil, feed on roots for 2-6 weeks, pupate in early August. One to 2 generations per year.',
    control_methods: [
        'cover_seedlings_with_floating_row_cover',
        'hand_pollinate_covered_plants',
        'deep_straw_mulch',
        'apply_parasitic_nematodes',
        'spray_pyrethrin'
    ],
    region: [united_states_east_of_rockies, canada_to_saskatchewan]
]).

frame(specific_insect, [
    name: flea_beetle,
    type: pest,
    scientific_name: 'Family Chrysomelidae',
    description: 'Small beetles that jump like fleas when disturbed, damaging leaves of many crops.',
    appearance: 'Adults: black, brown, or bronze, 1/10" beetles with well-developed hind legs; jump like fleas when disturbed. Larvae: thin, white, legless grubs with brown heads, up to 1/3", living in soil.',
    damage: 'Adults chew numerous small, round holes in leaves of most vegetable crops as well as many flowers and weeds. They are most damaging in early spring. Seedlings may be killed, larger plants usually survive. Larvae feed on plant roots. Adults may spread viral diseases as they feed.',
    host_plants: [vegetables, flowers, weeds],
    life_cycle: 'Overwintering adults emerge from soil in spring; they feed and lay eggs on plant roots, then die by early July. Eggs hatch in 1 week, larvae feed 2-3 weeks, then pupate in soil; adults emerge in 2-3 weeks. One to 4 generations per year.',
    control_methods: [
        'delay_planting',
        'cover_seedlings_with_row_cover',
        'provide_shade_through_interplanting',
        'drench_with_parasitic_nematodes',
        'spray_neem_or_pyrethrin'
    ],
    region: [north_america]
]).

frame(specific_insect, [
    name: cabbage_maggot,
    type: pest,
    scientific_name: 'Delia radicum',
    description: 'Larvae damage roots of cabbage family plants.',
    appearance: 'Adults: gray, 1/5" flies with long legs. Larvae: white, tapering, 1/4" maggots in roots.',
    damage: 'Maggots boring into roots of cabbage family plants ruin root crops and stunt or kill plants. Wounds allow disease organisms to enter roots. First sign of injury is usually wilting in midday.',
    host_plants: [cabbage, broccoli, cauliflower, radish, turnip, other_brassicas],
    life_cycle: 'Adults emerge from overwintering pupae from late March onward. Females lay eggs in soil beside roots; larvae tunnel in roots 3-4 weeks, then pupate in soil for 2-3 weeks. Two to 4 generations per year.',
    control_methods: [
        'cover_seedlings_with_floating_row_cover',
        'set_out_transplants_with_tar_paper_squares',
        'destroy_roots_after_harvesting',
        'apply_parasitic_nematodes',
        'mound_wood_ashes_or_diatomaceous_earth'
    ],
    region: [north_america]
]).

frame(specific_insect, [
    name: braconid_wasp,
    type: beneficial,
    scientific_name: 'Family Braconidae',
    description: 'Important native parasites of many pest insects.',
    appearance: 'Adults: slender, black or brown, 1/10"-1/2" wasps with threadlike waists. Larvae: tiny cream-colored grubs that feed in or on other insects.',
    damage: '',
    host_plants: [],
    life_cycle: 'Females inject eggs into host insects, singly or in large numbers. When larvae complete development, they spin cocoons on or near the dead host, then pupate. Several generations occur per year.',
    control_methods: [],
    region: [north_america]
]).

frame(specific_insect, [
    name: assassin_bug,
    type: beneficial,
    scientific_name: 'Family Reduviidae',
    description: 'General predators that help suppress populations of many insects.',
    appearance: 'Adults: flattened, 1/2" bugs with long, narrow heads and stout, curving beaks, some with flared or sculptured thoraxes; may bite when handled. Nymphs: smaller, similar to adults, wingless, some brightly colored.',
    damage: '',
    host_plants: [],
    life_cycle: 'Adults lay eggs in crevices; nymphs develop until last molt and hibernate in a pre-adult stage, then develop to adults the following June.',
    control_methods: [],
    region: [north_america]
]).

frame(specific_insect, [
    name: parasitic_nematode,
    type: beneficial,
    scientific_name: 'Various species',
    description: 'Beneficial nematodes that parasitize and kill pest insects in the soil.',
    appearance: 'Microscopic to several inches long, translucent unsegmented worms.',
    damage: '',
    host_plants: [],
    life_cycle: 'Most species have a mobile larval stage that moves through the soil or on a film of water to infect the host insect; larvae molt several times to reach the adult stage; adults lay eggs in masses.',
    control_methods: [],
    region: [north_america]
]).

frame(specific_insect, [
    name: japanese_beetle_natural_control,
    type: beneficial,
    scientific_name: 'Various species',
    description: 'Combination of controls that help manage Japanese beetle populations.',
    appearance: 'Various beneficial insects and biological controls.',
    damage: '',
    host_plants: [],
    life_cycle: 'Various life cycles depending on the specific control organism.',
    control_methods: [
        'milky_disease_spores',
        'parasitic_nematodes',
        'parasitic_wasps_and_flies',
        'pheromone_traps'
    ],
    region: [north_america]
]).

% ========================
% RELATIONSHIPS
% ========================

% Predator-prey relationships between beneficial insects and pests
preys_on(aphid_midge, aphid).
preys_on(lady_beetle, aphid).
preys_on(lady_beetle, scale_soft).
preys_on(lady_beetle, mealybug).
preys_on(hover_fly, aphid).
preys_on(lacewing, aphid).
preys_on(lacewing, small_caterpillars).
preys_on(lacewing, insect_eggs).
preys_on(assassin_bug, caterpillars).
preys_on(assassin_bug, flies).
preys_on(braconid_wasp, codling_moth).
preys_on(braconid_wasp, corn_borer).
preys_on(braconid_wasp, cabbageworm).
preys_on(braconid_wasp, hornworm).
preys_on(braconid_wasp, aphid).
preys_on(parasitic_nematode, soil_dwelling_larvae).
preys_on(parasitic_nematode, japanese_beetle).
preys_on(parasitic_nematode, colorado_potato_beetle).
preys_on(parasitic_nematode, cucumber_beetle_striped).
preys_on(spined_soldier_bug, tent_caterpillar).
preys_on(spined_soldier_bug, fall_webworm).
preys_on(spined_soldier_bug, mexican_bean_beetle).
preys_on(tiger_beetle, various_insects).
preys_on(tachinid_fly, cutworm).
preys_on(tachinid_fly, armyworm).
preys_on(tachinid_fly, tent_caterpillar).
preys_on(tachinid_fly, cabbage_looper).
preys_on(tachinid_fly, gypsy_moth).
preys_on(tachinid_fly, squash_bug).
preys_on(tachinid_fly, stink_bug).
preys_on(yellow_jacket, flies).
preys_on(yellow_jacket, caterpillars).

% Crop-pest relationships showing which crops are affected by specific pests
affects_crop(aphid, tomato).
affects_crop(aphid, pepper).
affects_crop(aphid, cabbage).
affects_crop(aphid, lettuce).
affects_crop(aphid, fruit_trees).

affects_crop(colorado_potato_beetle, potato).
affects_crop(colorado_potato_beetle, tomato).
affects_crop(colorado_potato_beetle, eggplant).

affects_crop(cabbage_looper, cabbage).
affects_crop(cabbage_looper, broccoli).
affects_crop(cabbage_looper, cauliflower).
affects_crop(cabbage_looper, kale).

affects_crop(japanese_beetle, rose).
affects_crop(japanese_beetle, grape).
affects_crop(japanese_beetle, raspberry).
affects_crop(japanese_beetle, apple).
affects_crop(japanese_beetle, cherry).

affects_crop(codling_moth, apple).
affects_crop(codling_moth, pear).
affects_crop(codling_moth, plum).

affects_crop(corn_earworm, corn).
affects_crop(corn_earworm, tomato).
affects_crop(corn_earworm, cotton).
affects_crop(corn_earworm, bean).
affects_crop(corn_earworm, pepper).

affects_crop(cucumber_beetle_striped, cucumber).
affects_crop(cucumber_beetle_striped, squash).
affects_crop(cucumber_beetle_striped, melon).
affects_crop(cucumber_beetle_striped, pumpkin).

affects_crop(flea_beetle, eggplant).
affects_crop(flea_beetle, potato).
affects_crop(flea_beetle, cabbage).
affects_crop(flea_beetle, tomato).
affects_crop(flea_beetle, radish).

affects_crop(cabbage_maggot, cabbage).
affects_crop(cabbage_maggot, broccoli).
affects_crop(cabbage_maggot, cauliflower).
affects_crop(cabbage_maggot, radish).
affects_crop(cabbage_maggot, turnip).

affects_crop(southwestern_corn_borer, corn).
affects_crop(southwestern_corn_borer, sorghum).

affects_crop(squash_bug, squash).
affects_crop(squash_bug, pumpkin).
affects_crop(squash_bug, cucumber).
affects_crop(squash_bug, melon).

affects_crop(squash_vine_borer, squash).
affects_crop(squash_vine_borer, pumpkin).
affects_crop(squash_vine_borer, cucumber).
affects_crop(squash_vine_borer, melon).
affects_crop(squash_vine_borer, gourd).

affects_crop(stink_bug, cabbage_family_crops).
affects_crop(stink_bug, squash).
affects_crop(stink_bug, bean).
affects_crop(stink_bug, pea).
affects_crop(stink_bug, corn).
affects_crop(stink_bug, tomato).
affects_crop(stink_bug, peach).

affects_crop(strawberry_root_weevil, strawberry).
affects_crop(strawberry_root_weevil, raspberry).
affects_crop(strawberry_root_weevil, grape).
affects_crop(strawberry_root_weevil, apple).
affects_crop(strawberry_root_weevil, peach).

affects_crop(tomato_hornworm, tomato).
affects_crop(tomato_hornworm, potato).
affects_crop(tomato_hornworm, pepper).
affects_crop(tomato_hornworm, eggplant).

affects_crop(whitefly, tomato).
affects_crop(whitefly, cucumber).
affects_crop(whitefly, citrus).
affects_crop(whitefly, ornamentals).

affects_crop(wireworm, potato).
affects_crop(wireworm, corn).
affects_crop(wireworm, flower_bulbs).
affects_crop(wireworm, vegetable_seedlings).

% Attraction methods for beneficial insects
attracts(flower_plants, lady_beetle).
attracts(flower_plants, hover_fly).
attracts(flower_plants, lacewing).
attracts(flower_plants, braconid_wasp).
attracts(dill, braconid_wasp).
attracts(parsley, braconid_wasp).
attracts(yarrow, braconid_wasp).
attracts(goldenrod, minute_pirate_bug).
attracts(daisy, minute_pirate_bug).
attracts(yarrow, minute_pirate_bug).
attracts(alfalfa, minute_pirate_bug).
attracts(goldenrod, soldier_beetle).
attracts(milkweed, soldier_beetle).
attracts(hydrangea, soldier_beetle).
attracts(catnip, soldier_beetle).
attracts(dill, tachinid_fly).
attracts(parsley, tachinid_fly).
attracts(sweet_clover, tachinid_fly).
attracts(flowering_herbs, tachinid_fly).
attracts(permanent_plantings, tiger_beetle).
attracts(permanent_beds, spined_soldier_bug).
attracts(perennial_plantings, spined_soldier_bug).

% Organic management practices effective against specific pests
controls(floating_row_cover, cabbage_maggot).
controls(floating_row_cover, flea_beetle).
controls(floating_row_cover, cucumber_beetle_striped).
controls(floating_row_cover, japanese_beetle).
controls(floating_row_cover, squash_bug).
controls(floating_row_cover, squash_vine_borer).
controls(floating_row_cover, strawberry_root_weevil).
controls(floating_row_cover, tarnished_plant_bug).

controls(crop_rotation, colorado_potato_beetle).
controls(crop_rotation, cucumber_beetle_striped).
controls(crop_rotation, cabbage_maggot).
controls(crop_rotation, southwestern_corn_borer).

controls(handpicking, colorado_potato_beetle).
controls(handpicking, japanese_beetle).
controls(handpicking, cabbage_looper).
controls(handpicking, squash_bug).
controls(handpicking, tomato_hornworm).
controls(handpicking, tent_caterpillar).
controls(handpicking, garden_webworm).

controls(btk, cabbage_looper).
controls(btk, corn_earworm).
controls(btk, codling_moth).
controls(btk, tent_caterpillar).
controls(btk, fall_webworm).
controls(btk, garden_webworm).
controls(btk, tomato_hornworm).
controls(btk, spruce_budworm).
controls(btk, tussock_moth).
controls(btk, woollybear).

controls(parasitic_nematodes, japanese_beetle).
controls(parasitic_nematodes, colorado_potato_beetle).
controls(parasitic_nematodes, flea_beetle).
controls(parasitic_nematodes, cucumber_beetle_striped).
controls(parasitic_nematodes, strawberry_root_weevil).
controls(parasitic_nematodes, wireworm).

controls(beneficial_insects, aphid).
controls(beneficial_insects, cabbage_looper).
controls(beneficial_insects, codling_moth).
controls(beneficial_insects, japanese_beetle).
controls(beneficial_insects, stink_bug).
controls(beneficial_insects, whitefly).

controls(trap_crops, cucumber_beetle_striped).
controls(trap_crops, flea_beetle).

controls(early_planting, southwestern_corn_borer).

controls(resistant_cultivars, southwestern_corn_borer).

controls(sanitation, vinegar_fly).
controls(sanitation, fall_webworm).
controls(sanitation, wireworm).

% Helper rules for finding appropriate control methods
potential_predator(Pest, Predator) :- preys_on(Predator, Pest).
potential_control_method(Pest, Method) :- controls(Method, Pest).
crop_pest(Crop, Pest) :- affects_crop(Pest, Crop).
beneficial_attractor(Beneficial, Plant) :- attracts(Plant, Beneficial).

% Additional helper rules
common_pests_of(Crop, PestList) :- findall(Pest, affects_crop(Pest, Crop), PestList).
control_methods_for(Pest, MethodList) :- findall(Method, controls(Method, Pest), MethodList).
predators_of(Pest, PredatorList) :- findall(Predator, preys_on(Predator, Pest), PredatorList).
plants_to_attract(Beneficial, PlantList) :- findall(Plant, attracts(Plant, Beneficial), PlantList).

% Additional relationships for newly added insects
preys_on(spined_soldier_bug, tent_caterpillar).
preys_on(spined_soldier_bug, fall_webworm).
preys_on(spined_soldier_bug, mexican_bean_beetle).
preys_on(tiger_beetles, various_insects).
preys_on(tachinid_fly, cutworm).
preys_on(tachinid_fly, armyworm).
preys_on(tachinid_fly, tent_caterpillar).
preys_on(tachinid_fly, cabbage_looper).
preys_on(tachinid_fly, gypsy_moth).
preys_on(tachinid_fly, squash_bug).
preys_on(tachinid_fly, stink_bug).
preys_on(yellow_jacket, flies).
preys_on(yellow_jacket, caterpillars).

affects_crop(southwestern_corn_borer, corn).
affects_crop(southwestern_corn_borer, sorghum).

affects_crop(squash_bug, squash).
affects_crop(squash_bug, pumpkin).
affects_crop(squash_bug, cucumber).
affects_crop(squash_bug, melon).

affects_crop(squash_vine_borer, squash).
affects_crop(squash_vine_borer, pumpkin).
affects_crop(squash_vine_borer, cucumber).
affects_crop(squash_vine_borer, melon).
affects_crop(squash_vine_borer, gourd).

affects_crop(stink_bug, cabbage_family_crops).
affects_crop(stink_bug, squash).
affects_crop(stink_bug, bean).
affects_crop(stink_bug, pea).
affects_crop(stink_bug, corn).
affects_crop(stink_bug, tomato).
affects_crop(stink_bug, peach).

affects_crop(strawberry_root_weevil, strawberry).
affects_crop(strawberry_root_weevil, raspberry).
affects_crop(strawberry_root_weevil, grape).
affects_crop(strawberry_root_weevil, apple).
affects_crop(strawberry_root_weevil, peach).

affects_crop(tomato_hornworm, tomato).
affects_crop(tomato_hornworm, potato).
affects_crop(tomato_hornworm, pepper).
affects_crop(tomato_hornworm, eggplant).

affects_crop(whitefly, tomato).
affects_crop(whitefly, cucumber).
affects_crop(whitefly, citrus).
affects_crop(whitefly, ornamentals).

affects_crop(wireworm, potato).
affects_crop(wireworm, corn).
affects_crop(wireworm, flower_bulbs).
affects_crop(wireworm, vegetable_seedlings).

attracts(dill, tachinid_fly).
attracts(parsley, tachinid_fly).
attracts(sweet_clover, tachinid_fly).
attracts(flowering_herbs, tachinid_fly).
attracts(permanent_plantings, tiger_beetle).
attracts(permanent_beds, spined_soldier_bug).
attracts(perennial_plantings, spined_soldier_bug).

controls(floating_row_cover, squash_bug).
controls(floating_row_cover, squash_vine_borer).
controls(floating_row_cover, strawberry_root_weevil).
controls(floating_row_cover, tarnished_plant_bug).

controls(crop_rotation, southwestern_corn_borer).

controls(handpicking, squash_bug).
controls(handpicking, tomato_hornworm).
controls(handpicking, tent_caterpillar).
controls(handpicking, garden_webworm).

controls(btk, tent_caterpillar).
controls(btk, fall_webworm).
controls(btk, garden_webworm).
controls(btk, tomato_hornworm).
controls(btk, spruce_budworm).
controls(btk, tussock_moth).
controls(btk, woollybear).

controls(parasitic_nematodes, strawberry_root_weevil).
controls(parasitic_nematodes, wireworm).

controls(beneficial_insects, japanese_beetle).
controls(beneficial_insects, stink_bug).
controls(beneficial_insects, whitefly).

controls(early_planting, southwestern_corn_borer).

controls(resistant_cultivars, southwestern_corn_borer).

controls(sanitation, vinegar_fly).
controls(sanitation, fall_webworm).
controls(sanitation, wireworm).

% Advanced helper rules for more complex queries
common_pests_of(Crop, PestList) :- findall(Pest, affects_crop(Pest, Crop), PestList).
control_methods_for(Pest, MethodList) :- findall(Method, controls(Method, Pest), MethodList).
predators_of(Pest, PredatorList) :- findall(Predator, preys_on(Predator, Pest), PredatorList).
plants_to_attract(Beneficial, PlantList) :- findall(Plant, attracts(Plant, Beneficial), PlantList).

% ========================
% NATIVE BENEFICIAL INSECTS
% ========================
% Information on important native beneficial insects and their roles in pest management

frame(beneficial_insect, [
    name: aphid_midge,
    category: predator,
    scientific_name: 'Aphidoletes aphidimyza',
    benefits: [aphid_control, population_reduction],
    target_pests: [aphids],
    description: 'Very common, globally distributed, and hardy nearly to the Arctic circle. Especially attracted to aphids in roses, shrubs, and orchard trees.',
    attraction_methods: [nectar_producing_plants, wind_shelter, water_sources],
    context: [organic_gardening, ipm, natural_predator]
]).

frame(beneficial_insect, [
    name: assassin_bugs,
    category: predator,
    scientific_name: 'Family Reduviidae',
    benefits: [pest_control, population_reduction],
    target_pests: [caterpillars, flies, various_insects],
    description: 'Robust, voracious insects, with strong beaks to attack prey; will squeak when handled; can inflict a painful bite.',
    attraction_methods: [permanent_plantings, shelter],
    context: [organic_gardening, ipm, natural_predator]
]).

frame(beneficial_insect, [
    name: bigeyed_bugs,
    category: predator,
    scientific_name: 'Geocoris spp.',
    benefits: [pest_control, population_reduction],
    target_pests: [aphids, small_caterpillars, leafhoppers, spider_mites, tarnished_plant_bugs],
    description: 'They may resemble tarnished plant bugs or chinch bugs; their big black eyes are a distinctive trait.',
    attraction_methods: [pigweed, goldenrod, alfalfa, clover, soybeans],
    context: [organic_gardening, ipm, natural_predator]
]).

frame(beneficial_insect, [
    name: braconid_wasps,
    category: parasitoid,
    scientific_name: 'Family Braconidae',
    benefits: [pest_control, population_reduction],
    target_pests: [aphids, armyworms, beetle_larvae, codling_moths, european_corn_borers, flies, gypsy_moths, imported_cabbageworms, caterpillars],
    description: 'Rigidly mummified aphids or dying caterpillars with white cocoons stuck to their backs are signs that braconids have been at work.',
    attraction_methods: [small_flowered_plants, nectar_producing_plants],
    context: [organic_gardening, ipm, parasitic_wasp]
]).

frame(beneficial_insect, [
    name: damsel_bugs,
    category: predator,
    scientific_name: 'Family Nabidae',
    benefits: [pest_control, population_reduction],
    target_pests: [aphids, small_caterpillars, leafhoppers, plant_bugs, thrips, treehoppers],
    description: 'These gray or brown bugs are common and important predators in orchards and alfalfa fields (where you can collect them for your garden).',
    attraction_methods: [alfalfa_fields, collect_and_transfer],
    context: [organic_gardening, ipm, natural_predator]
]).

frame(beneficial_insect, [
    name: ground_beetles,
    category: predator,
    scientific_name: 'Family Carabidae',
    benefits: [pest_control, population_reduction],
    target_pests: [cabbage_root_maggots, cutworms, slugs, snails, colorado_potato_beetle_larvae, gypsy_moths, tent_caterpillars],
    description: 'Exceptionally long-lived (adults live up to 2 years), most active at night.',
    attraction_methods: [permanent_beds, sod_pathways, limited_weeds, minimal_tillage, white_clover],
    context: [organic_gardening, ipm, soil_predator]
]).

frame(beneficial_insect, [
    name: hover_flies,
    category: predator,
    scientific_name: 'Family Syrphidae',
    benefits: [pest_control, population_reduction],
    target_pests: [aphids],
    description: 'These insects hover over flowers and dart away like miniature hummingbirds. They often lay eggs in young aphid colonies to ensure that larvae will have enough prey.',
    attraction_methods: [pollen_producing_flowers, nectar_producing_flowers, wild_carrots, yarrow, avoid_pesticides],
    context: [organic_gardening, ipm, natural_predator]
]).

frame(beneficial_insect, [
    name: ichneumon_wasps,
    category: parasitoid,
    scientific_name: 'Family Ichneumonidae',
    benefits: [pest_control, population_reduction],
    target_pests: [caterpillars, sawfly_larvae, beetle_larvae],
    description: 'Although most ichneumon wasps are very small, some are frighteningly large with long, threadlike ovipositors trailing behind; they cannot sting people.',
    attraction_methods: [pollen_producing_flowers, nectar_producing_flowers, flowering_cover_crops],
    context: [organic_gardening, ipm, parasitic_wasp]
]).

frame(beneficial_insect, [
    name: lacewings,
    category: predator,
    scientific_name: 'Chrysoperla (=Chrysopa) spp.',
    benefits: [pest_control, population_reduction],
    target_pests: [aphids, mealybugs, thrips, small_caterpillars, mites, moth_eggs, scales],
    description: 'The delicate adults flutter erratically in a zigzag flight through the garden at dusk; their voracious larvae are known as aphid lions.',
    attraction_methods: [pollen_producing_plants, nectar_producing_plants, dandelions, goldenrod, water_sources],
    context: [organic_gardening, ipm, natural_predator]
]).

frame(beneficial_insect, [
    name: lady_beetles,
    category: predator,
    scientific_name: 'Family Coccinellidae',
    benefits: [pest_control, population_reduction],
    target_pests: [aphids, mealybugs, soft_scales, spider_mites],
    description: 'Lady beetles abound in many sizes and colors, including solid black, ash gray, and yellow or orange with black spots or irregular blotches.',
    attraction_methods: [pollen_producing_flowers, nectar_producing_flowers, dandelions, wild_carrots, yarrow, protect_juveniles],
    context: [organic_gardening, ipm, natural_predator]
]).

frame(beneficial_insect, [
    name: minute_pirate_bug,
    category: predator,
    scientific_name: 'Orius tristicolor',
    benefits: [pest_control, population_reduction],
    target_pests: [small_caterpillars, leafhopper_nymphs, spider_mites, thrips, insect_eggs],
    description: 'These plentiful, black-and-white harlequin bugs are easy to spot. Look for them in corn silks and stinging nettles.',
    attraction_methods: [alfalfa, pollen_producing_plants, goldenrod, yarrow],
    context: [organic_gardening, ipm, natural_predator]
]).

frame(beneficial_insect, [
    name: rove_beetles,
    category: predator,
    scientific_name: 'Family Staphylinidae',
    benefits: [pest_control, population_reduction, soil_health],
    target_pests: [aphids, fly_eggs, maggots, nematodes, springtails, cabbage_root_maggots, fly_larvae],
    description: 'Often mistaken for earwigs, rove beetles are usually smaller and have no pincers; more than 3,000 species in North America.',
    attraction_methods: [permanent_plantings, cover_crops, mulch, permanent_pathways],
    context: [organic_gardening, ipm, soil_predator]
]).

frame(beneficial_insect, [
    name: soldier_beetles,
    category: predator,
    scientific_name: 'Family Cantharidae',
    benefits: [pest_control, population_reduction],
    target_pests: [aphids, beetle_larvae, cucumber_beetles, caterpillars, grasshopper_eggs],
    description: 'Unlike most beetles, soldier beetles have leathery rather than hard wing covers.',
    attraction_methods: [pollen_rich_plants, permanent_plantings],
    context: [organic_gardening, ipm, natural_predator]
]).

frame(beneficial_insect, [
    name: spined_soldier_bug,
    category: predator,
    scientific_name: 'Podisus maculiventris',
    benefits: [pest_control, population_reduction],
    target_pests: [fall_armyworms, hairless_caterpillars, tent_caterpillars, sawfly_larvae, colorado_potato_beetle_larvae, mexican_bean_beetle_larvae],
    description: 'These resemble stink bugs, but spined soldier bugs have sharp points on the "shoulders" of the thorax.',
    attraction_methods: [permanent_perennial_beds],
    context: [organic_gardening, ipm, natural_predator]
]).

frame(beneficial_insect, [
    name: tachinid_flies,
    category: parasitoid,
    scientific_name: 'Family Tachinidae',
    benefits: [pest_control, population_reduction],
    target_pests: [caterpillars, armyworms, cabbage_loopers, cutworms, gypsy_moths, tent_caterpillars, japanese_beetles, may_beetles, sawflies, squash_bugs],
    description: 'One of the largest and most beneficial groups of flies, they are often mistaken for houseflies.',
    attraction_methods: [pollen_rich_plants, nectar_rich_plants, goldenrod, wild_carrots, pigweed, preserve_parasitized_caterpillars],
    context: [organic_gardening, ipm, parasitic_fly]
]).

frame(beneficial_insect, [
    name: tiger_beetles,
    category: predator,
    scientific_name: 'Family Cicindelidae',
    benefits: [pest_control, population_reduction],
    target_pests: [ants, aphids, beetles, caterpillars, flies, grasshoppers, spiders],
    description: 'These insects are slow developers; larvae spend 2-3 years in their burrows before becoming spectacularly beautiful adults with bright, iridescent colors.',
    attraction_methods: [permanent_garden_beds, limited_night_lighting],
    context: [organic_gardening, ipm, natural_predator]
]).

% Add additional relationship predicates to connect these insects with their target pests

% Predator-prey relationships for aphid_midge
preys_on(aphid_midge, aphids).

% Predator-prey relationships for assassin_bugs
preys_on(assassin_bugs, caterpillars).
preys_on(assassin_bugs, flies).

% Predator-prey relationships for bigeyed_bugs
preys_on(bigeyed_bugs, aphids).
preys_on(bigeyed_bugs, small_caterpillars).
preys_on(bigeyed_bugs, leafhoppers).
preys_on(bigeyed_bugs, spider_mites).
preys_on(bigeyed_bugs, tarnished_plant_bugs).

% Predator-prey relationships for braconid_wasps
parasitizes(braconid_wasps, aphids).
parasitizes(braconid_wasps, armyworms).
parasitizes(braconid_wasps, beetle_larvae).
parasitizes(braconid_wasps, codling_moths).
parasitizes(braconid_wasps, european_corn_borers).
parasitizes(braconid_wasps, imported_cabbageworms).

% Predator-prey relationships for damsel_bugs
preys_on(damsel_bugs, aphids).
preys_on(damsel_bugs, small_caterpillars).
preys_on(damsel_bugs, leafhoppers).
preys_on(damsel_bugs, plant_bugs).
preys_on(damsel_bugs, thrips).
preys_on(damsel_bugs, treehoppers).

% Predator-prey relationships for ground_beetles
preys_on(ground_beetles, cabbage_root_maggots).
preys_on(ground_beetles, cutworms).
preys_on(ground_beetles, slugs).
preys_on(ground_beetles, snails).
preys_on(ground_beetles, colorado_potato_beetle_larvae).
preys_on(ground_beetles, gypsy_moths).
preys_on(ground_beetles, tent_caterpillars).

% Predator-prey relationships for hover_flies
preys_on(hover_flies, aphids).

% Predator-prey relationships for ichneumon_wasps
parasitizes(ichneumon_wasps, caterpillars).
parasitizes(ichneumon_wasps, sawfly_larvae).
parasitizes(ichneumon_wasps, beetle_larvae).

% Predator-prey relationships for lacewings
preys_on(lacewings, aphids).
preys_on(lacewings, mealybugs).
preys_on(lacewings, thrips).
preys_on(lacewings, small_caterpillars).
preys_on(lacewings, mites).
preys_on(lacewings, moth_eggs).
preys_on(lacewings, scales).

% Predator-prey relationships for lady_beetles
preys_on(lady_beetles, aphids).
preys_on(lady_beetles, mealybugs).
preys_on(lady_beetles, soft_scales).
preys_on(lady_beetles, spider_mites).

% Predator-prey relationships for minute_pirate_bug
preys_on(minute_pirate_bug, small_caterpillars).
preys_on(minute_pirate_bug, leafhopper_nymphs).
preys_on(minute_pirate_bug, spider_mites).
preys_on(minute_pirate_bug, thrips).
preys_on(minute_pirate_bug, insect_eggs).

% Predator-prey relationships for rove_beetles
preys_on(rove_beetles, aphids).
preys_on(rove_beetles, fly_eggs).
preys_on(rove_beetles, maggots).
preys_on(rove_beetles, nematodes).
preys_on(rove_beetles, springtails).
preys_on(rove_beetles, cabbage_root_maggots).

% Predator-prey relationships for soldier_beetles
preys_on(soldier_beetles, aphids).
preys_on(soldier_beetles, beetle_larvae).
preys_on(soldier_beetles, cucumber_beetles).
preys_on(soldier_beetles, caterpillars).
preys_on(soldier_beetles, grasshopper_eggs).

% Predator-prey relationships for spined_soldier_bug
preys_on(spined_soldier_bug, fall_armyworms).
preys_on(spined_soldier_bug, tent_caterpillars).
preys_on(spined_soldier_bug, sawfly_larvae).
preys_on(spined_soldier_bug, colorado_potato_beetle_larvae).
preys_on(spined_soldier_bug, mexican_bean_beetle_larvae).

% Predator-prey relationships for tachinid_flies
parasitizes(tachinid_flies, caterpillars).
parasitizes(tachinid_flies, armyworms).
parasitizes(tachinid_flies, cabbage_loopers).
parasitizes(tachinid_flies, cutworms).
parasitizes(tachinid_flies, gypsy_moths).
parasitizes(tachinid_flies, tent_caterpillars).
parasitizes(tachinid_flies, japanese_beetles).
parasitizes(tachinid_flies, sawflies).
parasitizes(tachinid_flies, squash_bugs).

% Predator-prey relationships for tiger_beetles
preys_on(tiger_beetles, ants).
preys_on(tiger_beetles, aphids).
preys_on(tiger_beetles, beetles).
preys_on(tiger_beetles, caterpillars).
preys_on(tiger_beetles, flies).
preys_on(tiger_beetles, grasshoppers).
preys_on(tiger_beetles, spiders).

% Helper predicate to find beneficial insects that attack a specific pest
beneficial_insects_for(Pest, BeneficialList) :-
    findall(Beneficial, 
           (preys_on(Beneficial, Pest); parasitizes(Beneficial, Pest)), 
           BeneficialList).

% Helper predicate to find methods to attract a specific beneficial insect
attraction_methods_for(Beneficial, MethodList) :-
    frame(beneficial_insect, [name:Beneficial, attraction_methods:MethodList, _]).

% Helper predicate to find all beneficial insects in a category
beneficials_by_category(Category, BeneficialList) :-
    findall(Beneficial, 
           frame(beneficial_insect, [name:Beneficial, category:Category, _]), 
           BeneficialList). 
% ========================
% ORGANIC SPRAYS AND DUSTS KNOWLEDGE BASE
% ========================
% Contains information about organic sprays and dusts for pest management
% Based on The Organic Gardeners Handbook of Natural Insect information

% Ensure compatibility with existing knowledge bases
:- discontiguous(frame/2).

% ========================
% FRAME TEMPLATES
% ========================
frame(organic_spray, [
    name: atom,
    category: atom,
    description: string,
    protection_offered: string,
    target_pests: list(atom),
    application_method: string,
    precautions: string,
    context: list(atom)
]).

frame(spray_safety, [
    name: atom,
    category: atom,
    description: string,
    guidelines: list(string),
    context: list(atom)
]).

% ========================
% SPRAY SAFETY GUIDELINES
% ========================
frame(spray_safety, [
    name: spray_safely,
    category: safety_guidelines,
    description: 'Guidelines for safe application of organic sprays and dusts to ensure effectiveness while protecting the applicator, beneficial insects, and the environment.',
    guidelines: [
        'Wait for calm weather. Applying under windy conditions causes drift where not wanted and increases risk of inhalation or eye contact.',
        'Harvest ripe produce before spraying to avoid having to enter treated areas later.',
        'Dress properly: wear long pants, shoes and socks, long-sleeved shirt, face mask (respirator if label advises), goggles, and rubber gloves.',
        'Precheck equipment for proper function before loading with pesticide.',
        'Mix only what you need to avoid disposal problems.',
        'Apply when beneficials are inactive, often mid-morning should be avoided.',
        'Spray and dust early morning or evening to avoid plant injury and pesticide breakdown from heat and sun.',
        'Cover plants thoroughly, including upper and lower leaf surfaces and mulch where pests might hide.',
        'Dispose of leftover solution by diluting with water, placing in sun to degrade, then disposing away from water sources.',
        'Change clothes and wash hands and face after application, shower if solution was spilled.',
        'Store products in original containers in cool, dark places out of reach of children.',
        'Apply only to plants specified on the label at recommended rates.'
    ],
    context: [organic_gardening, ipm, safety_protocol, application_guidelines]
]).

frame(spray_safety, [
    name: application_methods,
    category: application_guidelines,
    description: 'Techniques for effectively applying different types of organic sprays and dusts to target pests while minimizing impact on beneficial insects.',
    guidelines: [
        'For small jobs, use a hand-held trigger sprayer, keeping separate sprayers for non-poisonous sprays vs. biological/botanical pesticides.',
        'For larger spray jobs, select a pump-action pressure sprayer sized appropriately for the area.',
        'Clean and dry nozzles and filters after each use.',
        'For non-poisonous dusts like diatomaceous earth, punch small holes in paper bag or use an old sock tied at the end.',
        'For biological or botanical pesticide dusts, use a specialized duster to keep dust away from your face.',
        'Apply dusts when plants are wet from dew or after watering to help dust adhere.',
        'Apply pressure when dusting to create a cloud around plant leaves for better coverage.'
    ],
    context: [organic_gardening, ipm, application_techniques]
]).

% ========================
% GENERAL ORGANIC SPRAYS
% ========================
frame(organic_spray, [
    name: all_purpose_insect_spray,
    category: homemade_spray,
    description: 'A combination of common kitchen ingredients with repellent and insecticidal properties.',
    protection_offered: 'Effective against many leaf-eating pests in the garden.',
    target_pests: [leaf_eating_insects, various_garden_pests],
    application_method: 'Chop/grind 1 garlic bulb and 1 small onion. Add 1 teaspoon powdered cayenne pepper and mix with 1 quart water. Steep 1 hour, strain, then add 1 tablespoon liquid dish soap. Spray thoroughly, covering undersides of leaves. Store for up to 1 week refrigerated in labeled container.',
    precautions: 'Keep away from eyes and nose, wear rubber gloves as mixture can cause painful burning.',
    context: [organic_gardening, homemade_remedy, broad_spectrum_control]
]).

frame(organic_spray, [
    name: soap_spray,
    category: contact_insecticide,
    description: 'Solution using fatty acids from soaps that penetrate insect cuticles, causing cell membranes to collapse and leak, resulting in dehydration.',
    protection_offered: 'Controls soft-bodied insects like aphids, mealybugs, whiteflies, as well as chiggers, earwigs, fleas, mites, scales, thrips, and ticks. Less effective on caterpillars and beetles.',
    target_pests: [aphids, mealybugs, whiteflies, earwigs, fleas, mites, scales, thrips, ticks],
    application_method: 'Mix 1 teaspoon to several tablespoons of pure soap per gallon of water. Start with lower concentration. Spray when first pest colonies develop and again when populations increase. Spray during cool, humid weather for better results.',
    precautions: 'Test on a few leaves before treating whole plants. Plants with thin cuticles like beans, Chinese cabbage, cucumbers, ferns, gardenias, Japanese maples, nasturtiums, and young peas are easily damaged. Use no more than 3 successive sprays on any plant. Will kill beneficial insects along with pests.',
    context: [organic_gardening, commercial_product, soft_bodied_insect_control]
]).

frame(organic_spray, [
    name: oil_spray,
    category: smothering_agent,
    description: 'Modern horticultural oils that are lighter and contain fewer impurities than traditional dormant oils, allowing year-round use on various plants.',
    protection_offered: 'Controls aphids, mealybugs, mites, and scales on fruit, nut, ornamental, and shade trees while having minimal impact on beneficial insects.',
    target_pests: [aphids, mealybugs, mites, scales],
    application_method: 'For dormant application in early spring, use 3% solution (1/3 cup oil per gallon of water). For plants in full leaf, use 2% solution (1/4 cup oil per gallon). For sensitive plants, use 1% solution (2.5 tablespoons per gallon). Spray until leaves are well-coated with some dripping. Apply at weekly intervals as needed.',
    precautions: 'Do not spray water-stressed plants unless irrigated thoroughly first. Avoid using on weakened plants or in temperatures above 85°F or below freezing. Never apply within 1 month before or after sulfur application. Apply early morning or evening to avoid direct sunlight.',
    context: [organic_gardening, commercial_product, smothering_control]
]).

frame(organic_spray, [
    name: diatomaceous_earth,
    category: mechanical_insecticide,
    description: 'Fossilized silica shells of algae called diatoms with sharp projections that penetrate insect cuticles and absorb waxy coatings, causing dehydration.',
    protection_offered: 'Controls crawling pests like slugs and snails, soft-bodied pests like aphids, caterpillars, leafhoppers, and thrips. Excellent for stored grain and seeds.',
    target_pests: [slugs, snails, aphids, caterpillars, leafhoppers, thrips],
    application_method: 'Apply as dust only in problem areas. Place around bases of seedlings to control soil-dwelling pests. Dust foliage but avoid flowers. Apply when plants are wet from dew or after watering. Can be mixed with liquid soap and water to make a paint-on slurry for tree trunks.',
    precautions: 'Wear a dust mask when applying to avoid inhalation. Do not confuse with pool-grade DE which is chemically treated and poses severe respiratory hazard. Nonselective and will kill beneficial insects. Rain will dilute or wash away DE.',
    context: [organic_gardening, commercial_product, physical_control]
]).

% ========================
% BOTANICAL INSECTICIDES
% ========================
frame(organic_spray, [
    name: pyrethrin,
    category: botanical_insecticide,
    description: 'Insecticidal compounds extracted from pyrethrum daisies (Chrysanthemum cinerariifolium and C. coccineum) that kill insects on contact by attacking their nervous systems.',
    protection_offered: 'Broad-spectrum insect nerve poison effective against aphids, cabbage loopers, celery leaftiers, codling moths, Colorado potato beetles, leafhoppers, Mexican bean beetles, spider mites, stink bugs, thrips, tomato pinworms, and whiteflies.',
    target_pests: [aphids, cabbage_loopers, colorado_potato_beetle, leafhoppers, mexican_bean_beetle, spider_mites, stink_bugs, thrips, whiteflies],
    application_method: 'Apply as spray or dust according to label directions. For homemade pyrethrin, collect daisy blooms at full bloom, dry completely, grind to powder, and mix with liquid soap and water. Alternatively, extract in alcohol overnight and dilute with water for spray.',
    precautions: 'Moderately toxic to mammals. Will kill beneficial insects including lady beetles. Some people may have allergic reactions, especially those with hay fever. Works best at temperatures below 80°F. Many commercial products contain piperonyl butoxide synergist which may have safety concerns.',
    context: [organic_gardening, commercial_product, broad_spectrum_insecticide]
]).

frame(organic_spray, [
    name: neem,
    category: botanical_insecticide,
    description: 'Insecticide extracted from neem tree (Azadirachta indica) seeds that acts as repellent, growth regulator, and insect poison by making plants unpalatable and inhibiting molting and egg-laying.',
    protection_offered: 'Controls aphids, gypsy moths, leafminers, loopers, mealybugs, thrips, whiteflies, Colorado potato beetles, corn earworms, cucumber beetles, flea beetles, Mexican bean beetles, and pest mites.',
    target_pests: [aphids, gypsy_moths, leafminers, loopers, mealybugs, thrips, whiteflies, colorado_potato_beetle, corn_earworm, cucumber_beetles, flea_beetles, mexican_bean_beetle, mites],
    application_method: 'Apply according to label directions or make homemade spray by shredding neem fruit and soaking in water overnight. Cover plants thoroughly and evenly. Reapply every 5-7 days during growing season as neem breaks down quickly in sunlight and soil.',
    precautions: 'Almost nontoxic to mammals and biodegradable. Seeds and extracts are poisonous if consumed. Effect on beneficial insects is usually minimal since neem must be ingested to be toxic, but can harm parasites of insects that have eaten neem-sprayed foliage.',
    context: [organic_gardening, commercial_product, systemic_insecticide]
]).

frame(organic_spray, [
    name: garlic_oil,
    category: botanical_repellent,
    description: 'Mixture of garlic, mineral oil and soap that has antibiotic, antifungal, and insecticidal properties.',
    protection_offered: 'Controls aphids, imported cabbageworms, leafhoppers, larval mosquitoes, squash bugs, whiteflies, some fungi, and some nematodes.',
    target_pests: [aphids, cabbageworms, leafhoppers, mosquito_larvae, squash_bugs, whiteflies],
    application_method: 'Soak 3 ounces of finely minced garlic cloves in 2 teaspoons mineral oil for at least 24 hours. Add 1 pint of water with 1/4 ounce liquid dish soap mixed in. Strain, add 2 more cups water. Use 1-2 tablespoons of concentrate with 1 pint water for spray.',
    precautions: 'Test on a few leaves to check for injury from oil and soap components; damage may take 2-3 days to appear. Generally safe but use normal precautions for sprays.',
    context: [organic_gardening, homemade_remedy, repellent_insecticide]
]).

frame(organic_spray, [
    name: baking_soda,
    category: fungicide,
    description: 'Sodium bicarbonate solution that has fungicidal properties as both a protectant and eradicant for certain plant diseases.',
    protection_offered: 'Helps prevent black spot on roses and controls powdery mildew and other fungal diseases.',
    target_pests: [black_spot, powdery_mildew, fungal_diseases],
    application_method: 'Dissolve 1 teaspoon baking soda in 1 quart warm water. Add up to 1 teaspoon liquid dish soap or insecticidal soap to improve adherence to leaves. Spray infected plants thoroughly, covering undersides of leaves.',
    precautions: 'Generally safe for plants and applicator.',
    context: [organic_gardening, homemade_remedy, fungal_disease_control]
]).

frame(organic_spray, [
    name: compost_tea,
    category: fungicide,
    description: 'Solution made by soaking finished compost in water that provides nutrients to plants and serves as a natural fungicide.',
    protection_offered: 'Helps prevent various fungal diseases by promoting beneficial microorganisms that outcompete pathogens.',
    target_pests: [fungal_diseases, foliar_diseases],
    application_method: 'Soak finished compost in water according to standard compost tea preparation methods, strain, and apply as a foliar spray.',
    precautions: 'Generally safe for plants and applicator, but use precautions as with any spray application.',
    context: [organic_gardening, homemade_remedy, fungal_disease_prevention]
]).

frame(organic_spray, [
    name: sulfur,
    category: fungicide,
    description: 'One of the oldest known pesticides, used for centuries to control both plant pathogens and pests like insects and mites on contact.',
    protection_offered: 'Controls apple scab, brown rot of stone fruits, powdery mildews, rose black spot, rusts, and other plant diseases on grapes, potatoes, strawberries, tomatoes, and other crops. Also controls insects and mites on fruit trees and citrus.',
    target_pests: [apple_scab, brown_rot, powdery_mildew, black_spot, rusts, mites],
    application_method: 'Apply as dry powder for dusting or mix wettable formulation with water according to label directions. Agitate frequently as it settles out of solution.',
    precautions: 'Moderately toxic to humans and other mammals. Can irritate lungs, skin, and eyes. Nonspecific and can kill beneficial insects, soil microorganisms, and fish. Do not apply within 1 month of using oil spray. May cause plant injury above 80°F. Corrosive to metal equipment.',
    context: [organic_gardening, commercial_product, fungal_disease_control]
]).

frame(organic_spray, [
    name: hot_pepper_spray,
    category: botanical_repellent,
    description: 'Spray containing capsaicin from hot peppers that deters insects by making plants unpalatable and disrupting pest sensory receptors.',
    protection_offered: 'Repels onion maggots and other root maggots in vegetable seedlings. Also helps repel ants and the aphids they protect.',
    target_pests: [onion_maggots, root_maggots, ants, aphids],
    application_method: 'Sprinkle powder along both sides of seeded rows or around the base of each plant. Apply lightly but thoroughly. Renew after irrigation or heavy rain.',
    precautions: 'Avoid inhaling dust or getting it in eyes. Wear gloves as contact can irritate sensitive skin.',
    context: [organic_gardening, homemade_remedy, repellent]
]).

% ========================
% RELATIONSHIPS
% ========================

% General spray categories
belongs_to(all_purpose_insect_spray, homemade_spray).
belongs_to(soap_spray, contact_insecticide).
belongs_to(oil_spray, smothering_agent).
belongs_to(diatomaceous_earth, mechanical_insecticide).
belongs_to(pyrethrin, botanical_insecticide).
belongs_to(neem, botanical_insecticide).
belongs_to(garlic_oil, botanical_repellent).
belongs_to(baking_soda, fungicide).
belongs_to(compost_tea, fungicide).
belongs_to(sulfur, fungicide).
belongs_to(hot_pepper_spray, botanical_repellent).

% Controls relationships
controls(all_purpose_insect_spray, leaf_eating_insects).
controls(soap_spray, aphids).
controls(soap_spray, mealybugs).
controls(soap_spray, whiteflies).
controls(soap_spray, mites).
controls(oil_spray, aphids).
controls(oil_spray, mealybugs).
controls(oil_spray, mites).
controls(oil_spray, scales).
controls(diatomaceous_earth, slugs).
controls(diatomaceous_earth, snails).
controls(diatomaceous_earth, aphids).
controls(diatomaceous_earth, thrips).
controls(pyrethrin, aphids).
controls(pyrethrin, cabbage_loopers).
controls(pyrethrin, colorado_potato_beetle).
controls(pyrethrin, whiteflies).
controls(neem, aphids).
controls(neem, leafminers).
controls(neem, whiteflies).
controls(neem, colorado_potato_beetle).
controls(garlic_oil, aphids).
controls(garlic_oil, cabbageworms).
controls(garlic_oil, whiteflies).
controls(baking_soda, black_spot).
controls(baking_soda, powdery_mildew).
controls(compost_tea, fungal_diseases).
controls(sulfur, powdery_mildew).
controls(sulfur, black_spot).
controls(sulfur, mites).
controls(hot_pepper_spray, onion_maggots).
controls(hot_pepper_spray, root_maggots).
controls(hot_pepper_spray, ants).

% Safety level classifications
safety_level(all_purpose_insect_spray, moderate).
safety_level(soap_spray, high).
safety_level(oil_spray, moderate).
safety_level(diatomaceous_earth, moderate).
safety_level(pyrethrin, low).
safety_level(neem, high).
safety_level(garlic_oil, high).
safety_level(baking_soda, high).
safety_level(compost_tea, high).
safety_level(sulfur, low).
safety_level(hot_pepper_spray, moderate).

% Compatibility with beneficial insects
beneficial_impact(all_purpose_insect_spray, moderate).  % Some impact on beneficials
beneficial_impact(soap_spray, negative).  % Kills beneficials it contacts
beneficial_impact(oil_spray, minimal).  % Generally spares beneficials
beneficial_impact(diatomaceous_earth, negative).  % Nonselective
beneficial_impact(pyrethrin, negative).  % Kills beneficial insects
beneficial_impact(neem, minimal).  % Mostly spares beneficials
beneficial_impact(garlic_oil, minimal).  % Mostly spares beneficials
beneficial_impact(baking_soda, neutral).  % No significant impact
beneficial_impact(compost_tea, positive).  % Supports beneficial microorganisms
beneficial_impact(sulfur, negative).  % Harms beneficials
beneficial_impact(hot_pepper_spray, minimal).  % Mostly spares beneficials

% Application type
application_type(all_purpose_insect_spray, spray).
application_type(soap_spray, spray).
application_type(oil_spray, spray).
application_type(diatomaceous_earth, dust).
application_type(pyrethrin, both).  % Available as spray or dust
application_type(neem, spray).
application_type(garlic_oil, spray).
application_type(baking_soda, spray).
application_type(compost_tea, spray).
application_type(sulfur, both).  % Available as spray or dust
application_type(hot_pepper_spray, dust).

% Helper predicates
organic_sprays_for(Pest, SprayList) :-
    findall(Spray, controls(Spray, Pest), SprayList).

safe_organic_sprays(SafeSprayList) :-
    findall(Spray, safety_level(Spray, high), SafeSprayList).

beneficial_friendly_sprays(FriendlySprayList) :-
    findall(Spray, 
           (beneficial_impact(Spray, Impact),
            (Impact = minimal; Impact = positive; Impact = neutral)),
           FriendlySprayList).

sprays_by_category(Category, SprayList) :-
    findall(Spray, belongs_to(Spray, Category), SprayList).

sprays_by_application(Type, SprayList) :-
    findall(Spray, 
           (application_type(Spray, AppType),
            (AppType = Type; AppType = both)),
           SprayList).

% Query to find safe, beneficial-friendly sprays for a specific pest
safe_beneficial_friendly_for_pest(Pest, RecommendedSprayList) :-
    findall(Spray,
           (controls(Spray, Pest),
            safety_level(Spray, high),
            beneficial_impact(Spray, Impact),
            (Impact = minimal; Impact = positive; Impact = neutral)),
           RecommendedSprayList). 
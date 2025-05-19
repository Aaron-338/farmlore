# Farmlore Organic Pest Management Knowledge Base

This knowledge base contains structured information about organic pest management for gardening and agriculture. It integrates information about insects, plant diseases, crops, and control methods (both physical and biological).

## Knowledge Base Components

The system consists of several interconnected Prolog files:

1. **knowledgebase.pl** - Core knowledge base with general pest and practice information
2. **insect_reference.pl** - Detailed information about beneficial and pest insects
3. **plant_disease_reference.pl** - Plant disease information including symptoms, causes, and treatments
4. **control_methods.pl** - Physical and biological control methods for pest management
5. **crop_updates.pl** - Specific crop information including pests, diseases, and resistant cultivars
6. **pea_updates.pl** - Specific information about pea crops
7. **indigenous_kb.pl** - Traditional and indigenous pest management knowledge
8. **community_kb.pl** - Community-contributed pest management information
9. **organic_sprays.pl** - Comprehensive information on organic sprays and dusts, including application methods, safety, and target pests
10. **advanced_queries.pl** - Enhanced query interface supporting natural language, integrated knowledge areas, seasonal management, and location-based recommendations

## Loading the Knowledge Base

To load the entire knowledge base, consult the `load_all.pl` file:

```prolog
:- consult('load_all.pl').
```

## Query Examples

The `query_examples.pl` file demonstrates how to query the knowledge base. It includes examples like:

1. Finding physical control methods for specific pests
2. Identifying pests controlled by specific methods
3. Listing materials needed for different control methods
4. Finding control methods for pests affecting specific crops
5. Comparing effectiveness of biological vs physical controls
6. Finding appropriate organic sprays for specific pests
7. Identifying spray options that are safe for beneficial insects
8. Comparing safety levels of different botanical insecticides

To run all example queries:

```prolog
:- consult('query_examples.pl').
```

## Advanced Query Interface

The `advanced_queries.pl` file provides an enhanced interface for querying the knowledge base with the following features:

1. **Natural Language Processing**: Process semi-natural language queries using the `process_query/2` predicate:
   ```prolog
   process_query("How can I control aphids on my tomatoes in summer?", Response).
   ```

2. **Crop Rotation Planning**: Get crop rotation recommendations:
   ```prolog
   crop_rotation_for(tomato, RotationPlan).
   ```

3. **Seasonal Pest Management**:
   ```prolog
   seasonal_management(summer, spider_mites, Plan).
   seasonal_pests(fall, FallPests).
   ```

4. **Integrated Approach Across Knowledge Areas**: 
   ```prolog
   integrated_approach(aphids, tomato, summer, Approach).
   ```

5. **Location and Garden-Size Based Recommendations**:
   ```prolog
   custom_recommendation(aphids, 'Phoenix', summer, medium, Recommendations).
   ```

To test the advanced query capabilities, run:
```prolog
:- consult('advanced_queries.pl').
example_nl_query_1.
example_integrated_query.
example_location_query.
example_rotation_query.
```

## Frame Structure

The knowledge base uses a frame-based structure where information is organized into categories:

### Physical Control Methods
```prolog
frame(physical_control, [
    name: atom,
    category: atom,
    description: string,
    target_pests: list(atom),
    materials_needed: list(atom),
    application_method: string,
    effectiveness: atom,  % high, medium, low
    limitations: list(atom),
    context: list(atom)
]).
```

### Biological Control Methods
```prolog
frame(biological_control, [
    name: atom,
    category: atom,
    description: string,
    target_pests: list(atom),
    beneficial_organism: atom,
    application_method: string,
    effectiveness: atom,  % high, medium, low
    limitations: list(atom),
    context: list(atom)
]).
```

### Organic Sprays
```prolog
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
```

### Spray Safety
```prolog
frame(spray_safety, [
    name: atom,
    category: atom,
    description: string,
    guidelines: list(string),
    context: list(atom)
]).
```

### Insects
```prolog
frame(specific_insect, [
    name: atom,
    type: atom,
    scientific_name: string,
    description: string,
    life_cycle: string,
    damage: string,
    affects_crop: list(atom),
    prevention_methods: list(atom),
    control_methods: list(atom),
    beneficial_prey: list(atom)
]).
```

### Plant Diseases
```prolog
frame(specific_disease, [
    name: atom,
    type: atom,  % 'fungal', 'bacterial', 'viral', etc.
    scientific_name: atom,
    description: string,
    symptoms: string,
    host_plants: list(atom),
    spread_mechanism: string,
    conditions_favoring: list(atom),
    prevention_methods: list(atom),
    control_methods: list(atom),
    region: list(atom)
]).
```

## Common Queries

Here are some useful queries you can run:

### Find physical controls for a pest
```prolog
findall(Method, 
        (controls(Method, slugs), 
         belongs_to(Method, physical_control)), 
        Methods),
write('Physical controls for slugs:'), nl,
print_list(Methods).
```

### Find pests affected by a specific crop
```prolog
findall(Pest, affects_crop(Pest, tomato), Pests),
write('Pests affecting tomatoes:'), nl,
print_list(Pests).
```

### Find diseases that affect a plant
```prolog
findall(Disease, susceptible_to(rose, Disease), Diseases),
write('Diseases affecting roses:'), nl,
print_list(Diseases).
```

### Find all biological control methods
```prolog
control_methods_by_category(biological_control, Methods),
write('Biological control methods:'), nl,
print_list(Methods).
```

### Find organic sprays for a specific pest
```prolog
organic_sprays_for(aphids, Sprays),
write('Organic sprays for aphids:'), nl,
print_list(Sprays).
```

### Find safe organic sprays that don't harm beneficial insects
```prolog
safe_beneficial_friendly_for_pest(aphids, SafeSprays),
write('Safe sprays for aphids that minimize harm to beneficials:'), nl,
print_list(SafeSprays).
```

### Find spray safety guidelines
```prolog
frame(spray_safety, [name:spray_safely, guidelines:Guidelines, _]),
write('Safety guidelines for spray application:'), nl,
print_numbered_list(Guidelines).
```

## Helper Predicates

The system includes helper predicates to facilitate complex queries:

- `all_controls_for_pest(Pest, ControlList)`: Find all control methods for a pest
- `control_methods_for(Pest, ControlList)`: Find control methods directly related to a pest
- `materials_for(ControlMethod, MaterialList)`: Find materials needed for a control method
- `control_category(ControlMethod, Category)`: Find the category a control method belongs to
- `physical_controls_in_category(Category, Controls)`: Find physical controls in a specific category
- `beneficial_organisms(ControlMethod, Organisms)`: Find beneficial organisms used in a control method
- `control_methods_by_category(Category, Methods)`: Find all control methods in a category
- `organic_sprays_for(Pest, SprayList)`: Find organic sprays that control a specific pest
- `safe_organic_sprays(SafeSprayList)`: Find organic sprays with high safety ratings
- `beneficial_friendly_sprays(FriendlySprayList)`: Find sprays that minimize harm to beneficial insects
- `sprays_by_category(Category, SprayList)`: Find sprays belonging to a specific category
- `safe_beneficial_friendly_for_pest(Pest, RecommendedSprayList)`: Find safe, beneficial-friendly sprays for a specific pest

## Extending the Knowledge Base

To add new information to the knowledge base:

1. Use the appropriate frame structure for the type of information
2. Add relationship predicates to connect with existing knowledge
3. Test with queries to ensure proper integration

Example of adding a new organic spray method:

```prolog
frame(organic_spray, [
    name: new_spray_method,
    category: homemade_spray,
    description: 'Description of the new spray method',
    protection_offered: 'What protection it provides',
    target_pests: [pest1, pest2],
    application_method: 'How to apply the spray',
    precautions: 'Safety precautions when using this spray',
    context: [organic_gardening, homemade_remedy]
]).

% Add relationships
controls(new_spray_method, pest1).
controls(new_spray_method, pest2).
belongs_to(new_spray_method, homemade_spray).
safety_level(new_spray_method, high).
beneficial_impact(new_spray_method, minimal).
application_type(new_spray_method, spray).
``` 
% Basic facts about pests
pest(tomato_hornworm).
pest(aphid).
pest(spider_mite).
pest(whitefly).
pest(cutworm).

% Crops affected by pests
affects(tomato_hornworm, tomato).
affects(aphid, tomato).
affects(aphid, cucumber).
affects(spider_mite, tomato).
affects(spider_mite, cucumber).
affects(whitefly, tomato).
affects(cutworm, tomato).

% Symptoms caused by pests
symptom(tomato_hornworm, defoliation).
symptom(tomato_hornworm, fruit_damage).
symptom(aphid, yellowing_leaves).
symptom(aphid, stunted_growth).
symptom(spider_mite, webbing).
symptom(spider_mite, leaf_spotting).
symptom(whitefly, sticky_leaves).
symptom(cutworm, stem_damage).

% Control methods for pests
control_method(tomato_hornworm, handpicking).
control_method(tomato_hornworm, bt_spray).
control_method(aphid, neem_oil).
control_method(aphid, insecticidal_soap).
control_method(spider_mite, neem_oil).
control_method(spider_mite, increase_humidity).
control_method(whitefly, yellow_sticky_traps).
control_method(cutworm, collar_barriers).

% Prevention methods
prevention_method(tomato_hornworm, companion_planting).
prevention_method(aphid, reflective_mulch).
prevention_method(spider_mite, regular_misting).
prevention_method(whitefly, crop_rotation).
prevention_method(cutworm, soil_barriers).

% Rules for inference
pest_identification(Crop, Symptom, Pest) :-
    affects(Pest, Crop),
    symptom(Pest, Symptom).

suitable_control(Pest, Method) :-
    pest(Pest),
    control_method(Pest, Method).

prevention_strategy(Pest, Method) :-
    pest(Pest),
    prevention_method(Pest, Method).

all_controls_for_pest(Pest, Methods) :-
    findall(Method, control_method(Pest, Method), Methods).

all_symptoms_for_pest(Pest, Symptoms) :-
    findall(Symptom, symptom(Pest, Symptom), Symptoms).

pests_for_crop(Crop, Pests) :-
    findall(Pest, affects(Pest, Crop), Pests).

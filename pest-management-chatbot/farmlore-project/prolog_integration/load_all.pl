% ========================
% FARMLORE KNOWLEDGE BASE LOADER
% ========================
% This file loads all the Prolog knowledge bases for the pest management system

% Load existing knowledge bases
:- consult(knowledgebase).
:- consult(insect_reference).
:- consult(plant_disease_reference).
:- consult(crop_updates).
:- consult(pea_updates).
:- consult(indigenous_kb).
:- consult(community_kb).

% Load the new control methods knowledge base
:- consult(control_methods).

% Load the organic sprays knowledge base
:- consult(organic_sprays).

% Load the frame adapters to make the frame-based KB work with the connector
:- consult(frame_adapters).

% Note: advanced_queries.pl loads its dependencies directly to avoid circular references
% It is loaded last to ensure all other knowledge bases are available
:- consult(advanced_queries).

% Informative message when everything is loaded
:- write('All knowledge bases loaded successfully.'), nl.
:- write('Available knowledge bases:'), nl.
:- write('- Main knowledge base (knowledgebase.pl)'), nl.
:- write('- Insect reference (insect_reference.pl)'), nl.
:- write('- Plant disease reference (plant_disease_reference.pl)'), nl.
:- write('- Crop updates (crop_updates.pl)'), nl.
:- write('- Pea information (pea_updates.pl)'), nl.
:- write('- Indigenous knowledge (indigenous_kb.pl)'), nl.
:- write('- Community knowledge (community_kb.pl)'), nl.
:- write('- Control methods (control_methods.pl)'), nl.
:- write('- Organic sprays and dusts (organic_sprays.pl)'), nl.
:- write('- Frame adapters (frame_adapters.pl)'), nl.
:- write('- Advanced query interface (advanced_queries.pl)'), nl. 
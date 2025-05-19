% ========================
% TEST FRAME ADAPTERS
% ========================
% This file tests the frame adapters to ensure they work correctly

% Load the knowledge base and adapters
:- consult(knowledgebase).
:- consult(frame_adapters).

% Test pest adapter
test_pest_adapter :-
    write('Testing pest adapter...'), nl,
    findall(Name, pest(name:Name, _), PestNames),
    write('Found pests: '), write(PestNames), nl,
    length(PestNames, Count),
    write('Total pests found: '), write(Count), nl.

% Test practice adapter
test_practice_adapter :-
    write('Testing practice adapter...'), nl,
    findall(Name, practice(name:Name, _), PracticeNames),
    write('Found practices: '), write(PracticeNames), nl,
    length(PracticeNames, Count),
    write('Total practices found: '), write(Count), nl.

% Test crop adapter
test_crop_adapter :-
    write('Testing crop adapter...'), nl,
    findall(Name, crop(name:Name, _), CropNames),
    write('Found crops: '), write(CropNames), nl,
    length(CropNames, Count),
    write('Total crops found: '), write(Count), nl.

% Test pest_solutions adapter
test_pest_solutions :-
    write('Testing pest_solutions adapter...'), nl,
    (pest(name:Name, _), 
     pest_solutions(Name, global, Solutions),
     write('Solutions for '), write(Name), write(': '), write(Solutions), nl,
     fail
    ; true).

% Test recommend_solution adapter
test_recommend_solution :-
    write('Testing recommend_solution adapter...'), nl,
    (pest(name:Name, _), 
     recommend_solution(Name, Solution),
     write('Recommended solution for '), write(Name), write(': '), write(Solution), nl,
     fail
    ; true).

% Run all tests
run_tests :-
    write('Running adapter tests...'), nl,
    test_pest_adapter,
    test_practice_adapter,
    test_crop_adapter,
    test_pest_solutions,
    test_recommend_solution,
    write('All tests completed.'), nl.

% Auto-run tests when file is consulted
:- run_tests. 
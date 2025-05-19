% ========================
% FRAME ADAPTERS
% ========================
% This file provides adapter predicates to make the frame-based knowledge base
% compatible with the connector's query format

% Adapter for pest queries
% Convert pest(name:Name, Attributes) to frame(pest, [name:Name|Attributes])
pest(name:Name, Attributes) :-
    frame(pest, Attributes),
    member(name:Name, Attributes).

% Adapter for practice queries
% Convert practice(name:Name, Attributes) to frame(practice, [name:Name|Attributes])
practice(name:Name, Attributes) :-
    frame(practice, Attributes),
    member(name:Name, Attributes).

% Adapter for crop queries
% Convert crop(name:Name, Attributes) to frame(crop, [name:Name|Attributes])
crop(name:Name, Attributes) :-
    frame(crop, Attributes),
    member(name:Name, Attributes).

% Adapter for pest_solutions
% Extract solutions from pest frame's controls slot
pest_solutions(Pest, Region, Solutions) :-
    pest(name:Pest, Attributes),
    member(controls:Solutions, Attributes),
    % Check if the pest applies to the given region
    (member(cultural_context:Contexts, Attributes) ->
        (member(Region, Contexts) ; member(global, Contexts))
    ;
        true  % If no cultural_context specified, assume global
    ).

% Adapter for recommend_solution
% Simple implementation that returns the first solution from pest_solutions
recommend_solution(Pest, Solution) :-
    pest_solutions(Pest, global, Solutions),
    Solutions = [Solution|_]. 
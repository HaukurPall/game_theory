# Data structures -
# Preference
# -Is a higher than b?
# -Generate random preferences
#  Profile
# - Is manipulable? to voting rule
# - Adjust t
# Voting Rule
# - Winning decision
# - Manipulable requirement
import random

class Preference:

    """
    :param list_of_preferences: orderer list of integers, in which integer is a unique candidate, first candidate is 0
    """
    def __init__(self, preference_order):
        self.preference_order = preference_order
        self.number_of_candidates = len(preference_order)

    @staticmethod
    def generate_random_preference_order(m):
        preference_set = set([x for x in range(0, m)])
        preference_list = [random.sample(preference_set, 1) for x in range(0, m)]
        return Preference(preference_list)

    def is_x_more_preferred_than_y(self, x, y):
        return self.preference_order.index(x) < self.preference_order.index(y)

    def place_x_first(self, x):
        old_order = self.get_order()
        old_order.remove(x)
        return Preference([x] + old_order)

    def place_x_last(self, x):
        old_order = self.get_order()
        old_order.remove(x)
        return Preference(old_order + [x])

    def find_most_preferred_candidate(self, list_of_candidates):
        lowest_index = self.get_number_of_candidates()
        for candidate in list_of_candidates:
            candidate_index = self.preference_order.index(candidate)
            if candidate_index < lowest_index:
                lowest_index = candidate_index
        return lowest_index

    def find_least_preferred_candidate(self, list_of_candidates):
        highest_index = -1
        for candidate in list_of_candidates:
            candidate_index = self.preference_order.index(candidate)
            if candidate_index > highest_index:
                highest_index = candidate_index
        return highest_index

    def get_most_preferred_candidate(self):
        return self.preference_order[0]

    def get_order(self):
        return self.preference_order

    def get_number_of_candidates(self):
        return self.number_of_candidates


class Profile:

    def __init__(self, list_of_preferences):
        self.list_of_preferences = list_of_preferences
        self.number_of_voters = len(list_of_preferences)

    def get_number_of_candidates(self):
        return self.list_of_preferences[0].get_number_of_candidates()

    def is_manipulable(self, voting_rule, scores):
        winners = voting_rule.get_winners(scores)
        possible_winners = voting_rule.get_possible_winners(scores)
        if not voting_rule.is_result_manipulable(winners, possible_winners):
            return False
        # multiple winners, we attempt to find some voter which had none of them on top but then likes one more
        if len(winners) > 1:
            for index, preference_order in enumerate(self.list_of_preferences):
                # he did not vote for one of the winners
                if preference_order.get_most_prefered_candidate() not in winners:
                    candidate_should_win = preference_order.find_most_preferred_candidate(winners)
                    candidate_should_lose = preference_order.find_least_preferred_candidate(winners)
                    new_preference_order = preference_order.place_x_first(candidate_should_win)
                    new_preference_order = new_preference_order.place_x_last(candidate_should_lose)
                    self.manipulate_preference_order(index, new_preference_order)
                    print("Found many winners, made one of them win.")
                    return True

        for preference_order in self.list_of_preferences:
            for winner in winners:
                for possible_winner in possible_winners:


    def manipulate_preference_order(self, i, new_preference_order):
        self.list_of_preferences[i] = new_preference_order


class VotingRule:
    def __init__(self, name):
        self.name = name

    def calculate_scores(self, profile):
        pass

    def get_winners(self, candidate_scores):
        pass

    def get_possible_winners(self, candidate_scores):
        pass

    @staticmethod
    def is_result_manipulable(winners, possible_winners):
        # are there many winners? Someone will, maybe, want either of them to win
        if len(winners) != 1:
            return True
        # are there possible winners? Someone will, maybe, want some of them to win
        if len(possible_winners) != 0:
            return True
        return False


class PluralityRule(VotingRule):

    def __init__(self):
        super("Plurality rule")

    def calculate_scores(self, profile):
        candidate_scores = [0 for x in range(0, profile.get_number_of_candidates())]
        for preference_order in profile:
            candidate = preference_order.get_most_prefered_candidate()
            candidate_scores[candidate] += 1

        return candidate_scores

    def get_winners(self, candidate_scores):
        winners = []
        max_score = max(candidate_scores)
        for index, score in enumerate(candidate_scores):
            if score == max_score:
                winners.append(index)
        return winners


    def get_possible_winners(self, candidate_scores):
        possible_winners = []
        max_score = max(candidate_scores)
        possible_winner_score = max_score - 1
        for index, score in enumerate(candidate_scores):
            if score == possible_winner_score:
                possible_winners.append(index)
        return possible_winners


#Steps:
#1. Generate the profiles for various n.
#2. Algorithm to determine winner under each rule
#3. Find some algorithm to check for manipulablity under each voting rule.
#4. Draw sample from profiles generated, look at manipulable fraction, do statistical tests to determine whether difference is significant.

#1. Generate profiles
import numpy as np
#for n voters, x candidates. profile =  x * n array.
#1st item in row is most preferred etc.

#2. Determine winner under Plurality, Copeland and Borda
#Borda: assign each candidate a counter. move through array and update counter with Borda-vector values. pick candidate with maximal number (tie breaking?)
#Plurality: assign each candidate a counter. move through rows of array and give first candidate one point. pick candidate with maximal number (tie breaking?)
#Copeland: assign each candidate a counter. move through rows of array in following way:
#give first candidate x-1 points, give all candidates from second place onwards -1 point.
#give second candidate x-2 points, give all candidates from third place onwards -1 point.
#...
#give last candidate x-x=0 points, assign nobody negative points, move to next row until all rows completed
#the candidate with most points wins (tie breaking?)

#3. algorithm to check whether some player stands to benefit from manipulating the vote (for given profile and rule)
#Plurality:
# look at candidate count: if margin of victory > 1, declare profile not manipulable (no single player can change anything)
# if margin of victory < 2, note who lost and look at all voter's profile in following way:
# if rank of 2nd > actual winner's rank, declare profile manipulable
#otherwise move to next voter
#if no voter can manipulate, declare profile not manipulable

#Borda:
#look at candidate count: if margin of victory > x-1, declare profile not manipulable (no single player can change anything about winner because maximal 'distance in her ranking is x-1)
#if margin of victory <= x-1, note who was within x-2 of the actual winner and put them in (LOSERS) set. not what the margin of victory (mov) was with respect to them. then look at all voter's 			profile:
#start with first ranked candidate: if candidate = winner, move to next voter. otherwise, move to second ranked candidate for same voter:
#if that candidate is ranked higher than winner & in LOSERS, then check winner's rank: if (mov) of winner wrt to second candidate <= 1+ (x-rank of winner), then declare profile manipulable. 			(1 for putting second placed candidate on top, (x-rank of winner) for putting winner at the bottom). otherwise, move to third ranked candidate:
#if that candidate is ranked higher than winner & in LOSERS, then check winner's rank: if (mov) of winner wrt to third candidate <= 2+ (x-rank of winner), then declare profile manipulable. 			(2 for putting third placed candidate on top, (x-rank of winner) for putting winner at the bottom). otherwise, move to forth ranked candidate:
#etc.
#if, for all voters, no candidate fullfils all three criteria (candidate ranked higher than winner, in LOSERS, within manipulable range), declare profile not manipulable

#Copeland:
#
#
#
#
#


#4. Draw sufficiently large sample of profiles for varying n.
#Run all profiles in sample through 2. and 3. for each rule. Note fraction that are manipulable for each.
#Do statistical test for significance of difference in fraction of manipulable between the three. (unsure how to do a three-way test still. see: http://isites.harvard.edu/fs/docs/icb.topic576892.files/15Anova.pdf)
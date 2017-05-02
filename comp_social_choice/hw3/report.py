from comp_social_choice.hw3.manipulability import Preference, Profile, BordaRule, PluralityRule, CopelandRule
import matplotlib.pyplot as plt
import time


def generate_profiles(number_of_voters=10, number_of_candidates=3, number_of_profiles=10):
    profiles = []
    for profile in range(0, number_of_profiles):
        profiles.append(Profile.generate_random_profile(number_of_voters, number_of_candidates))
    return profiles


def create_graphs(data_file, graph_name):
    x, y_borda, y_plurality, y_copeland = extract_counts(data_file)

    fig, ax = plt.subplots()
    plt.xlabel("number of voters")
    trace0 = ax.plot(
        x,
        y_plurality,
        'o',
        label='plurality'
    )
    trace1 = ax.plot(
        x,
        y_borda,
        'o',
        label='borda/copeland'
    )

    ax.legend(loc='upper center', shadow=True)
    ax.set_ylim([0, 100])
    plt.savefig(graph_name)
    plt.clf()


def compute_averages(data_file):
    x, y_borda, y_plurality, y_copeland = extract_counts(data_file)
    plurality_sum = 0
    borda_sum = 0
    for index, voter_count in enumerate(x):
        plurality_sum += y_plurality[index]
        borda_sum += y_borda[index]
    print("plurality: " + str(plurality_sum / len(x)))
    print("borda: " + str(borda_sum / len(x)))


def extract_counts(data_file):
    with open(data_file) as data_file:
        next(data_file)
        y_plurality = []
        y_borda = []
        y_copeland = []
        x_is_voter_counts = True
        x = []
        voter_count = 0
        counter = -1
        for line in data_file:
            data_line = line.strip().split(",")
            data_line = [int(data) for data in data_line]
            if x_is_voter_counts:
                if data_line[1] != voter_count:
                    y_plurality.append(0)
                    y_borda.append(0)
                    y_copeland.append(0)
                    voter_count = data_line[1]
                    x.append(voter_count)
                    counter += 1
                if 1 == int(data_line[3]):
                    if data_line[0] == 0:
                        y_plurality[counter] += 1
                    if data_line[0] == 1:
                        y_borda[counter] += 1
                    if data_line[0] == 2:
                        y_copeland[counter] += 1
    return x, y_borda, y_plurality, y_copeland


def write_aggregated_data_to_file(output_file, input_file):
    x, y_borda, y_plurality, y_copeland = extract_counts(input_file)
    with open(output_file + "_plurality", "a") as data_file:
        for i in range(0, len(x)):
            data_file.write(",".join([str(x[i]), str(y_plurality[i])]) + "\n")
    with open(output_file + "_borda", "a") as data_file:
        for i in range(0, len(x)):
            data_file.write(",".join([str(x[i]), str(y_borda[i])]) + "\n")


def generate_data(file_name, number_of_candidates, number_of_profiles, start_voters, end_voters, increment_voters):
    plurality_rule = PluralityRule()
    borda_rule = BordaRule()
    copeland_rule = CopelandRule()
    number_of_voters = start_voters
    with open(file_name, "a") as file:
        file.write("rule,voters,candidates,manipulable\n")
        while number_of_voters <= end_voters:
            profiles = generate_profiles(number_of_voters, number_of_candidates, number_of_profiles)
            for profile in profiles:
                write_to_file(file, number_of_candidates, number_of_voters, plurality_rule,
                              profile.is_manipulable(plurality_rule))
                write_to_file(file, number_of_candidates, number_of_voters, borda_rule,
                              profile.is_manipulable(borda_rule))
                write_to_file(file, number_of_candidates, number_of_voters, copeland_rule,
                              profile.is_manipulable(copeland_rule))
            number_of_voters += increment_voters


def write_to_file(file, number_of_candidates, number_of_voters, rule, manipulable):
    if manipulable:
        file.write(",".join([str(rule.get_number()), str(number_of_voters), str(number_of_candidates), "1"]) + "\n")
    else:
        file.write(",".join([str(rule.get_number()), str(number_of_voters), str(number_of_candidates), "0"]) + "\n")


def main():
    t0 = time.time()
    generate_data("10_candidates_csv.csv", 10, 100, 10, 1000, 10)
    create_graphs("10_candidates_csv.csv", "10 candidates")
    compute_averages("10_candidates_csv.csv")
    #write_aggregated_data_to_file("6_candidates_aggregated", "6_candidates_csv.csv")
    t1 = time.time()
    total = t1-t0
    print("Total time taken: " + str(total))

if __name__ == "__main__":
    main()

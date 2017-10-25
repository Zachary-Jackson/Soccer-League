import csv
import os

# Imports the data into a list of dictionaries
def CSV_reader():
    file_location = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(file_location, 'soccer_players.csv')
    with open(file_name) as csvfile:
        CSV_contents = []
        reader = csv.DictReader(csvfile)
        for row in reader:
            CSV_contents.append(row)
    return CSV_contents


# Returns two lists of players seperated via experiance
def experience_seperator(player_info_list):
    beginner = []
    experienced = []
    for player in player_info_list:
        if player["Soccer Experience"] == "NO":
            beginner.append(player["Name"])
        else:
            experienced.append(player["Name"])

    return(beginner, experienced)


# Assign players their team via updating the master_list
def team_assigner(beginner_players, experienced_players, player_info_list):
    team = 3
    Sharks, Dragons, Raptors = [], [], []

    for player in beginner_players:
        temp_name = [player]
        if team == 3:
            Raptors.append(temp_name.pop())
        elif team == 2:
            Dragons.append(temp_name.pop())
        else:
            Sharks.append(temp_name.pop())
        if team > 1:
            team -=1
        else:
            team = 3

    for player in experienced_players:
        temp_name = [player]
        if team == 3:
            Raptors.append(temp_name.pop())
        elif team == 2:
            Dragons.append(temp_name.pop())
        else:
            Sharks.append(temp_name.pop())
        if team > 1:
            team -=1
        else:
            team = 3

    #Updates the player_info_list
    for player in player_info_list:
        if player["Name"] in Raptors:
            player["Team"] = "Raptors"
        elif player["Name"] in Dragons:
            player["Team"] = "Dragons"
        else:
            player["Team"] = "Sharks"

    return(player_info_list)


# Create and/or clears teams.txt file
def file_creator(named_file):
    file_location = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(file_location, named_file)
    file = open(file_name, "w")
    file.close()


# Adds data to teams.txt in a sorted, orderly maner
def teams_file_editor(player_info_list):
    teams = ["Raptors", "Sharks", "Dragons"]
    counter = 2
    current_team = teams[counter] # cycles with the upcoming loop to change teams
    with open("teams.txt", "a")as file:
        while counter >= 0:
            if counter != 2:
                file.write("\n")
            file.write(current_team)
            file.write("\n")
            for player in player_info_list:
                if player["Team"] == current_team:
                    file.write(("{}, {}, {}".format((player["Name"]), (player["Soccer Experience"]), (player["Guardian Name(s)"])))+"\n")
            counter -= 1
            current_team = teams[counter]


# Create a letter for each parent in the firstname_lastname.txt format being lowercased
def guardian_letters(player_info_list):
    name_splitter = "_"
    for player in player_info_list:

        # Creates a file for each player's guardian
        full_name = player["Name"].lower().split(" ")
        full_name =(name_splitter.join(full_name))+".txt"
        file_creator(full_name)

        # Writes to the file for each player's guardian
        with open(full_name, "a") as file:
            file.write("""Dear {}.

    Your child {} has been accepted onto the {} team in our soccer league.
Please bring your child to the soccer court at 3:45 PM on September 19th.
We will discuss the fourms and procedures of the sport then as well as answer any questions you may have.


Thanks again,

From your favorite elementary school!""".format((player["Guardian Name(s)"]), (player["Name"]), (player["Team"])))



def main():
    master_list = [] # This value holds a list of dictionarys for each player
    beginner_list, experienced_list = [], [] # These lists seperate players based on experience

    master_list = CSV_reader()
    beginner_list, experienced_list = experience_seperator(master_list)

    # Updates the master_list to have assigned teams
    master_list = team_assigner(beginner_list, experienced_list, master_list)

    #Creates the list of teams and the players in teams.txt
    file_creator("teams.txt")
    teams_file_editor(master_list)

    # Creates letters for each guardian
    guardian_letters(master_list)


# Makes sure that the script does not run if imported
if __name__ == "__main__":
    main()

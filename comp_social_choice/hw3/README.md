# Manipulability
## Description
This program computes manipulability of the plurality, borda and copeland rules. It works on automatically generated profiles. 
### Authors
Haukur Páll Jónsson
Silvan Hungerbuhler
Max Rapp
## Running the code
### Prerequisites
- python 3.5+

### Input
Our program takes 3 inputs. These need to be changed in code:

    voters=Number of voters per profiles
    candidates=Number of candidates per profile
    profiles=Number of profiles to create with these properties
### Executing
    python3 manipulability.py
### Output
The program outputs 4 values to a file called 'data.txt'. 
    
    RuleName=
    voters=
    candidates=
    manipulable=
   
Rule name is a string. Voters is the number of voters used for this profile. Candidates is the number of candidates used for this profile. Manupulable is either 0 or 1, depending if the profile was maipulable or not.
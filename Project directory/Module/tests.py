import pandas as pd

from functions import TeamMember
from functions import Task

#defining the variables to be used in the 3 tests
task1 = Task("Write first section", 2, ["Writing", "Biology"])
task2 = Task("Write second section", 3, ["Writing", "Chemistry"])
task3 = Task("Write third section", 4, ["Patience", "Math"])
task4 = Task("Write fourth section", 1, ["Math", "Chemistry", "Biology"])
task5 = Task("Write fifth section", 5, ["Patience", "Biology"])
task6 = Task("Check answers with TA", 6, ["Reading", "Editing"])
task7 = Task("Assign citations", 7, ["Reading", "Writing"])

member1 = TeamMember("Thu", ["Writing", "Chemistry"])
member2 = TeamMember("Prini", ["Biology", "Editing"])
member3 = TeamMember("Belen", ["Reading", "Patience"])
member4 = TeamMember("Anya", ["Math", "Writing"])
member5 = TeamMember("Trisha",["Patience", "Biology"])

team1 = [member1, member2, member3, member4, member5]
team2 = [member1]
                
tasks1 = [task1, task2, task3, task4, task5, task6, task7]
tasks2 = [task2]

def test_sort_time():
    test1 = tasks1
    run1 = Task.sort_time(test1)
    assert run1[0] == test1[6] 
    assert run1[1] == test1[5] 
    assert run1[2] == test1[4]
    
def test_assign_tasks():
    test2 = Task.assign_tasks(tasks2, team2)
    run2 = sorted(test2, key = lambda chore : chore.assigned_person)
    assert run2[0].assigned_person == 'Thu'

def test_shortest_day_of_tasks():
    day1 = [task1, task2]
    day2 = [task6, task7]
    test3 = [day1, day2]
    run3 = Task.shortest_day_of_tasks(test3)
    assert run3 == day1
import pandas as pd

class TeamMember:
    def __init__(self, name, skills):
        self.name = name
        self.skills = skills
               
class Task:
    
    def __init__(self, name, time, required_skills):
        # Initialize Task object with name, time, required skills and assigned person
        self.name = name
        self.time = time
        self.required_skills = required_skills
        self.assigned_person = ''

    def sort_time(task_list):
        """This function arranges tasks in descending order based on the time required to complete them.
    
        Parameters:
        task_list : list 
            List of inputted tasks
            
        Returns:
        output : list 
            Sorted list of instances of Task class
        """
        output = sorted(task_list, key=lambda task: task.time, reverse=True) # Sort the task list by time in descending order (hence reverse)
        return output
       
    def assign_tasks(tasks, team):
        """Assigns tasks to team members considering their skillset and availability.
    
        Parameters:
        tasks : list 
            List of inputted tasks
        team : list
            List of team members
    
        Returns:
        all_tasks : list 
            Resulting list of instances of Task class
        """
        all_tasks = Task.sort_time(tasks)  # Sort tasks by time with the sort_time function
        count = 0

        # Iterate over each task and assign it to a team member
        for task in all_tasks:
            assigned = False
        
            # Iterate over team members to find one with the required skills
            for person in team:
                if all(skill in person.skills for skill in task.required_skills):
                    task.assigned_person = person.name
                    count += 1
                    assigned = True
                    break
        
            # If no one has required skills, assign task to the least busy person
            if not assigned:
                least_workload_person = min(team, key=lambda person: sum(task.time for task in all_tasks if task.assigned_person == person.name))
                task.assigned_person = least_workload_person.name

        return all_tasks
    def shortest_day_of_tasks(week):
        """Identifies the day with the minimum total duration occupied by tasks and provides a list of tasks completed on that day.
    
        Parameters:
        week : list 
            List of a list of instances of Task class, each element representing tasks for each day
    
        Returns:
        shortest_day_of_tasks : list 
            List of instances of Task class representing the tasks for that day
        """
        
        # Find the day with the shortest total time taken up by tasks by summing the amount of time taken by tasks each day
        shortest_day_of_tasks = week[0]
        shortest_time_taken = sum(task.time for task in week[0])
    
        for day in week:
            total_time_taken = sum(task.time for task in day)
            if total_time_taken <= shortest_time_taken:
                shortest_time_taken = total_time_taken
                shortest_day_of_tasks = day
            
        return shortest_day_of_tasks

    def split_daily(tasks):
        """Split tasks into daily allotments according to the time they will take up.
        
        Parameters:
        tasks : list 
            List of instances of Task class
    
        Returns:
        week : list 
            List of a list of instances of Task class, each element representing tasks for each day
        """
        distribute = []
        sunday = []       
        monday = []
        tuesday = []
        wednesday = []
        thursday = []
        friday = []
        saturday = []

    
        # Divide tasks into days based
        for task in tasks:
            distribute.append(task)
            
        week = [sunday, monday, tuesday, wednesday, thursday, friday, saturday]
        distribute = Task.sort_time(distribute)
    
        for task in distribute:
            Task.shortest_day_of_tasks(week).append(task)
        
        return week
    
    def distribute_per_person(week_tasks, team_members):
        """Separate tasks into a dictionary representing each team member's tasks for the week.
    
        Parameters:
        week_tasks : list 
            List of a list of instances of Task class, each element representing tasks for each day
        team_members : list
            List of team members
    
        Returns:
        output : dictionary
            Key - each person, value - array with each element representing tasks of each day
        """
        
        person_tasks_weekly = [[[] for day in range(len(week_tasks))] for team_member in range(len(team_members))]
        day_index = 0

        # loops through each task in the week and sorts tasks into a dictionary of each person's weekly tasks
        for day_tasks in week_tasks:
            day_tasks_sorted = sorted(day_tasks, key=lambda task: task.assigned_person)
            person_index = 0
            
            for team_member in team_members:
                for task in day_tasks_sorted:
                    if team_member.name == task.assigned_person: 
                        person_tasks_weekly[person_index][day_index].append(task.name)
                person_index += 1
            day_index += 1

        tasks_per_person = dict(zip([member.name for member in team_members], person_tasks_weekly))
        return tasks_per_person
    
    def task_allocator(task_list, team):
        """Brings together functions to distribute tasks.
    
        Parameters:
        task_list : list 
            List of inputted tasks
        team : list
            List of team members
    
        Returns:
        output : pandas DataFrame
            Table with tasks corresponding to each person as columns and the days as rows   
        """
        
        # Allocate tasks to team members and generate pandas DataFrame
        week = Task.split_daily(Task.assign_tasks(task_list, team))
        result = Task.distribute_per_person(week, team)
        output = Task.table_format(result, team)
        
        # Check if all tasks are allocated
        for tasks_per_day in result.values():
            for tasks in tasks_per_day:
                for task in tasks:
                    if task == '':
                        print("Error: Not all tasks are allocated.")
                        break
    
        return output
    
    def table_format(week, team):
        """Structures segmented tasks into a visual DataFrame.
    
        Parameters:
        week : list 
            List of a list of instances of Task class, each element representing tasks for each day
        team : list
            List of team members
    
        Returns:
        output : pandas DataFrame
            Table with tasks corresponding to each person as columns and the days as rows   
        """
        
        # Create pandas DataFrame for visual representation of tasks
        week_task_names = [[task for task in day] for day in week]

        output = pd.DataFrame(week, index=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    
        for person in team:
            output[person.name] = output[person.name].astype('string').apply(lambda x: x.replace('[','').replace(']','').replace('\'',''))
        
        return output
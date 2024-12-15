#Simple To-Do List Manager
#Problem: Create a simple to-do list manager.
	#• Allow the user to:
	#	1. Add a task
	#	2. View all tasks
	#	3. Mark a task as done
	#	4. Exit

task = []
while True:
    print('1. Add a task')
    print('2. View all task')
    print('3. Mark as done')
    print('4. Exit')
    action = input('Hello, any tasks to be done or do?: ')

    if action == '1':
        task.append(input('Enter a task: '))
        print('Task added!')
    elif action == '2':
        print('Behold! Here are your tasks for today:')
        for index, value in enumerate(task, start = 1):
            print(f"{index}. {value}")
    elif action == '3':
        remove= int(input('Woohoo! What task have you successfully done?:'))
        task.pop(remove - 1)
        print('Task removed!')
    elif action == '4':
        print('Okay, have fun doing your tasks! Goodluck!')
        break
    else:
        print('Invalid Menu. Please try again.')
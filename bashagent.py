import openai
import os
import json
import subprocess

#config
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
gpt35 = "gpt-3.5-turbo"
gpt4 = "gpt-4"

##############################################
usrmsg = ""
def user_input():
    global usrmsg
    usrmsg = ""
    print("Enter Instructions: ")
    usrmsg = input()
##############################################


def parse_action_string(action_string):
    actions = json.loads(action_string).items()
    action_dict = []
    for i in actions:
        action_name, action_function = i
        action_dict.append((action_name, action_function))  
    return action_dict

def order_actions(action_list):
    action_names = []
    actions_array = []
    for actions in action_list:
        action_name, action_function = actions
        action_names.append(action_name)
        actions_array.append(action_function)
    return action_names, actions_array

def run_script_action(action):
    os.system(action)

def run_all_script_actions(actions_array):
    for i in range(len(actions_array)):
        run_script_action(actions_array[i]) 
    print("All actions completed.")
    

def run_named_script(action_dict, action_name):
    for name, action in action_dict:
        if name == action_name:
            run_script_action(action)
            print("Action completed.")


##############################################
def append_message(messages, input_txt, role):
    messages.append({"role": role, "content": f"{input_txt}"})

def delete_message(messages):
    messages.pop()
    messages.pop()
    messages.pop()

def llmagent(message_array, llmmodel, temp):
    response = openai.ChatCompletion.create(
        model=llmmodel,
        temperature=temp,
        messages=message_array
    )
    return response.choices[0].message.content
##############################################

def script_agent():
    system_message = "For a given task or instruction, generate the bash actions needed to complete the task. Return just a dictionary with the action names and the actions itself. Add _<index> at the end of each name"
    messages = []
    append_message(messages, system_message, "system")
    user_input()
    if usrmsg == "quit":
        print("Quitting agent . . .")
        return
    append_message(messages, usrmsg, "user")
    action_dict = parse_action_string(llmagent(messages, gpt4, 0))
    action_names, actions_array = order_actions(action_dict)
    run_all_script_actions(actions_array)
    continue_script_agent(messages)

def continue_script_agent(messages):
    append_message(messages, "I just completed the task. What should I do next? I will only return new actions", "assistant")
    user_input()
    if usrmsg == "delete":
        delete_message(messages)
        continue_script_agent(messages)
        return
    if usrmsg == "quit":
        print("Quitting agent . . .")
        return
    append_message(messages, usrmsg, "user")
    action_dict = parse_action_string(llmagent(messages, gpt4, 0))
    action_names, actions_array = order_actions(action_dict)
    run_all_script_actions(actions_array)
    continue_script_agent(messages)




script_agent()

#examples
#create a new python script called this.py in a new folder called this in the pwd. The file should print "this works!". Then run the file as a python3 script.

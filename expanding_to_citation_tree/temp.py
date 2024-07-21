import webbrowser
import time
import random

from searches import searches

links_of_lists = searches

# Total time for each sublist to run (in seconds)
sublist_runtime = 30 * 60  # 30 minutes

# Delay range between searches within a sublist (in seconds)
min_delay_within = 1 * 60  # 1 minute
max_delay_within = 5 * 60  # 5 minutes

# Delay range between sublists (in seconds)
min_delay_between = 10 * 60  # 10 minutes
max_delay_between = 20 * 60  # 20 minutes

# Function to perform the search
def perform_search(link):
    webbrowser.open(link)
    print(link)

# Execute searches with random delays for each sublist
for sublist in links_of_lists:
    print(sublist)
    start_time_sublist = time.time()
    for link in sublist:
        if time.time() - start_time_sublist > sublist_runtime:
            break
        perform_search(link)
        delay_within = random.randint(min_delay_within, max_delay_within)
        print(f"Waiting for {delay_within // 60} minutes and {delay_within % 60} seconds before the next search...")
        time.sleep(delay_within)
    
    if sublist != links_of_lists[-1]:  # Avoid adding delay after the last sublist
        delay_between = random.randint(min_delay_between, max_delay_between)
        print(f"Waiting for {delay_between // 60} minutes and {delay_between % 60} seconds before starting the next sublist...")
        time.sleep(delay_between)

print("Script completed.")


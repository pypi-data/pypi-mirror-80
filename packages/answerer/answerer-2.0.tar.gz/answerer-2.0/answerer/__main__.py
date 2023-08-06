from .main import *

try:
    answer_issues()
    print("Finding links complete. Generating links... \n")
    generate_links()
    print("Done!")
except KeyboardInterrupt:
    print("\nProgram Stopped!")

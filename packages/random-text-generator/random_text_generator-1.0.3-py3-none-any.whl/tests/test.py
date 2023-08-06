"""

Test for the simple code generator

@author -> LokotamaTheMastermind
@email -> lokotamathemastermind2@gmail.com
@created -> 3/8/2020
@license -> MIT
@categories -> helpers, handlers, python, pip, code. generators
@supported -> [>=python3]

@tests = [
    parameter
    startup
]

@success = [
    parameter
    startuo
]

"""

if __name__ == "__main__":
    from simple_code_generator.src.main import generate_code_simple
    import time

    test_type = input("What type of test do you want to perform: ")
    if test_type == "Startup":
        code = generate_code_simple()
        print(f"Generated code -> {code}")
        time.sleep(3)
        print("Done")
    elif test_type == "Parameters":
        first_param = input("Want to have the first param? | [y or n] --> ")
        if first_param == "y":
            first_param = input("What is the value for the first param | [int] --> ")
            param_one = int(first_param)
            second_param = input("What is the value for the second param | [int] --> ")
            param_two = int(second_param)
            third_param = input("What is the value for the third param | [int] --> ")
            param_three = int(third_param)
            fourth_param = input("What is the value for the fourth param | [int] --> ")
            param_four = int(fourth_param)
            code = generate_code_simple(param_two, param_two, param_three, param_four)
            print(f"\nGenerated code -> {code}")
            time.sleep(3)
            print("\nDone!")
        elif first_param == "n":
            print("Okay, why did you run the script in the first place!")
            time.sleep(2)
            exit()
    else:
        print("Sorry option not available, are you the author of the application!")
        print("Only the owner of the script knows the options")
        time.sleep(3)
        exit()

# importing the module and create a function to get live date and time.
def get_time():
    import datetime
    return datetime.datetime.now()


def take(n):
    if(n==1):
        print("Enter 1 for exercise/2 for food:-")
        data=int(input())
        value=input("please enter your data here:\n")
        if(data==1):
            with open("rohit-ex.txt","a") as rg:
                rg.write(str([str(get_time())])+": "+value+"\n")
                print("your data entered entered successfully")
        elif(data==2):
            with open("rohit-food.txt","a") as rg:
                rg.write(str([str(get_time())])+": "+value+"\n")
                print("your data entered entered successfully")
    elif(n==2):
        print("Enter 1 for exercise/2 for food:-")
        data = int(input())
        value = input("please enter your data here:\n")
        if (data == 1):
            with open("rajeev-ex.txt", "a") as ru:
                ru.write(str([str(get_time())]) + ": " + value + "\n")
                print("your data entered entered successfully")
        elif (data == 2):
            with open("rajeev-food.txt", "a") as ru:
                ru.write(str([str(get_time())]) + ": " + value + "\n")
                print("your data entered entered successfully")
    elif(n==3):
        print("Enter 1 for exercise/2 for food:-")
        data = int(input())
        value = input("please enter your data here:\n")
        if (data == 1):
            with open("deepak-ex.txt", "a") as dp:
                dp.write(str([str(get_time())]) + ": " + value + "\n")
                print("your data entered entered successfully")
        elif (data == 2):
            with open("deepak-food.txt", "a") as dp:
                dp.write(str([str(get_time())]) + ": " + value + "\n")
                print("your data entered entered successfully")
def retrieve(n):
    if(n==1):
        data=int(input("Enter 1 for exercise/2 for food:-"))
        if(data==1):
            with open("rohit-ex.txt") as rg:
                for i in rg:
                    print(i,end="")
        elif(data==2):
            with open("rohit.food") as rg:
                for i in rg:
                    print(i,end="")
    elif(n==2):
        data = int(input("Enter 1 for exercise/2 for food:-"))
        if (data == 1):
            with open("rajeev-ex.txt") as ru:
                for i in ru:
                    print(i, end="")
        elif (data == 2):
            with open("rajeev.food") as ru:
                for i in ru:
                    print(i, end="")
    elif(n==3):
        data = int(input("Enter 1 for exercise/2 for food:-"))
        if (data == 1):
            with open("deepak-ex.txt") as dp:
                for i in dp:
                    print(i, end="")
        elif (data == 2):
            with open("deepak.food") as dp:
                for i in dp:
                    print(i, end="")


dataSelector = int(input("Enter 1 to log your data/2 to retrieve your data:-"))
if(dataSelector==1):
    nameSelector = int(input("Enter 1 for Rohit/2 for Rajeev/3 for Deepak:-"))
    take(nameSelector)
elif(dataSelector==2):
    nameSelector = int(input("Enter 1 for Rohit/2 for Rajeev/3 for Deepak:-"))
    retrieve(nameSelector)
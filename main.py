import commands.calendar as cal
import commands.races as race

if __name__ == "__main__":
    choice = int(input("Please select what you want: "))
    if choice == 1:
        cal.create_csv()
    elif choice == 2:
        race.create_csv()

    


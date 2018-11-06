from schedule import Schedule


class Plan():

    def __init__(self):
        print("test1")

    def plan(self):
        print("test")

        schedule = Schedule([None] * 140)
        schedule.print_schedule( 0, 2)
        schedule.load_schedule()


if __name__ == "__main__":
    schedule = Plan()
    schedule.plan()

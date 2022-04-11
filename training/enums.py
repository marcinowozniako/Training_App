class Days:
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    Sunday = 6

    CHOICES = (
        (Monday, 'Monday'),
        (Tuesday, 'Tuesday'),
        (Wednesday, 'Wednesday'),
        (Thursday, 'Thursday'),
        (Friday, 'Friday'),
        (Saturday, 'Saturday'),
        (Sunday, 'Sunday'),
    )


class RepUnit:
    CHOICES = (
        ('Reps', 'Reps'),
        ('Seconds', 'Seconds'),
        ('Until Failure', 'Until Failure'),
    )


class WeightUnit:
    CHOICES = (
        ('Kg', 'Kg'),
        ('Body Weight', 'Body Weight'),
        )

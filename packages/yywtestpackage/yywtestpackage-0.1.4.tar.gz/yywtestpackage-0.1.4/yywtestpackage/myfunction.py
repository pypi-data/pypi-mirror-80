import pandas as pd


class Important_Dates():

    def __init__(self, birth_day, wedding_day):
        """Initialize class
        Args:
         birth_day: birth day in the format of 'YYYY-MM-DD'
         wedding_day: similar as birth_day
        """

        self.birth_day = pd.to_datetime(birth_day)
        self.wedding_day = pd.to_datetime(wedding_day)

    def get_days_passed_in_my_life(self):
        """Calcualte number of days passed in my life.
        """

        tmp = pd.Timestamp.now() - self.birth_day
        print('You have been living in this world for {} days!'.format(tmp.days))

    def get_days_passed_in_marriage(self):
        """Calculate number of days passed in marriage.
        """

        tmp = pd.Timestamp.now() - self.wedding_day
        print('You have been married for {} days!'.format(tmp.days))
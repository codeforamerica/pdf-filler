
import random

from faker import Factory
fake = Factory.create('en_US')


def example_pdf_answers(count=1):
    return [{
        'Address City': fake.city(),
        'Address State': 'CA',
        'Address Street': fake.street_address(),
        'Address Zip': fake.numerify('9####'),
        'Arrested outside SF': 'No',
        'Cell phone number': fake.numerify('###-###-####'),
        'Charged with a crime': 'No',
        'Date': fake.date_time_between('-7d').strftime('%m/%d/%Y'),
        'Date of Birth': fake.date_time_between('-65y','-20y').strftime('%m/%d/%Y'),
        'Dates arrested outside SF': '',
        'Drivers License': random.choice([fake.bothify('D#######'),'']),
        'Email Address': fake.random_element({
            fake.free_email(): 0.3,
            '': 0.7 }),
        'Employed': 'No',
        'First Name': fake.first_name(),
        'Home phone number': '',
        'How did you hear about the Clean Slate Program':
            random.choice(['From a friend', 'probation officer', '']),
        'If probation where and when?': '',
        'Last Name': fake.last_name(),
        'MI': fake.random_letter().upper(),
        'May we leave voicemail': 'Yes',
        'May we send mail here': 'Yes',
        'Monthly expenses': random.randint(0, 2000),
        'On probation or parole': 'No',
        'Other phone number': '',
        'Serving a sentence': 'No',
        'Social Security Number': fake.ssn(),
        'US Citizen': fake.random_element({'Yes':.8, 'No':.2}),
        'What is your monthly income': random.randint(0, 3000),
        'Work phone number': '',
    } for n in range(count)]

if __name__ == '__main__':
    from pprint import pprint
    pprint(example_pdf_answers(5))
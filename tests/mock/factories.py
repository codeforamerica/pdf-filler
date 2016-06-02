import random
import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Factory

from src.main import db
from src.pdfhook.models import PDFForm
from src.pdfhook.serializers import PDFFormDumper
import json



fake = Factory.create('en_US')
pdf_dumper = PDFFormDumper()

def lazy(func):
    return factory.LazyAttribute(func)


class CheckboxFactory:
    count = 0
    def __call__(self, name=None):
        self.count += 1
        name = name or 'Checkbox '+str(self.count)
        return {
            'name': name,
            'options': ['Yes', 'Off'],
            'type': 'button'
        }

class RadioFactory:
    count = 0
    def __call__(self, name=None, options=None):
        self.count += 1
        name = name or 'Group '+str(self.count)
        options = options or fake.bs().split(' ')
        if 'Off' not in options:
            options.append('Off')
        return {
            'name': name,
            'options': options,
            'type': 'button'
        }

class TextFactory:
    count = 0
    def __call__(self, name=None):
        self.count += 1
        name = name or 'Text Box '+str(self.count)
        return {
            'name': name,
            'type': 'text'
        }

checkbox = CheckboxFactory()
radio = RadioFactory()
text = TextFactory()


class FieldMapFactory:

    def __call__(self, n=None):
        if not n:
            n = random.randint(3, 20)
        fields = []
        for i in range(n):
            field_type = random.choice([checkbox, radio, text])
            fields.append(field_type())
        return fields

fake_field_map = FieldMapFactory()


class SessionFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = db.session


class PDFFormFactory(SessionFactory):
    class Meta:
        model = PDFForm
    id = factory.Sequence(lambda n: n)
    added_on = lazy(lambda obj: fake.date_time_between('-2w'))
    original_pdf = lazy(lambda obj: fake.binary(1024))
    original_pdf_title = factory.Sequence(lambda n: "Form {}.pdf".format(n))
    field_map = lazy(lambda obj: json.dumps(fake_field_map()))
    post_count = lazy(lambda obj: random.randint(0, 100))
    latest_post = lazy(lambda obj: fake.date_time_between(obj.added_on))


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
    from src.main import create_app
    app = create_app()
    app.config['SERVER_NAME'] = 'pdfhook.mock.com'
    with app.app_context():
        pdfs = [PDFFormFactory.build() for i in range(5)]
        pprint([pdf_dumper.dump(pdf).data for pdf in pdfs])
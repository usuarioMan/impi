from faker import Faker


def fake_data_generetor():
    fake = Faker()
    return fake.text()

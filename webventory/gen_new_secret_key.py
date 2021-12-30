from django.core.management import utils


def main():
    with open('key.txt', 'w') as file:
        file.write(utils.get_random_secret_key())


if __name__ == '__main__':
    main()

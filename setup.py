import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="trello_client-basics-api-nightgust_2",
    version="0.0.2",
    author="Александр Плугарев",
    author_email="nightgust@gmail.com",
    description="API клиент для работы с трелло - получать сипсок задач доски, создавать задачи, двигать задачи по этапам",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/avplugarev/trello_client.git", # Адрес сайта моего пакета.
    packages=setuptools.find_packages(), #автоматически собеерем список всех пакретов необходимых для работы.
    classifiers=[ "Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License", "Operating System :: OS Independent", ],
    python_requires='>=3.6',)